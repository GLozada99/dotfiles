#!/bin/sh

if [[ -n `xrandr --query | grep "HDMI1 connected"` ]]
then
    xrandr --output HDMI1 --mode 1920x1080 --right-of eDP1
	setxkbmap -option compose:rctrl
    setxkbmap -option compose:menu
else
    xrandr --output HDMI1 --off
    setxkbmap -option compose:rctrl
fi
