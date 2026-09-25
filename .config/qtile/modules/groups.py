from libqtile.config import Key, Group, ScratchPad, DropDown, Match
from libqtile.lazy import lazy

from modules.keys import keys
from modules.constants import GROUP_NAMES
from modules.settings.keys import Keys
from modules.settings.apps import Apps


groups = [
    Group(entry['name'])
    for entry in GROUP_NAMES
]

for entry in GROUP_NAMES:
    keys.extend([
        Key([Keys.ALT],
            entry['key_name'],
            lazy.group[entry['name']].toscreen(),
            desc="Switch to group {}".format(entry['name'])),

        Key([Keys.ALT, "shift"],
            entry['key_name'],
            lazy.window.togroup(entry['name']),
            desc="Switch to & move focused window to group {}".format(entry['name'])),
    ])

keys.extend(
    [
        Key([Keys.ALT], "slash", lazy.screen.next_group(), desc="Switch to next group"),
        Key([Keys.ALT], "comma", lazy.screen.prev_group(), desc="Switch to previous group"),
    ]
)


# This window is hidden, not closed, when the dropdown is dismissed.
groups.append(ScratchPad("scratchpad", [
    DropDown(
        "terminal",
        Apps.TERMINAL + " --class qtile-scratchpad --title Scratchpad",
        match=Match(wm_class="qtile-scratchpad"),
        x=0.1, y=0.1, width=0.8, height=0.65,
        opacity=1.0,
        on_focus_lost_hide=True,
        warp_pointer=False,
    ),
]))
