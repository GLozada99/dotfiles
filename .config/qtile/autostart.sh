#!/bin/sh
function run {
    if ! pgrep $1 ;
    then
        $@&
    fi
}

feh --bg-scale /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png
picom & disown # --experimental-backends --vsync should prevent screen tearing on most setups if needed

~/.config/qtile/scripts/check_battery.sh & disown
run /usr/bin/blueman-applet & disown
run /usr/bin/nm-applet & disown
run /usr/bin/variety & disown
run /usr/bin/flameshot & disown
run /usr/bin/caffeine-indicator & disown
run /usr/bin/cbatticon & disown

eos-welcome & disown


/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & disown # start polkit agent from GNOME
