from libqtile import hook, qtile
import subprocess
import os
import time

from modules.constants import GROUP_NAMES


RESET = time.time()
group_match_map = {entry["name"]: entry["matches"] for entry in GROUP_NAMES}


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([script])
    global RESET
    RESET = time.time()

@hook.subscribe.startup
def screen():
    script = os.path.expanduser('~/.config/qtile/screen.sh')
    subprocess.call([script])
    global RESET
    RESET = time.time()


@hook.subscribe.client_managed
def show_window(window):
    window.group.cmd_toscreen()


@hook.subscribe.client_new
def move_window_to_group(window):
    global RESET
    if (time.time() - RESET) <= 5:
        return

    group_name = qtile.current_screen.group.name

    try:
        wm_name = window.window.get_wm_class()[0]
    except IndexError:
        return
    if wm_name in group_match_map[group_name]:
        return

    for name, matches in group_match_map.items():
        if wm_name in matches:
            window.togroup(name)


