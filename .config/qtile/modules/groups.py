from libqtile.config import Key, Group
from libqtile.command import lazy
from modules.keys import keys
from modules.constants import GROUP_NAMES
from modules.settings.keys import Keys


groups = [Group(entry['name']) for entry in GROUP_NAMES]

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

# keys.extend(
#     [
#         Key([Keys.ALT], "Right", lazy.screen.next_group(), desc="Switch to next group"),
#         Key([Keys.ALT], "Left", lazy.screen.prev_group(), desc="Switch to previous group"),
#     ]
# )
