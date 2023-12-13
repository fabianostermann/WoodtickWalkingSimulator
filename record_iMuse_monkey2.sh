#!/bin/bash

if [ "$1" == "" ]; then
	echo "Please provide a dump directory."
	exit 0
fi

DUMP_DIR=$1

mkdir -p $DUMP_DIR

echo "Start log record of $DUMP_DIR.."
bash start_woodtick.sh --dump-dir $DUMP_DIR > $DUMP_DIR/dump.log

echo "Make MIDICSV file for $DUMP_DIR.."
midicsv $DUMP_DIR/dump.mid > $DUMP_DIR/dump.midicsv

echo "Compress $DUMP_DIR.."
gzip $DUMP_DIR/*.midicsv $DUMP_DIR/*.log

echo "Recording of $DUMP_DIR ended."
