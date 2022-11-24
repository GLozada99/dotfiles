from subprocess import PIPE, Popen
from typing import Iterable


def run_command(command: str) -> Iterable[str]:
        process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        return map(lambda entry: entry.decode('utf-8'), stdout.splitlines())

def get_monitor_number() -> int:
    command = 'xrandr | grep " connected " | awk \'{ print$1 }\''
    result = run_command(command)
    return len(list(result))