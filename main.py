from typing import Any
import betterinput as bti

class T:
    def __init__(self, val: Any):
        self.val = val

device = bti.InputDevice(True, True, 5)

print(f"Streamsize      : {device.streamsize}")
print(f"Show warnings   : {device.warnings}")
print(f"Raise exceptions: {device.raise_exceptions}")
print(f"Device kit      : {device.kit}")

x = device.get_multiple_input([int, [str, int, float], [int], int, str, float], separator=" ")
