#!/bin/sh
if [[ -n `xrandr --query | grep "HDMI1 connected"` ]]
then
    xrandr --output HDMI1 --mode 1920x1080i --right-of eDP1
else
    xrandr --output HDMI1 --off
fi