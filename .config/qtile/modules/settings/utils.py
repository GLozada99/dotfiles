from subprocess import PIPE, Popen
from typing import Iterable


def run_command(command: str) -> Iterable[str]:
        process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        return map(lambda entry: entry.decode('utf-8'), stdout.splitlines())

def get_monitor_number() -> int:
    # Connected-but-disabled outputs must not get Qtile screens.
    result = run_command("xrandr --listactivemonitors")
    first_line = next(iter(result), "Monitors: 1")
    try:
        return max(1, int(first_line.split(":", 1)[1]))
    except (ValueError, IndexError):
        return 1
