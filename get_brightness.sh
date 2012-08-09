#!/bin/bash
max=`cat /sys/class/backlight/acpi_video0/max_brightness`
current=`cat /sys/class/backlight/acpi_video0/brightness`
if [ $current -eq  $max ]; then
  r=9
else
  r=`calc "round($current*9/$max)"`
fi 
echo $r


#9 15
#8 13
#7 12
#6 10
#5  8
#4  7
#3  5
#2  3
#1  2
#0  0


