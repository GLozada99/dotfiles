#!/bin/sh
# xss-lock delays suspend/hibernate until i3lock has secured the screen.
for program in i3lock xss-lock xfconf-query; do
    if ! command -v "$program" >/dev/null 2>&1; then
        notify-send 'Session power setup incomplete' 'Install i3lock and xss-lock, then rerun ~/.config/qtile/scripts/session-power.sh.'
        exit 1
    fi
done

if ! pgrep -u "$(id -u)" -x xss-lock >/dev/null; then
    xss-lock --transfer-sleep-lock -- i3lock --nofork --color=282a36 &
    # Check that the listener survives startup before delegating locking to it.
    sleep 1
    if ! pgrep -u "$(id -u)" -x xss-lock >/dev/null; then
        notify-send 'Screen locking unavailable' 'xss-lock failed to start; lid settings were not changed.'
        exit 1
    fi
fi

set_property() {
    xfconf-query -c xfce4-power-manager -p "/xfce4-power-manager/$1" \
        --create --type "$2" --set "$3"
}

# Xfce 4.20 ignores lid-close with external monitors. Delegate to logind.
# /etc/systemd/logind.conf must specify HandleLidSwitchDocked=suspend.
# xss-lock owns locking for all logind sleep requests.
set_property logind-handle-lid-switch bool true
set_property lock-screen-suspend-hibernate bool false
