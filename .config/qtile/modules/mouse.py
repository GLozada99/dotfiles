from libqtile.config import Click, Drag
from libqtile.lazy import lazy
from modules.settings.keys import Keys

# Drag floating layouts.
mouse = [
    Drag([Keys.MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([Keys.MOD], "Button3", lazy.window.toggle_floating()),
    Click([Keys.MOD], "Button2", lazy.window.toggle_fullscrean())
]
