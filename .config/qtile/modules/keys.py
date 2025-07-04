from libqtile.lazy import lazy
from libqtile.config import Key

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

spawn = [
    Key([Keys.MOD], "Return", lazy.spawn(Apps.TERMINAL), desc="Launch Terminal"),
    Key([Keys.MOD], "b", lazy.spawn(Apps.BROWSERS[0]), desc="Launch Browser 1"),
    Key([Keys.MOD], "n", lazy.spawn(Apps.FILE_EXPLORER), desc="Launch Nemo"),
    Key([Keys.MOD], "c", lazy.spawn(Apps.BROWSERS[1]), desc="Launch Browser 2"),
    Key([Keys.MOD], "z", lazy.spawn(Apps.BROWSERS[2]), desc="Launch Browser 3"),
    Key(
        [Keys.MOD], "x", lazy.spawn(Apps.AUDIO_CONTROL), desc="Launch Audio Controller"
    ),
    Key([Keys.MOD], "t", lazy.spawn(Apps.TELEGRAM), desc="Launch Telegram"),
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
        Key([], Keys.VOL_UP, lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%")),
        Key([], Keys.VOL_DOWN, lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),
        Key(
            [],
            Keys.TOGGLE_MUTE,
            lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        ),
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
