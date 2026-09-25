#!/bin/sh
# Match full command lines: several applet names exceed pgrep's 15-character
# process-name limit. Only start installed programs owned by this session's user.
run() {
    command -v "$1" >/dev/null 2>&1 || return 0
    if ! pgrep -u "$(id -u)" -f "(^|/)${1##*/}([[:space:]]|$)" >/dev/null; then
        "$@" &
    fi
}

feh --bg-scale /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png
picom & # --experimental-backends --vsync should prevent screen tearing on most setups if needed

# ~/.config/qtile/scripts/check_battery.sh &
run /usr/bin/blueman-applet
run /usr/bin/nm-applet
run /usr/bin/variety
run /usr/bin/flameshot
run /usr/bin/copyq
# run /usr/bin/caffeine-indicator &
# run /usr/bin/clight-gui &
# run /usr/bin/spotify-tray &

eos-welcome &


/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & # start polkit agent from GNOME

# Power Options owns hardware profiles; Xfce handles display/lid/idle policy.
# Configure the system services as described in POWER.md before using both.
# run /usr/bin/power-options-tray
run /usr/bin/xfce4-power-manager

# Configure lid suspend and start the lock-before-sleep listener.
"$HOME/.config/qtile/scripts/session-power.sh"

# Qtile handles brightness keys and uses Dunst for feedback.
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/handle-brightness-keys --create --type bool --set false
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/show-brightness-popup --create --type bool --set false
