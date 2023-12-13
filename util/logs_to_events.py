#!/usr/bin/python3

import os

import pandas as pd
import pretty_midi

from time import time as now

VERBOSE = False

DEFAULT_LOG_FILENAME = "dump.log.gz"
LINE_TAG = "WOODTICK RL :"
DEFAULT_MIDI_FILENAME = "dump.mid"

OUTFILE_NOTES = "notes.csv"
OUTFILE_NOTES_NODRUMS = "notes_nodrums.csv"
OUTFILE_ROOMS = "rooms.csv"

room_to_idx_map = {
    7: 0,
    "outside": 0,
    8: 1,
    "wally": 1,
    9: 2,
    "bar": 2,
    12: 3,
    "hotel": 3,
    14: 4,
    "laundry": 4,
    15: 5,
    "woodshop": 5,
}


def room_to_idx(room):
    return room_to_idx_map[room]


# temp files that have to be global due to use of exec()
room = None
millis = None
delta = []
message = []


def process_dir(path_to_dir):
    if VERBOSE:
        print(f"Processing directory.. ({path_to_dir})")

    for no_drums in [True, False]:
        path_to_midi = os.path.join(path_to_dir, DEFAULT_MIDI_FILENAME)
        midi_list, offset = midi_to_notes(
            path_to_midi, return_offset=True, no_drums=no_drums
        )
        notes_df = pd.DataFrame(midi_list)

        # write notes to file
        notes_out_file = os.path.join(
            path_to_dir, OUTFILE_NOTES_NODRUMS if no_drums else OUTFILE_NOTES
        )
        notes_df.to_csv(notes_out_file, float_format="%.3f", index=False)
        os.system("gzip -f " + notes_out_file)

    path_to_log = os.path.join(path_to_dir, DEFAULT_LOG_FILENAME)
    rooms_list = log_to_rooms(path_to_log, clean_up=True, additional_offset=offset)
    rooms_df = pd.DataFrame(rooms_list)

    # write room info to file
    rooms_out_file = os.path.join(path_to_dir, OUTFILE_ROOMS)
    rooms_df.to_csv(rooms_out_file, float_format="%.3f", index=False)

    os.system("gzip -f " + rooms_out_file)


def midi_to_notes(
    path_to_file,
    return_offset=False,
    no_drums=False,
):
    midi_data = pretty_midi.PrettyMIDI(path_to_file)
    notes = []

    if VERBOSE and no_drums:
        print("Ignoring drum events..")

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            if no_drums and instrument.is_drum:
                continue  # skip drum instrument if desired
            notes.append(
                {
                    "start": note.start,
                    "duration": note.get_duration(),
                    "pitch": note.pitch,
                    "velocity": note.velocity / 127.0,
                    "instrument": -1 if instrument.is_drum else instrument.program,
                }
            )
        # make sure, no pitch_bend occur in midi data
        count_pitch_bends = 0
        for pitch_bend in instrument.pitch_bends:
            if pitch_bend.pitch != 0:
                count_pitch_bends += 1
        if count_pitch_bends > 0:
            if VERBOSE:
                print("WARNING:", count_pitch_bends, "pitch bends were ignored.")
        # print(instrument.control_changes[0])
        for control_change in instrument.control_changes:
            pass  # print(control_change)

    # sort after start, instrument (drums=-1 first), and pitch, respectively
    notes = sorted(notes, key=lambda x: (x["start"], x["instrument"], x["pitch"]))

    # remove offset from start
    offset = notes[0]["start"]
    for i in range(len(notes)):
        notes[i]["start"] -= offset

    # add delta information
    notes[0]["delta"] = notes[0]["start"]
    for i in range(len(notes) - 1):
        notes[i + 1]["delta"] = notes[i + 1]["start"] - notes[i]["start"]

    if return_offset:
        return notes, offset
    else:
        return notes


def log_to_rooms(
    path_to_file,
    clean_up=False,  # rm extracted log file after read
    additional_offset=0,
):
    if VERBOSE:
        print(f"Processing log file.. ({path_to_file})")

    # unzip if necessary
    start_time = now()
    if path_to_file.split(".")[-1] == "gz":
        path_to_unzipped_file = path_to_file[: -len(".gz")]
        # check if exist, then unzipping is not needed
        if not os.path.isfile(path_to_unzipped_file):
            if VERBOSE:
                print("Unzip.. ", end="")
            os.system("gunzip -k -f " + path_to_file)
            if VERBOSE:
                print(f"({now() - start_time:.3f}s)")

    else:
        path_to_unzipped_file = path_to_file

    rooms_list = []
    last_room = -1  # set to invalid room number

    start_time = now()
    if VERBOSE:
        print("Processing lines", end="")
    with open(path_to_unzipped_file, "r") as lines:
        for i, line in enumerate(lines):
            # print("Read:",line)
            if not line.startswith(LINE_TAG):
                continue
            command = line[len(LINE_TAG) :]

            # load command line variables
            exec(command.strip(), globals())

            if last_room != room:
                rooms_list.append({"time": millis / 1000, "room": room})
                last_room = room

            if i % 500 == 0:
                if VERBOSE:
                    print(".", end="", flush=True)

    initial_offset = rooms_list[0]["time"]
    for i in range(len(rooms_list)):
        rooms_list[i]["time"] = round(
            max(rooms_list[i]["time"] - initial_offset - additional_offset, 0), 3
        )

    if VERBOSE:
        print(f" done. ({now() - start_time:.3f}s)")

    if clean_up:
        if VERBOSE:
            print("Removing extracted log..", end="")
        os.system("rm " + path_to_unzipped_file)
    if VERBOSE:
        print(" done.")

    return rooms_list


def read_csv_to_df(file):
    if not os.path.exists(file):
        file = file + ".gz"
    return pd.read_csv(file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Utility to convert note event features from midi to csv"
        + " as well as to load room changes as environmental information."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose prints"
    )
    parser.add_argument(
        "--dir",
        dest="path_to_dir",
        type=str,
        default=None,
        help="give directory where the log and midi files are located (mandatory).",
    )
    args = parser.parse_args()

    VERBOSE = args.verbose

    if args.path_to_dir is not None:
        process_dir(args.path_to_dir)
        exit()

    parser.print_help()
