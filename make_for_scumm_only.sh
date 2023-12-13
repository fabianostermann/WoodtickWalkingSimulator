#!/bin/bash

cd scummvm-WoodtickRL

CPU_COUNT=$(grep -c ^processor /proc/cpuinfo)
JOBS=$(python -c "print($CPU_COUNT+4)")
echo "Found $CPU_COUNT cpus, set jobs=$JOBS."

perform_configure=false
perform_clean=false

for arg in "$@"; do
  if [[ $arg == "--configure" ]]; then
    perform_configure=true
  fi
  if [[ $arg == "--clean" ]]; then
    perform_clean=true
  fi
done

if $perform_configure; then
  ./configure \
  	--disable-all-engines \
  	--enable-engine=scumm \
  	--enable-eventrecorder
  	# enable event recorder to get --disable-display option
fi

if $perform_clean; then
  make clean
fi

time make --jobs=$JOBS


