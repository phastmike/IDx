"""
HMI - Human Machine Interface class
      Output information leds
      Power led is not controllable
"""

import rp2
import utime
from machine import Pin

class HMI:

    def __init__(self, led_ctcss = 17, led_id = 18):
        self.led_ctcss = Pin(led_ctcss, Pin.OUT, None, value=0)
        self.led_id = Pin(led_id, Pin.OUT, None, value=0)
        # Instantiate a state machine with the blink program, at 2000Hz, with set bound to Pin(25) (LED on the rp2 board)
        # Run the state machine, the internal LED should blink.
        self.__sm = rp2.StateMachine(0, self.blink, freq=2000, set_base=Pin(25))

    def led_id_turn_on(self):
        self.led_id.high()
        print("[HMI ] :: Led ID is on")

    def led_id_turn_off(self):
        self.led_id.low()
        print("[HMI ] :: Led ID is off")

    def led_pico_blink_enable(self):
        self.__sm.active(1)
        print("[HMI ] :: Led Pico started blinking")

    def led_pico_blink_disable(self):
        self.__sm.active(0)
        print("[HMI ] :: Led Pico stopped blinking")

    # Define the blink program.  It has one GPIO to bind to on the set instruction, which is an output pin.
    # Use lots of delays to make the blinking visible by eye.
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def blink():
        wrap_target()
        set(pins, 1)   [31]
        nop()          [31]
        nop()          [31]
        nop()          [31]
        nop()          [31]
        set(pins, 0)   [31]
        nop()          [31]
        nop()          [31]
        nop()          [31]
        nop()          [31]
        wrap()

