#!/usr/bin/env bash
set -euo pipefail

# Runtime state survives Qtile reloads/restarts, but resets at the next login.
state_file="${XDG_RUNTIME_DIR:?}/qtile-display-mode"
exec 9>"${XDG_RUNTIME_DIR}/qtile-display-mode.lock"
flock 9
mode=regular
[[ ! -f "$state_file" ]] || read -r mode < "$state_file"
toggle=false
if [[ "${1:-}" == --toggle ]]; then
    toggle=true
    shift
    if [[ "$mode" == laptop ]]; then mode=regular; else mode=laptop; fi
fi

SCREEN_NAME=${1:-eDP-1}
HDMI_NAME=${2:-HDMI-1}
HDMI2_NAME=${3:-HDMI-2}
outputs=$(xrandr --query)
is_connected() {
    awk -v output="$1" '$1 == output && $2 == "connected" { found = 1 } END { exit !found }' <<< "$outputs"
}

if ! is_connected "$SCREEN_NAME"; then
    notify-send 'Display mode unchanged' "Laptop output $SCREEN_NAME is unavailable."
    exit 1
fi

args=(--output "$SCREEN_NAME" --auto --primary --rotate normal --pos 0x0)
if [[ "$mode" == laptop ]]; then
    # Disable every external output, even if a powered-off monitor reports connected.
    while read -r output; do
        [[ "$output" == "$SCREEN_NAME" ]] || args+=(--output "$output" --off)
    done < <(awk '$2 == "connected" || $2 == "disconnected" {print $1}' <<< "$outputs")
else
    if is_connected "$HDMI_NAME"; then
        args+=(--output "$HDMI_NAME" --auto --rotate normal --above "$SCREEN_NAME")
    else
        args+=(--output "$HDMI_NAME" --off)
    fi
    if is_connected "$HDMI2_NAME"; then
        if is_connected "$HDMI_NAME"; then
            args+=(--output "$HDMI2_NAME" --auto --right-of "$HDMI_NAME" --rotate left)
        else
            args+=(--output "$HDMI2_NAME" --auto --above "$SCREEN_NAME" --rotate normal)
        fi
    else
        args+=(--output "$HDMI2_NAME" --off)
    fi
fi

xrandr "${args[@]}"
printf '%s\n' "$mode" > "$state_file"
setxkbmap -option compose:ralt
# Keep the brightness selected by the user/power manager.
# Release before reloading: Qtile startup hooks also call this script.
flock -u 9
if "$toggle"; then
    qtile cmd-obj -o root -f reload_config
    if [[ "$mode" == laptop ]]; then
        notify-send 'Displays: laptop only' 'Super+Ctrl+D restores your regular screens.'
    else
        notify-send 'Displays: regular layout' 'Super+Ctrl+D switches to laptop only.'
    fi
fi
