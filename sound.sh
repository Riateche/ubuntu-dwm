#!/bin/bash

# Usage: sound.sh mute|up|down


if [ "$1" = "mute" ]; then
  pacmd dump|awk --non-decimal-data '$1~/set-sink-mute/{system ("pacmd "$1" "$2" "($3=="yes"?"no":"yes"))}' > /dev/null
else
  if [ "$1" = "up" ]; then
    sign=+
  else
    sign=-
  fi
  pacmd dump|awk --non-decimal-data '$1~/set-sink-volume/{system ("pacmd "$1" "$2" "$3'$sign'2000)}' > /dev/null
fi

