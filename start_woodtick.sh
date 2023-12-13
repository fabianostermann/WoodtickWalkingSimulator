#!/bin/bash

###############
### find information of the options here:
### https://docs.scummvm.org/en/latest/advanced_topics/configuration_file.html
### https://docs.scummvm.org/en/latest/advanced_topics/command_line.html
###############

echo "Start time: $(date)"

SCUMMVM_PATH=$(realpath "scummvm-WoodtickRL/scummvm")
CONFIG_FILE=$(realpath "scummvm.ini")

DEBUGGER=""

if [ "$1" == "--menu" ]; then
	$SCUMMVM_PATH --config=$CONFIG_FILE
	exit 0
else if [ "$1" == "" ]; then
	echo "no parameters given."
else if [ "$1" == "--help" ]; then
	$SCUMMVM_PATH --help
	exit 0
else if [ "$1" == "--debug" ]; then
	DEBUGGER="gdb -ex=run --args"
else if [ "$1" == "--dump-dir" ]; then
	echo "Dump directory given: $2"
else
	$SCUMMVM_PATH $@
	exit 0
fi
fi
fi
fi
fi

GAME_ID="monkey2"
GAMEPATH=$(realpath "gamedata/$GAME_ID-game")
SAVEPATH=$(realpath "gamedata/$GAME_ID-savegames")

LOAD_SAVESLOT=""
LOAD_SAVESLOT="--save-slot=1"

SCALE_FACTOR=""
SCALE_FACTOR="--scale-factor=3" # use this to scale up renders

DUMP_MIDI=""
DUMP_MIDI="--dump-midi" # enable this to dump a midi file

MUSIC_TEMPO=""
#MUSIC_TEMPO="--tempo=100" # default: 100 [in percent 50-200]

DISABLE_DISPLAY=""
#DISABLE_DISPLAY="--disable-display=1" # enable this to disable renders

DEBUG_LEVEL=""
#DEBUG_LEVEL="--debuglevel=0"

if [ "$1" == "--dump-dir" ]; then
	if [ "$2" == "" ]; then
		echo "No valid dump directory given."
	else
		DUMP_DIR=$2
		mkdir -p $DUMP_DIR
		cd $DUMP_DIR
	fi
fi

# start ScummVM with options:
$DEBUGGER \
$SCUMMVM_PATH \
	--path=$GAMEPATH \
	--savepath=$SAVEPATH $LOAD_SAVESLOT \
	--config=$CONFIG_FILE \
	$DEBUG_LEVEL \
	$DISABLE_DISPLAY $SCALE_FACTOR \
	$DUMP_MIDI $MUSIC_TEMPO \
	"$GAME_ID"



