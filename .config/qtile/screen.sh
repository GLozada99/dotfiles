#!/bin/sh

SCREEN_NAME=${1:-"eDP-1"}
HDMI_NAME=${2:-"HDMI-1"}

setxkbmap -option compose:rctrl

if [[ -n `xrandr --query | grep "$HDMI_NAME connected"` ]]
then
    xrandr --output $HDMI_NAME --mode 1920x1080 --right-of $SCREEN_NAME
    setxkbmap -option compose:menu
else
    xrandr --output $HDMI_NAME --off
fi
