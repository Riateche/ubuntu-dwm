#!/bin/bash
max=`cat /sys/class/backlight/acpi_video0/max_brightness`
if [ $1 -eq  9 ]; then
  target=$max
else
  target=`calc "round($1*$max/9)"`
fi 

echo $target | sudo  tee /sys/class/backlight/acpi_video0/brightness

