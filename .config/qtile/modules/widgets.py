import os
import shutil
import subprocess

from libqtile import qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

from modules.settings.apps import Apps
from modules.settings.colors import monokai_pro as colors

widget_defaults = dict(
    font="JetBrains Mono Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


class MyVolume(widget.Volume):
    def _configure(self, qtile, bar):
        widget.Volume._configure(self, qtile, bar)
        self.volume = self.get_volume()
        if self.volume <= 0:
            self.text = "🔇"
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""
        # drawing here crashes Wayland

    def _update_drawer(self, wob=False):
        if self.volume <= 0:
            self.text = "🔇"
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""
        self.draw()

        if wob:
            with open(self.wob, "a") as f:
                f.write(str(self.volume) + "\n")


volume = MyVolume(
    fontsize=18,
    font="JetBrains Mono Nerd Font",
    foreground=colors[4],
    background=colors[0],
    mouse_callbacks={
        "Button1": lambda: qtile.spawn("pavucontrol"),
        "Button3": lambda: qtile.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
    },
)

def _get_separator(foreground: str, background: str):
    return [widget.TextBox(
        text="", padding=0, fontsize=28, foreground=foreground, background=background,
    )]

def _get_spacer(foreground: str, background: str, length: int):
    return [widget.Spacer(background=background, length=length),]

def _get_logo():
    return [
        widget.Sep(padding=4, linewidth=0, background=colors[0]),
        widget.Image(
            filename="~/.config/qtile/logo.png",
            margin=3,
            background=colors[0],
            mouse_callbacks={
                "Button1": lambda: qtile.spawn("rofi -show combi"),
            },
        ),
    ]


def _get_group():
    return [
        widget.Sep(padding=4, linewidth=0, background=colors[0]),
        widget.GroupBox(
            highlight_method="line",
            this_screen_border=colors[6],
            this_current_screen_border=colors[6],
            active=colors[6],
            inactive=colors[1],
            background=colors[0],
        ),
        widget.TextBox(
            text="", padding=0, fontsize=28, foreground=colors[0], background=colors[2]
        ),
    ]


def _get_space():
    return [
        widget.Prompt(background=colors[2]),
        widget.Spacer(background=colors[2], length=5),
        widget.WindowName(
            background=colors[2],
            foreground=colors[8],
            fmt="{}",
            max_chars=65,
        ),
        widget.Chord(
            background=colors[2],
            name_transform=lambda name: name.upper(),
            chords_colors={"launch": ("#ff0000", "#ffffff")},
        ),
        widget.CurrentLayoutIcon(background=colors[2], scale=0.75),
    ]


def _open_power_settings(command, package):
    if shutil.which(command):
        qtile.spawn(command)
    else:
        qtile.spawn([
            "notify-send", "Power settings unavailable",
            f"Install {package} to enable this settings window.",
        ])


def _microphone_status():
    try:
        result = subprocess.run(
            ["pactl", "get-source-mute", "@DEFAULT_SOURCE@"],
            capture_output=True, text=True, timeout=2, check=True,
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.SubprocessError):
        return "Mic: unavailable"
    state = result.stdout.strip().split(":", 1)[-1].strip()
    return {"yes": "Mic: muted", "no": "Mic: ready"}.get(state, "Mic: unavailable")


def _get_volume_and_battery():
    return [
        widget.TextBox(
            text="", padding=0, fontsize=28, foreground=colors[0], background=colors[2]
        ),
        widget.GenPollText(
            name="microphone",
            func=_microphone_status,
            update_interval=2,
            foreground=colors[8],
            background=colors[0],
            padding=6,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn([
                    os.path.expanduser("~/.config/qtile/scripts/media-control.sh"),
                    "mic-mute",
                ]),
                "Button3": lambda: qtile.spawn("pavucontrol --tab=4"),
            },
        ),
        widget.Battery(
            battery="BAT0",
            format="{char} {percent:2.0%} {hour:d}:{min:02d}",
            full_short_text="Battery full",
            empty_short_text="Battery empty",
            charge_char="↑",
            discharge_char="↓",
            update_interval=30,
            low_percentage=0.20,
            low_foreground=colors[5],
            foreground=colors[8],
            background=colors[0],
            padding=6,
            mouse_callbacks={
                "Button1": lambda: _open_power_settings(
                    "power-options-gtk", "power-options-gtk"
                ),
                "Button3": lambda: _open_power_settings(
                    "xfce4-power-manager-settings", "xfce4-power-manager"
                ),
            },
        ),
        widget.Backlight(
            format="☀ {percent:2.0%}",
            change_command="brightnessctl --class=backlight set {0}%",
            step=5,
            min_brightness=5,
            update_interval=2,
            foreground=colors[8],
            background=colors[0],
            padding=6,
            mouse_callbacks={
                "Button1": lambda: _open_power_settings(
                    "xfce4-power-manager-settings", "xfce4-power-manager"
                ),
            },
        ),
        widget.Sep(linewidth=0, padding=5, background=colors[0]),
    ]


def _get_metrics():
    return [
        widget.TextBox(
            text="", padding=0, fontsize=28, foreground=colors[2], background=colors[0]
        ),
        widget.ThermalSensor(
            foreground=colors[8],
            background=colors[2],
            threshold=90,
            fmt="Temp: {}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[8],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=10, background=colors[2]),
        widget.Memory(
            foreground=colors[4],
            background=colors[2],
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(Apps.TERMINAL + " -e htop"),
                "Button3": lambda: qtile.spawn(Apps.TERMINAL + " -e nvtop"),
            },
            fmt="Mem:{}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[4],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=10, background=colors[2]),
        widget.Clock(
            foreground=colors[6],
            background=colors[2],
            format="%A, %B %d - %H:%M ",
            decorations=[
                BorderDecoration(
                    colour=colors[6],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
    ]


def _get_power():
    return [
        widget.TextBox(
            text="", padding=0, fontsize=28, foreground=colors[0], background=colors[2]
        ),
        widget.TextBox(
            fontsize=20,
            padding=8,
            text="",
            foreground=colors[5],
            background=colors[0],
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    os.path.expanduser("~/.config/rofi/powermenu.sh")
                )
            },
        ),
    ]


def _get_systray():
    return [widget.Systray(icon_size=20, background=colors[0], opacity=1.0)]


def get_horizontal_widgets():
    return _get_logo() + _get_group() + _get_space() + _get_volume_and_battery() + _get_metrics() + _get_power()


def get_vertical_widgets():
    power_widgets = [
        _get_separator(colors[2], colors[0])[0],
        _get_separator(colors[0], colors[2])[0],
        _get_power()[-1]
    ]
    return _get_logo() + _get_group() + _get_space() + _get_volume_and_battery() + power_widgets

def get_principal_widgets():
    power_widgets = [
        _get_separator(colors[0], colors[2])[0],
        _get_power()[-1]
    ]
    return (_get_logo() + _get_group() + _get_space() + _get_volume_and_battery() + [
        widget.Systray(icon_size=20, background=colors[0], opacity=1.0)] +
            _get_metrics() +
            power_widgets)
