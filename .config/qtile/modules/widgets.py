import os

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
        "Button1": lambda: qtile.cmd_spawn("pavucontrol"),
        "Button3": lambda: qtile.cmd_spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
    },
)


def get_base_widgets():
    return [
        widget.Sep(padding=3, linewidth=0, background=colors[0]),
        widget.Image(
            filename="~/.config/qtile/logo.png",
            margin=3,
            background=colors[0],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("rofi -show combi")},
        ),
        widget.Sep(padding=4, linewidth=0, background=colors[0]),
        widget.GroupBox(
            highlight_method="line",
            this_screen_border=colors[6],
            this_current_screen_border=colors[6],
            active=colors[6],
            inactive=colors[1],
            background=colors[0],
        ),
        widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        widget.Prompt(),
        widget.Spacer(length=5),
        widget.WindowName(foreground=colors[8], fmt="{}"),
        widget.Chord(
            name_transform=lambda name: name.upper(),
            chords_colors={"launch": ("#ff0000", "#ffffff")},
        ),
        widget.CurrentLayoutIcon(scale=0.75),
        widget.CheckUpdates(
            update_interval=1800,
            distro="Arch_yay",
            display_format="{updates} Updates",
            foreground=colors[1],
            background=colors[0],
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(Apps.TERMINAL + " -e yay -Syu")
            },
        ),
        # widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        # widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        # Systray for principal window,
        widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        MyVolume(
            fontsize=18,
            font="JetBrains Mono Nerd Font",
            foreground=colors[4],
            background=colors[0],
            decorations=[
                BorderDecoration(
                    colour=colors[4],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn("pavucontrol"),
                "Button3": lambda: qtile.cmd_spawn(
                    "pactl set-sink-mute @DEFAULT_SINK@ toggle"
                ),
            },
        ),
        widget.ThermalSensor(
            foreground=colors[8],
            background=colors[0],
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
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Memory(
            foreground=colors[4],
            background=colors[0],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(Apps.TERMINAL)},
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
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.KeyboardLayout(
            foreground=colors[8],
            background=colors[0],
            fmt="Keyboard: {}",
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
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Clock(
            foreground=colors[6],
            background=colors[0],
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
        widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
        widget.TextBox(
            text="",
            foreground=colors[5],
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    os.path.expanduser("~/.config/rofi/powermenu.sh")
                )
            },
        ),
    ]


def get_systray_widgets():
    systray_position = 11
    systray_widgets = get_base_widgets()

    del systray_widgets[systray_position]
    # del systray_widgets[systray_position]

    systray_widgets.insert(systray_position, widget.Systray(icon_size=20))
    systray_widgets.insert(
        systray_position,
        widget.TextBox(text="", padding=0, fontsize=28, foreground=colors[0]),
    )

    return systray_widgets
