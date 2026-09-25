# Laptop power controls

The Qtile bar shows BAT0's charge, charging/discharging direction and estimated
remaining time. Time estimates depend on the battery's reported discharge rate;
a zero estimate while plugged in or idle does not mean the battery is empty.
The battery text changes colour below 20%.

- Left-click the battery: Power Options GTK settings.
- Right-click the battery: Xfce power settings (display, idle, lid and battery actions).
- Scroll over the brightness percentage: adjust the laptop backlight by 5%, with
  a 5% minimum. Left-click it to open Xfce power settings.
- Power Options' tray applet starts at login for profile selection.
- Xfce Power Manager starts at login when installed, including its brightness-key
  handling and low-battery notifications. Qtile does not duplicate those bindings
  or notifications.

## Dependencies and activation

`brightnessctl` and `power-options-tray` are already installed on this machine.
Install the missing graphical utilities:

```sh
sudo pacman -S xfce4-power-manager
yay -S power-options-gtk
```

Review the AUR package build instructions as usual. Missing GUI programs produce
a notification when clicked; missing optional autostart programs are skipped.

Restart Qtile with Super+Ctrl+R to load the widgets. The `startup_once` hook only
runs on login, so log out and back in to start the applets, or launch
`power-options-tray` and `xfce4-power-manager` once from the application launcher.
Do not rerun the entire autostart script just to start these two programs.

## Power-policy ownership

These dotfiles do not change system services or graphics modes. TLP and Power
Options were both enabled when inspected; system76-power was also installed.
Before relying on automatic profiles, choose one owner for overlapping CPU/device
power settings. The intended setup uses Power Options for those settings and
Xfce for screen dimming, idle, lid and critical-battery actions. Avoid configuring
competing brightness/idle policies in Power Options, or profile switching in
Xfce. Check existing logind lid handling as part of that setup.

System76 graphics switching needs separate review before disabling any related
service. The existing system-wide `nvidia-fix` service also needs review: it
requests persistence mode and polls the GPU every five seconds. Neither service
is changed by this Qtile update, and battery-runtime improvements are not yet
measured.

## Locking and lid suspend

Install `i3lock` and `xss-lock`, then run:

```sh
~/.config/qtile/scripts/session-power.sh
```

This is also run at login. It starts `xss-lock --transfer-sleep-lock` with i3lock
and delegates lid handling to systemd-logind. The current system has
`HandleLidSwitchDocked=suspend` in `/etc/systemd/logind.conf`, so lid-close
suspends even with an external display. The default AC/battery action is suspend.
Xfce 4.20 skips lid-close with external monitors; its old `lid-docked-active-*`
settings are unsupported in this version. Xfce's separate screen-lock request is disabled
because xss-lock handles the logind sleep event and delays sleep until locked.
If the locker dependencies are missing, the script leaves lid settings unchanged.

Super+M enters the native Qtile power chord. Release Super, then press L to
lock, O to log out of the current session, S to suspend, or H to hibernate.
The chord exits after one action; Escape cancels. The bar shows the available
keys while the chord is active. No Rofi window is opened by this shortcut.
The bar power button still opens Rofi, including Restart and Shutdown without
letter shortcuts. Lock/sleep/hibernate report missing locker setup rather than
proceeding unlocked. Manual locking uses the same xss-lock listener as sleep.

After updating the keybinding, restart Qtile with Super+Ctrl+R. Starting the
listener and changing lid policy does not require restarting Qtile or logging out.
A real lock/unlock and lid-close/resume cycle still needs to be checked manually.

## Volume and brightness indicators

Qtile's volume, mute and brightness keys use `scripts/media-control.sh` to show
centered GTK overlays with symbolic icons and a percentage/progress bar. Repeated adjustments
replace the previous notification. Volume and brightness change in 5% steps;
muting shows an explicit muted state. Volume amplification above 100% is retained,
with the visual progress bar capped at 100%. Notifications expire after 1.5 seconds.

Qtile owns the brightness keys; autostart disables Xfce's duplicate key handler
and brightness popup. Xfce still manages idle display policy. Restart Qtile with
Super+Ctrl+R after changing the keybindings. The indicators use the installed GTK 3/PyGObject/Cairo stack, `pactl`,
`brightnessctl` and `flock`. Ordinary Dunst notifications are unchanged.

Brightness uses the dedicated XF86MonBrightnessDown/Up key events (Fn plus
the brightness keys in the current keyboard mode). Plain F1/F2 remain available
to applications. These controls adjust the laptop panel, not external monitors.

The observed Fn+F1/F2 events are XF86Launch5 and XF86Launch6; these are
also bound to brightness down/up. Standard laptop brightness keys remain bound.


## Monitor toggle

Super+Ctrl+D toggles laptop-only and regular monitor mode. Laptop-only disables
all external outputs without unplugging cables. Regular mode restores HDMI-1
above eDP-1 and HDMI-2 rotated left to its right when both monitors are connected.
Qtile reloads its screen configuration automatically; groups remain available
through the normal workspace bindings. The chosen mode survives Qtile restarts
within the login session. External outputs must report connected to be restored.
Keep the laptop lid open when using laptop-only mode.

## Microphone indicator

The bar shows `Mic: ready` (unmuted), `Mic: muted`, or `Mic: unavailable` for
the default audio source, refreshed every two seconds. Ready does not mean an
application is recording. Click to toggle mute; right-click opens input-device
settings. Super+Shift+M and the dedicated microphone-mute key do the same.
The toggle shows a centered microphone icon with a muted/unmuted label. Applications explicitly using a
different input device are not affected by muting the default microphone.


The media overlay is centered on X11's primary monitor (currently eDP-1),
rechecking the primary monitor on each update. It never takes keyboard focus,
accepts no mouse input, and hides after 1.5 seconds. A single GTK application
instance handles repeated updates. Its diagnostic log is in
`$XDG_RUNTIME_DIR/qtile-media-osd.log`.


## Floating terminal

Super+Enter toggles a reusable Alacritty scratchpad on the current screen.
It occupies 80% of the screen width and 65% of its height and hides on focus loss.
Plain Escape is passed through to the terminal; use Super+Enter to hide it.
Super+Q is ignored in the floating terminal to prevent accidental closure.
Super+Escape deliberately closes it and ends its shell (a tmux session, if used,
continues running).
Hiding keeps its shell and processes running. Ctrl+Super+Enter launches a regular
terminal. Closing the scratchpad window ends its shell; the next toggle creates
another. Tmux is optional: run `tmux new-session -A -s scratchpad` inside it to
retain a named session even if the window closes (not across reboot).
