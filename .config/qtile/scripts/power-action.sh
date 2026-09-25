#!/bin/sh
# Shared actions for the native Qtile chord and the clickable Rofi menu.
require_locker() {
    if ! command -v i3lock >/dev/null || ! command -v xss-lock >/dev/null; then
        notify-send 'Screen locker not installed' 'Install the i3lock and xss-lock packages.'
        return 1
    fi
    if ! pgrep -u "$(id -u)" -x xss-lock >/dev/null; then
        notify-send 'Screen lock listener is not running' \
            'Run ~/.config/qtile/scripts/session-power.sh, or log out and back in.'
        return 1
    fi
}

case "${1:-}" in
    lock) require_locker && xset s activate ;;
    logout) loginctl terminate-session "$XDG_SESSION_ID" ;;
    sleep) require_locker && systemctl suspend ;;
    hibernate) require_locker && systemctl hibernate ;;
    *) exit 2 ;;
esac
