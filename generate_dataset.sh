#!/bin/bash

# Read about functions and simple arithmetic:
# https://www.baeldung.com/linux/bash-functions
###############################################

if [ $1 == "" ]; then
  DATASET_DIR="dataset"
else
  DATASET_DIR="$1"
fi

NUM_OF_PARALLEL_INSTANCES=20

# calculate with woodtick max sim time=10min, add 5 seconds offset
SLEEP_TIME="$((10*60/$NUM_OF_PARALLEL_INSTANCES+5))s"

echo "Using $NUM_OF_PARALLEL_INSTANCES parallel instances -> set sleep time to $SLEEP_TIME."

for ID in {001..010} # << set number of runs
do	
	dump_dir="$DATASET_DIR/$ID/"
	echo "Attempting to generate $dump_dir.."

	if [ ! -e $dump_dir ]
	then
		./record_iMuse_monkey2.sh "$dump_dir" &
		echo "Wait $SLEEP_TIME before starting next instance."
		sleep $SLEEP_TIME
	else
		echo "Directory exists: $dump_dir.. skipping!" 
	fi
done

echo "Dataset generation ended."
