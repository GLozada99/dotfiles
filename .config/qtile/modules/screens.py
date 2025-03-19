from libqtile import bar

from modules.settings.utils import get_monitor_number
from .widgets import *
from libqtile.config import Screen
import os
import enum

class ScreenType(enum.Enum):
    NORMAL = 0
    PRINCIPAL = 1
    VERTICAL = 2


def generate_screen(screen_type: ScreenType):
    match screen_type:
        case ScreenType.PRINCIPAL:
            return Screen(
                top=bar.Bar(
                    get_principal_widgets(),
                    30,
                    margin=[8, 0, 0, 0],
                    opacity=0.9,
                    background="#404552"
                    )
                )
        case ScreenType.VERTICAL:
            return Screen(
                top=bar.Bar(
                    get_vertical_widgets(),
                    30,
                    margin=[8, 0, 0, 0],
                    opacity=0.9,
                    background="#404552"
                )
            )
        case _:
            return Screen(
                top=bar.Bar(
                    get_horizontal_widgets(),
                    30,
                    margin=[8, 0, 0, 0],
                    opacity=0.9,
                    background="#404552"
                )
            )

def generate_screens():
    match get_monitor_number():
        case 1:
            return [generate_screen(ScreenType.PRINCIPAL)]
        case 2:
            return [generate_screen(ScreenType.NORMAL), generate_screen(
                ScreenType.PRINCIPAL)]
        case 3:
            return [generate_screen(ScreenType.NORMAL), generate_screen(
                ScreenType.PRINCIPAL), generate_screen(ScreenType.VERTICAL),]
    # screens = []
    # extra_monitors = get_monitor_number() - 1
    # if extra_monitors > 0:
    #     screens.extend([generate_screen() for _ in range(extra_monitors)])
    #
    # position = min(principal_position, len(screens))
    # screens.insert(position, generate_screen(principal=True))
    # return screens

screens = generate_screens()
