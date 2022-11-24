#!/bin/sh
function run {
    if ! pgrep $1 ;
    then
        $@&
    fi
}

feh --bg-scale /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png
picom & disown # --experimental-backends --vsync should prevent screen tearing on most setups if needed

# Low battery notifier
~/.config/qtile/scripts/check_battery.sh & disown
run /usr/bin/blueman-applet &
run /usr/bin/variety &
run /usr/bin/flameshot &
run /usr/bin/megasync &

eos-welcome & disown


/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & disown # start polkit agent from GNOME
