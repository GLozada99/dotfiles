from libqtile import bar

from modules.settings.utils import get_monitor_number
from .widgets import *
from libqtile.config import Screen
import os

def generate_screen(principal: bool = False):
    return Screen(
        top=bar.Bar(
            base_widgets if not principal else systray_widgets, 30,
            margin=[8, 0, 0, 0],
            opacity=0.9,
            background="#404552"
            )
        )

def generate_screens(principal_position: int = 0):
    screens = []
    extra_monitors = get_monitor_number() - 1
    if extra_monitors > 0:
        screens.extend([generate_screen() for _ in range(extra_monitors)])

    position = min(principal_position, len(screens))
    screens.insert(position, generate_screen(principal=True))
    return screens

screens = generate_screens(1)