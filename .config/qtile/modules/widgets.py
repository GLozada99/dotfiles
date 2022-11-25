import os
from libqtile import widget
from libqtile import qtile

from modules.settings.apps import Apps

colors = [
	      ["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]  # backbround for inactive screens
] 


widget_defaults = dict(
    font='Cantarell',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
class MyVolume(widget.Volume):
    def _configure(self, qtile, bar):
        widget.Volume._configure(self, qtile, bar)
        self.volume = self.get_volume()
        if self.volume <= 0:
            self.text = ''
        elif self.volume <= 15:
            self.text = ''
        elif self.volume < 50:
            self.text = ''
        else:
            self.text = ''
        # drawing here crashes Wayland

    def _update_drawer(self, wob=False):
        if self.volume <= 0:
            self.text = ''
        elif self.volume <= 15:
            self.text = ''
        elif self.volume < 50:
            self.text = ''
        else:
            self.text = ''
        self.draw()

        if wob:
            with open(self.wob, 'a') as f:
                f.write(str(self.volume) + "\n")

volume = MyVolume(
    fontsize=18,
    font='Font Awesome 5 Free',
    foreground=colors[4],
    background='#2f343f',
    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pavucontrol")}
)

def get_base_widgets():
    return [
        widget.Sep(padding=3, linewidth=0, background="#2f343f"),
        widget.Image(
            filename='~/.config/qtile/logo.png', margin=3,
            background="#2f343f", 
            mouse_callbacks={
                'Button1': lambda: qtile.cmd_spawn("rofi -show combi")
            }
        ),
        widget.Sep(padding=4, linewidth=0, background="#2f343f"), 
        widget.GroupBox(
            highlight_method='line',
            this_screen_border="#5294e2",
            this_current_screen_border="#5294e2",
            active="#ffffff",
            inactive="#848e96",
            background="#2f343f"
        ),
        widget.TextBox(
            text = '',
            padding = 0,
            fontsize = 28,
            foreground='#2f343f'
        ),
        widget.Prompt(),
        widget.Spacer(length=5),
        widget.WindowName(foreground='#99c0de',fmt='{}'),
        widget.Chord(
            name_transform=lambda name: name.upper(),
            chords_colors={'launch': ("#ff0000", "#ffffff")}
        ),
        widget.CurrentLayoutIcon(scale=0.75),
        widget.CheckUpdates(
            update_interval=1800, distro="Arch_yay",
            display_format="{updates} Updates", foreground="#ffffff",
            background="#2f343f",
            mouse_callbacks={'Button1':
                lambda: qtile.cmd_spawn(Apps.TERMINAL + ' -e yay -Syu')}
        ),
        widget.TextBox(
            text = '', padding = 0, 
            fontsize = 28, foreground='#2f343f'
        ),
        volume,
        widget.TextBox(
            text = '', padding = 0,
            fontsize = 28, foreground='#2f343f'
        ),
        widget.TextBox(
            text = '', padding = 0,
            fontsize = 28, foreground='#2f343f'
        ),
        widget.Clock(
            format=' %Y-%m-%d %a %I:%M %p',
            background="#2f343f", foreground='#9bd689'
        ),
        widget.TextBox(
            text = '', padding = 0,
            fontsize = 28, foreground='#2f343f'
        ),
        widget.TextBox(
            text='', foreground='#e39378',
            mouse_callbacks={'Button1': lambda: 
                qtile.cmd_spawn(
                    os.path.expanduser(
                        '~/.config/rofi/powermenu.sh'))}
        ),
    ]

def get_systray_widgets():
    systray_position = 11
    systray_widgets =  get_base_widgets()
    systray_widgets.insert(systray_position, widget.Systray(icon_size = 20))
    
    return systray_widgets

