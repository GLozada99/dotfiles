#!/usr/bin/env bash

SCREEN_NAME=${1:-"eDP-1"}
HDMI_NAME=${2:-"HDMI-1"}
HDMI2_NAME=${3:-"HDMI-2"}

is_connected() {
    xrandr --query | awk -v output="$1" '$1 == output && $2 == "connected" { found = 1 } END { exit !found }'
}

if is_connected "$SCREEN_NAME"; then
    xrandr --output "$SCREEN_NAME" --auto --gamma 1:1:1
fi

if is_connected "$HDMI_NAME" && is_connected "$HDMI2_NAME"; then
    xrandr --output "$HDMI_NAME" --auto --above "$SCREEN_NAME"
    xrandr --output "$HDMI2_NAME" --auto --right-of "$HDMI_NAME" --rotate left
    setxkbmap -option compose:ralt
elif is_connected "$HDMI_NAME"; then
    xrandr --output "$HDMI_NAME" --auto --above "$SCREEN_NAME"
    xrandr --output "$HDMI2_NAME" --off
    setxkbmap -option compose:ralt
elif is_connected "$HDMI2_NAME"; then
    xrandr --output "$HDMI_NAME" --off
    xrandr --output "$HDMI2_NAME" --auto --above "$SCREEN_NAME"
    setxkbmap -option compose:ralt
else
    xrandr --output "$HDMI_NAME" --off
    xrandr --output "$HDMI2_NAME" --off
    setxkbmap -option compose:ralt
fi

brightnessctl set 19
