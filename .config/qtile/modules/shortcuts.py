"""Searchable help built from the running Qtile configuration."""
import subprocess
from functools import partial

from libqtile.config import KeyChord


MODIFIERS = {"mod4": "Super", "mod1": "Alt", "control": "Ctrl", "shift": "Shift"}


def shortcut_rows(bindings, prefix=""):
    rows = []
    for binding in bindings:
        key = "+".join([MODIFIERS.get(mod, mod) for mod in binding.modifiers] + [str(binding.key)])
        sequence = f"{prefix} → {key}" if prefix else key
        if isinstance(binding, KeyChord):
            rows.append(f"{sequence}    —    {binding.desc or 'Enter chord'}")
            rows.extend(shortcut_rows(binding.submappings, sequence))
        else:
            description = binding.desc or ", ".join(command.name for command in binding.commands)
            if not description and binding.key == "Escape":
                description = "Cancel chord"
            rows.append(f"{sequence}    —    {description or 'Unassigned'}")
    return rows


def show_shortcuts(qtile):
    rows = shortcut_rows(qtile.config.keys)
    # Rofi waits in a worker thread, leaving Qtile responsive. Selecting a row
    # only dismisses this help menu; it never executes the listed action.
    qtile.run_in_executor(partial(
        subprocess.run,
        ["rofi", "-dmenu", "-i", "-p", "Qtile shortcuts", "-no-custom",
         "-mesg", "Type to search · Esc to close", "-lines", "18"],
        input="\n".join(rows), text=True, stdout=subprocess.DEVNULL, check=False,
    ))
