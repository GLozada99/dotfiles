from libqtile import hook
import subprocess
import os

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([script])

@hook.subscribe.startup
def screen():
    script = os.path.expanduser('~/.config/qtile/screen.sh')
    subprocess.call([script])
