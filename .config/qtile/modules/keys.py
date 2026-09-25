import os

from libqtile.lazy import lazy
from libqtile.config import Key, KeyChord

from modules.settings.apps import Apps
from modules.settings.keys import Keys

focus = [
    Key([Keys.ALT], "Left", lazy.layout.left(), desc="Move Focus Left"),
    Key([Keys.ALT], "Right", lazy.layout.right(), desc="Move Focus Right"),
    Key([Keys.ALT], "Down", lazy.layout.down(), desc="Move Focus Down"),
    Key([Keys.ALT], "Up", lazy.layout.up(), desc="Move Focus Up"),
]

move = [
    Key([Keys.MOD], "Left", lazy.layout.shuffle_left(), desc="Move Window Left"),
    Key([Keys.MOD], "Right", lazy.layout.shuffle_right(), desc="Move Window Right"),
    Key([Keys.MOD], "Down", lazy.layout.shuffle_down(), desc="Move Window Down"),
    Key([Keys.MOD], "Up", lazy.layout.shuffle_up(), desc="Move Window Up"),
]

grow = [
    Key([Keys.MOD, Keys.ALT], "Left", lazy.layout.grow_left(), desc="Grow Left"),
    Key([Keys.MOD, Keys.ALT], "Right", lazy.layout.grow_right(), desc="Grow Right"),
    Key([Keys.MOD, Keys.ALT], "Down", lazy.layout.grow_down(), desc="Grow Down"),
    Key([Keys.MOD, Keys.ALT], "Up", lazy.layout.grow_up(), desc="Grow Up"),
]

media_control = os.path.expanduser("~/.config/qtile/scripts/media-control.sh")

power_action = os.path.expanduser("~/.config/qtile/scripts/power-action.sh")

spawn = [
    Key([Keys.MOD, "control"], "d",
        lazy.spawn([os.path.expanduser("~/.config/qtile/screen.sh"), "--toggle"]),
        desc="Toggle laptop-only / regular monitor layout"),
    KeyChord(
        [Keys.MOD], "m",
        [
            Key([], "l", lazy.spawn([power_action, "lock"]), desc="Lock"),
            Key([], "o", lazy.spawn([power_action, "logout"]), desc="Log out"),
            Key([], "s", lazy.spawn([power_action, "sleep"]), desc="Sleep"),
            Key([], "h", lazy.spawn([power_action, "hibernate"]), desc="Hibernate"),
        ],
        mode=False,
        name="Power: [l] lock · [o] logout · [s] sleep · [h] hibernate",
        desc="Power actions",
    ),
    Key([Keys.MOD], "Return", lazy.spawn(Apps.TERMINAL), desc="Launch Terminal"),
    Key([Keys.MOD], "b", lazy.spawn(Apps.BROWSERS[0]), desc="Launch Browser 1"),
    Key([Keys.MOD], "n", lazy.spawn(Apps.FILE_EXPLORER), desc="Launch Nemo"),
    Key([Keys.MOD], "c", lazy.spawn(Apps.BROWSERS[1]), desc="Launch Browser 2"),
    Key([Keys.MOD], "z", lazy.spawn(Apps.BROWSERS[2]), desc="Launch Browser 3"),
    Key(
        [Keys.MOD], "x", lazy.spawn(Apps.AUDIO_CONTROL), desc="Launch Audio Controller"
    ),
    Key([Keys.MOD], "t", lazy.spawn(Apps.TELEGRAM), desc="Launch Telegram"),
    Key([Keys.MOD], "p", lazy.spawn(Apps.TODO), desc="Launch ToDo app"),
    Key([Keys.MOD], "w", lazy.spawn(Apps.WHATSAPP), desc="Launch Whatsapp"),
    # Key([Keys.MOD], "d", lazy.spawn(Apps.DOCUMENT), desc="Launch Libreoffice"),
    # Key([Keys.MOD], "d", lazy.spawn(Apps.CODE_EDITOR), desc="Launch Libreoffice"),
]

keys = (
    [
        Key(
            [Keys.ALT],
            "Tab",
            lazy.layout.next(),
            desc="Move window focus to next window",
        ),
        Key(
            [Keys.ALT, "shift"],
            "Tab",
            lazy.layout.up(),
            desc="Move window focus to previous window",
        ),
        Key([Keys.MOD], "r", lazy.spawn("rofi -show combi"), desc="spawn rofi"),
        Key([Keys.MOD], "q", lazy.window.kill(), desc="Kill focused window"),
        Key([Keys.MOD, "control"], "r", lazy.restart(), desc="Restart Qtile"),
        Key([Keys.MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
        Key([Keys.MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        Key([Keys.MOD, "shift"], "space", lazy.layout.flip()),
        Key(
            [Keys.MOD, "shift"],
            "r",
            lazy.spawncmd(),
            desc="Spawn a command using a prompt widget",
        ),
        Key([], Keys.VOL_UP, lazy.spawn([media_control, "volume-up"])),
        Key([], Keys.VOL_DOWN, lazy.spawn([media_control, "volume-down"])),
        Key(
            [],
            Keys.TOGGLE_MUTE,
            lazy.spawn([media_control, "mute"]),
        ),
        # External keyboard Fn+F1/F2 emit Launch5/Launch6 (verified with xev).
        Key([], "XF86Launch5", lazy.spawn([media_control, "brightness-down"])),
        Key([], "XF86Launch6", lazy.spawn([media_control, "brightness-up"])),
        Key([], "XF86MonBrightnessUp", lazy.spawn([media_control, "brightness-up"])),
        Key([], "XF86MonBrightnessDown", lazy.spawn([media_control, "brightness-down"])),
        Key([], Keys.NEXT, lazy.spawn("playerctl next")),
        Key([], Keys.PREV, lazy.spawn("playerctl previous")),
        Key([], Keys.TOGGLE_PLAY, lazy.spawn("playerctl play-pause")),
        Key([Keys.MOD], "Print", lazy.spawn(Apps.SCREENSHOT), desc="Take screenshot"),
        Key([Keys.MOD], "Home", lazy.spawn(Apps.SCREENSHOT), desc="Take screenshot"),
        Key([Keys.ALT], "period", lazy.next_screen(), desc="Cycle monitor focus"),
    ]
    + focus
    + move
    + grow
    + spawn
)
