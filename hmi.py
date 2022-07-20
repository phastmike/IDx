"""
HMI - Human Machine Interface class
      Output information leds
      Power led is not controllable
"""

import utime
from machine import Pin

class HMI:

    def __init__(self):

        self.led_ctcss = Pin(17, Pin.OUT, None, value=0)
        self.led_id = Pin(18, Pin.OUT, None, value=0)
