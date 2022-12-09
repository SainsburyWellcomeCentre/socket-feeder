"""Socket feeder device  - feeder module.

Controls the position of the feeder shutter plate.
"""

from machine import Pin
import re
import piostep

clienthelp = """
Hello, you are connected to a socket feeder. I support the following commands:

Hn - Home step by n steps.
Mn - Move to position n, where n = [0, 29].
"""
npos = 2 * 15
nsteps = int((50 * 360) / (1 * 7.5))
steps_per_pos = int(nsteps / npos)
motor = piostep.Stepper(Pin(18), 100)
regex = re.compile(b'-?\d+')
position = 0


def process(command):
    global position
    try:
        parameter = int(regex.search(bytes(command)).group(0))
        if command[0:1] == b'H':
            print(f'INFO: Homing by {parameter} steps')
            motor.move(parameter)
            position = 0
        elif command[0:1] == b'M':
            delta = steps_per_pos * (parameter - position) % nsteps
            if delta > nsteps / 2:
                delta -= nsteps
            print(f'INFO: Moving to position {parameter} in {delta} steps')
            motor.move(delta)
            position = parameter
        else:
            print(f'WARN: Unknown command {command}')
    except:
        print(f'ERROR: Could not parse message {command}')
