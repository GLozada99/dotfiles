import subprocess
import os
import time
from collections import deque, defaultdict

from libqtile import bar, hook, qtile
from libqtile.widget.chord import Chord
from qtile_extras.widget.currentlayout import CurrentLayoutIcon
from libqtile.widget.windowname import WindowName

from modules.constants import GROUP_NAMES

RESET = time.time()
RESET_GROUP_CHANGE = time.time()
PREVIOUS_GROUPS = defaultdict(lambda: deque([], maxlen=3))


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
def show_window(client):
    global RESET, PREVIOUS_GROUPS, RESET_GROUP_CHANGE
    if "qtile-scratchpad" in (client.get_wm_class() or []):
        return
    if (time.time() - RESET) <= 1:
        return
    client.group.toscreen()
    RESET_GROUP_CHANGE = time.time()


@hook.subscribe.client_killed
def client_killed(client):
    global RESET_GROUP_CHANGE
    group = _get_previous_group(3) or _get_previous_group(2)
    if not group:
        return
    if (time.time() - RESET_GROUP_CHANGE) > 5:
        return
    qtile.groups_map[group].toscreen()


@hook.subscribe.client_focus
def client_focus(client):
    # No need to have two of the same group together, only add the current one if the
    # previous is not the same, except if the current one is floating.
    # if client.group.name != _get_previous_group(1) or client.floating:
    PREVIOUS_GROUPS[qtile.current_screen].append(client.group.name)


@hook.subscribe.client_new
def move_window_to_group(window):
    if "qtile-scratchpad" in (window.get_wm_class() or []):
        return
    global RESET
    if (time.time() - RESET) <= 1:
        return

    group_match_map = {entry["name"]: entry["matches"] for entry in GROUP_NAMES}
    group_name = qtile.current_screen.group.name

    try:
        wm_name = window.window.get_wm_class()[0]
    except IndexError:
        return

    # checks whether the current group matches
    if wm_name in group_match_map[group_name]:
        return

    # Checks for a match in all other groups
    for name, matches in group_match_map.items():
        if wm_name in matches:
            window.togroup(name)
            break


def _get_previous_group(n: int):
    try:
        # last index is current group, so second to last is previous
        return PREVIOUS_GROUPS[qtile.current_screen][-n]
    except IndexError:
        return


# Preserve each screen's normal sizing while a chord occupies the title area.
_chord_widget_sizes = {}


@hook.subscribe.enter_chord
def show_chord_options(chord_name):
    for screen in qtile.screens:
        for panel in (screen.top, screen.bottom, screen.left, screen.right):
            if not isinstance(panel, bar.Bar):
                continue
            for item in panel.widgets:
                if isinstance(item, (WindowName, CurrentLayoutIcon, Chord)):
                    if item not in _chord_widget_sizes:
                        _chord_widget_sizes[item] = (item.length_type, item.length)
                    item.length_type = bar.STRETCH if isinstance(item, Chord) else bar.STATIC
                    item.length = 0
            panel.draw()


@hook.subscribe.leave_chord
def restore_window_details():
    panels = set()
    for item, (length_type, length) in _chord_widget_sizes.items():
        item.length_type = length_type
        item.length = length
        panels.add(item.bar)
    _chord_widget_sizes.clear()
    for panel in panels:
        panel.draw()
