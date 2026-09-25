#!/usr/bin/python
"""Single-instance, non-focusable X11 media overlay using the installed GTK stack."""
import sys

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gio, GLib, Gtk


class MediaOSD(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="local.qtile.MediaOSD",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.timeout = 0

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.hold()
        # POPUP is override-redirect on X11: Qtile does not tile or focus it.
        self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.window.set_name("media-osd")
        self.window.set_title("Qtile Media OSD")
        self.window.set_accept_focus(False)
        self.window.set_focus_on_map(False)
        self.window.set_keep_above(True)
        self.window.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)
        self.window.set_default_size(220, 210)
        self.window.set_app_paintable(True)
        visual = self.window.get_screen().get_rgba_visual()
        if visual:
            self.window.set_visual(visual)
        self.window.connect("draw", self.clear_background)
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        panel.set_name("osd-panel")
        self.image = Gtk.Image()
        self.image.set_pixel_size(72)
        self.label = Gtk.Label()
        self.progress = Gtk.ProgressBar()
        panel.pack_start(self.image, True, True, 0)
        panel.pack_start(self.label, False, False, 0)
        panel.pack_start(self.progress, False, False, 0)
        self.window.add(panel)
        css = Gtk.CssProvider()
        css.load_from_data(b"""
            #media-osd { background-color: transparent; }
            #osd-panel { background-color: rgba(48,48,52,0.94); color: #f8f8f2;
                         border-radius: 18px; padding: 24px; }
            #osd-panel label { font: bold 14px Sans; }
            #osd-panel image { color: #f8f8f2; }
            #osd-panel progressbar trough { min-height: 7px; border: none;
                border-radius: 4px; background-color: #555866; }
            #osd-panel progressbar progress { min-height: 7px; border: none;
                border-radius: 4px; background-color: #8be9fd; }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            self.window.get_screen(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def clear_background(self, window, context):
        import cairo
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.set_source_rgba(0, 0, 0, 0)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)
        return False

    def do_command_line(self, command_line):
        args = command_line.get_arguments()[1:]
        if len(args) != 3:
            return 2
        icon, label, raw_value = args
        try:
            value = int(raw_value)
        except ValueError:
            return 2
        self.image.set_from_icon_name(icon, Gtk.IconSize.DIALOG)
        self.image.set_pixel_size(72)
        self.label.set_text(label)
        self.progress.set_fraction(max(0, min(value, 100)) / 100)
        self.window.show_all()
        self.progress.set_visible(value >= 0)
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() or display.get_monitor(0)
        if monitor:
            rect = monitor.get_geometry()
            minimum, natural = self.window.get_preferred_size()
            width, height = max(220, natural.width), max(210, natural.height)
            self.window.resize(width, height)
            self.window.move(rect.x + (rect.width - width) // 2,
                             rect.y + (rect.height - height) // 2)
        # Let clicks pass through rather than blocking the application underneath.
        import cairo
        self.window.get_window().input_shape_combine_region(cairo.Region(), 0, 0)
        if self.timeout:
            GLib.source_remove(self.timeout)
        self.timeout = GLib.timeout_add(1500, self.hide)
        return 0

    def hide(self):
        self.window.hide()
        self.timeout = 0
        return False


if __name__ == "__main__":
    raise SystemExit(MediaOSD().run(sys.argv))
