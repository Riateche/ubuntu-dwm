#!/bin/bash

feh --bg-scale ~/Pictures/tardis_doctor_who_desktop_1920x1080_wallpaper-1065045.jpg

killall stalonetray pidgin gxneur nm-applet xbindkeys gm-notify
stalonetray -bg "#333" --geometry +0+16 &
pidgin &
gxneur &
nm-applet &
rm ~/.dwm/mail_count
~/.dwm/gmail-checker/gm-notify &
xbindkeys   # runs as daemon itself

setxkbmap "us,ru(typewriter)" -option grp:toggle,grp_led:scroll
xset r rate 300 32

kill `cat /tmp/pid_dwm_title`
~/.dwm/set_title.sh &
echo $! > /tmp/pid_dwm_title
