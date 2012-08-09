while true; do                                 
  #------------ Sound
  pactl list sinks  | sed -n '/alsa_output.pci-0000_00_1b.0.analog-stereo/,$p' | grep "Mute: yes" > /dev/null
  if  [ $? -eq 0 ] 
  then
    volume=mute
  else
    volume=`pactl list sinks  | sed -n '/alsa_output.pci-0000_00_1b.0.analog-stereo/,$p' | grep "Volume: 0:" | sed 's/[ \t]\+/ /g' | cut -d " " -f 4`
  fi

  #------------ Mail
  mail_count=`cat ~/.dwm/mail_count`
  if [ $mail_count -gt 0 ]; then
    mail="| Mail $mail_count "
  else
    mail=""
  fi
  
  #------------ Brightness
  br=`~/.dwm/get_brightness.sh`

  #------------ Battery
  BAT_INFO="/proc/acpi/battery/BAT0/info"
  BAT_STATE="/proc/acpi/battery/BAT0/state"
  #using last full capacity because it's more accurate then design capacity
  BAT_CAPACITY=`cat $BAT_INFO |grep "last full capacity:"|cut -f9 -d\ `
  #remaining capacity
  BAT_LEVEL=`cat $BAT_STATE | grep remaining |cut -f8 -d\ `
  BAT_PERCENT=`calc "round($BAT_LEVEL*100/$BAT_CAPACITY)" | sed -e 's/^[ \t]*//'`
  if grep off-line /proc/acpi/ac_adapter/AC/state > /dev/null; then
    AC="(-)"
  else
    AC="(+)"
  fi

  #----------- Pidgin status
  if purple-remote getstatus | grep away > /dev/null; then
    PIDGIN="| Pidgin away "
  else
    PIDGIN=""
  fi 

  xsetroot -name "$PIDGIN$mail| Br $br | Vol $volume | Bat $BAT_PERCENT% $AC | $(date +"%a, %d.%m.%y %H:%M")"
  sleep 1s
done 
