#!/usr/bin/env bash

# Custom Rofi bindings return 10..13; Enter/mouse selection still works.
lock="[l] Lock"
logout="[o] Log out"
sleep="[s] Sleep"
hibernate="[h] Hibernate"
reboot="Restart"
shutdown="Shutdown"
selected_option=$(printf '%s\n' "$lock" "$logout" "$sleep" "$hibernate" "$reboot" "$shutdown" |
    rofi -dmenu -i -p Power \
        -config "$HOME/.config/rofi/powermenu.rasi" \
        -font 'Cascadia Code 12' -lines 6 \
        -kb-custom-1 l -kb-custom-2 o -kb-custom-3 s -kb-custom-4 h)
result=$?
case "$result" in
    0) ;;
    10) selected_option=$lock ;;
    11) selected_option=$logout ;;
    12) selected_option=$sleep ;;
    13) selected_option=$hibernate ;;
    *) exit 0 ;;
esac

action_script="$HOME/.config/qtile/scripts/power-action.sh"
case "$selected_option" in
    "$lock") exec "$action_script" lock ;;
    "$logout") exec "$action_script" logout ;;
    "$sleep") exec "$action_script" sleep ;;
    "$hibernate") exec "$action_script" hibernate ;;
    "$reboot") systemctl reboot ;;
    "$shutdown") systemctl poweroff ;;
esac
