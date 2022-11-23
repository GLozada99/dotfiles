from libqtile.config import Key, Group
from libqtile.command import lazy
from modules.keys import keys, mod
from modules.constants import KP

GROUP_NAMES = [
    {'key_name': KP['1'], 'name': 'CMD'},
    {'key_name': KP['2'], 'name': 'CHAT'},
    {'key_name': KP['3'], 'name': 'WWW1'},
    {'key_name': KP['4'], 'name': 'WWW2'},
    {'key_name': KP['5'], 'name': 'MEDIA'},
    {'key_name': KP['6'], 'name': 'WORK'},
    {'key_name': KP['7'], 'name': 'DEV'},
    {'key_name': KP['8'], 'name': 'DOCS'},
    {'key_name': KP['9'], 'name': 'EXT'},
]

groups = [Group(entry['name']) for entry in GROUP_NAMES]

for entry in GROUP_NAMES:
    keys.extend([
        Key([mod],
            entry['key_name'],
            lazy.group[entry['name']].toscreen(),
            desc="Switch to group {}".format(entry['name'])),

        Key([mod, "shift"],
            entry['key_name'],
            lazy.window.togroup(entry['name']),
            desc="Switch to & move focused window to group {}".format(entry['name'])),
    ])

# keys.extend(
#     [
#         Key([mod], "Right", lazy.screen.next_group(), desc="Switch to next group"),
#         Key([mod], "Left", lazy.screen.prev_group(), desc="Switch to previous group"),
#     ]
# )
