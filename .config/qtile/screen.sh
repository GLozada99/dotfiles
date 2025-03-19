#!/bin/sh

SCREEN_NAME=${1:-"eDP-1"}
HDMI_NAME=${2:-"HDMI-1"}
HDMI2_NAME=${2:-"HDMI-2"}

echo $SCREEN_NAME
echo $HDMI_NAME

if [[ -n `xrandr --query | grep "$HDMI_NAME connected"` ]]
then
    # xrandr --output $HDMI_NAME --mode 1920x1080 --right-of $SCREEN_NAME
    xrandr --output $SCREEN_NAME --gamma 1:1:1
    xrandr --output $HDMI_NAME --mode 1920x1080 --above $SCREEN_NAME
    xrandr --output $HDMI2_NAME --mode 1920x1080 --right-of $SCREEN_NAME --right-of $HDMI_NAME --rotate left
    setxkbmap -option compose:ralt
else
    xrandr --output $HDMI_NAME --off
    xrandr --output $SCREEN_NAME --gamma 1:1:1
    setxkbmap -option compose:ctrl
    setxkbmap -option compose:ralt
fi

brightnessctl set 19
