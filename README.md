# Woodtick Walking Simulator

This is a walking simulator for **Monkey Island 2** that lets Guybrush, the main character, walk at random to different locations in the town known as 'Woodtick', which Guybrush visits at the beginning of the game.
The music beautifully changes as Guybrush enters different locations.

This is intended for academic use as a dataset generator for machine learning of conditional music data.
Do not hesitate to [contact me](mailto:fabian.ostermann@tu-dortmund.de) if you need any help!

### Setup ScummVM code

***Disclaimer***: *The install scripts were developed and tested on Linux. Imho, they could probably work on Windows using WSL or MinGW.*

The code of the game emulator [ScummVM](https://www.scummvm.org/) is not included in this repository.
It also is intendedly NOT setup as an submodule (because of management overhead).

Therefore, just clone the scummvm-WoodtickRL repo in a subdirectory and check out the branch with following commands:
```
git clone https://github.com/fabianostermann/scummvm-WoodtickRL.git scummvm-WoodtickRL
cd scummvm-WoodtickRL
git checkout WoodtickRL
```

### Compile ScummVM

For Linux, install necessary packages (tested for Ubuntu 20.04 & 22.04):

```
apt install g++ make git nasm libsdl2-dev libsdl2-net-dev liba52-dev libjpeg-turbo8-dev libmpeg2-4-dev libogg-dev libvorbis-dev libflac-dev libmad0-dev libpng-dev libtheora-dev libfaad-dev libfluidsynth-dev libfreetype6-dev zlib1g-dev libfribidi-dev libgif-dev libcurl4-openssl-dev libgtk-3-dev libspeechd-dev libsndio-dev libunity-dev libvpx-dev libmikmod-dev
```

For compiling, use the bash make script: `bash make_for_scumm_only.sh --configure`

For more information on compiling ScummVM, see:
<https://wiki.scummvm.org/index.php?title=Compiling_ScummVM/GCC>

### Running the simulator

You will need the actual game in order to run it.
If you do not own it, you can [download it from archive.org](https://archive.org/details/msdos_Monkey_Island_2_-_LeChucks_Revenge_1991)
Put the monkey2 game data in a subfolder called `gamedata/monkey2-game`. The necessary savegame files are already provided by this repository.

Test your setup by running `bash start_woodtick.sh`.

You should now be able to record a log with `bash record_iMuse_monkey2.sh`,\
or create a whole dataset of multiple logs with `bash generate_database.sh <desired_location>`


