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
