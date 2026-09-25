#!/bin/sh
# Serialize key repeats so each adjustment is reflected in the notification.
set -eu
exec 9>"${XDG_RUNTIME_DIR:?}/qtile-media-control.lock"
flock 9
export LC_ALL=C
case "${1:-}" in
    volume-up) pactl set-sink-volume @DEFAULT_SINK@ +5% ;;
    volume-down) pactl set-sink-volume @DEFAULT_SINK@ -5% ;;
    mic-mute) pactl set-source-mute @DEFAULT_SOURCE@ toggle ;;
    mute) pactl set-sink-mute @DEFAULT_SINK@ toggle ;;
    brightness-up) brightnessctl --class=backlight --min-value=1 set +5% >/dev/null ;;
    brightness-down) brightnessctl --class=backlight --min-value=1 set 5%- >/dev/null ;;
    *) exit 2 ;;
esac

case "$1" in
    mic-mute)
        if pactl get-source-mute @DEFAULT_SOURCE@ | grep -q 'yes'; then
            title='Microphone muted'
            icon=microphone-sensitivity-muted
        else
            title='Microphone unmuted'
            icon=microphone-sensitivity-high
        fi
        value=-1
        ;;
    brightness-*)
        current=$(brightnessctl --class=backlight get)
        maximum=$(brightnessctl --class=backlight max)
        value=$((100 * current / maximum))
        title="Brightness: $value%"
        icon=display-brightness
        ;;
    *)
        value=$(pactl get-sink-volume @DEFAULT_SINK@ | awk 'NR == 1 {gsub(/%/, "", $5); print $5}')
        if pactl get-sink-mute @DEFAULT_SINK@ | grep -q 'yes'; then
            title='Volume: muted'
            icon=audio-volume-muted
            value=0
        else
            title="Volume: $value%"
            icon=audio-volume-high
        fi
        ;;
esac
# Release the adjustment lock before starting the persistent single-instance OSD.
flock -u 9
exec 9>&-
osd_script="$(dirname "$0")/media-osd.py"
/usr/bin/python "$osd_script" "${icon}-symbolic" "$title" "$value" \
    >>"${XDG_RUNTIME_DIR}/qtile-media-osd.log" 2>&1 &
