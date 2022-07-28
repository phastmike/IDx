"""
DR1X- class representing the repeater

      This class should be a singleton
      as only one instance should exist
      due to hhrdware dependency
"""

import utime
from machine import Pin

class DR1x:

    __on_tx_start = None
    __on_tx_stop  = None

    def __init__(self):
        self.pin_remote = Pin(0, Pin.OUT, Pin.PULL_UP, value=1)
        self.pin_ptt = Pin(1, Pin.OUT, Pin.PULL_UP, value=1)
        self.pin_ctcss_rx = Pin(2, Pin.IN, Pin.PULL_UP)
        self.pin_ext1 = Pin(3, Pin.OUT, Pin.PULL_UP, value=0)
        self.pin_ext3 = Pin(4, Pin.OUT, Pin.PULL_UP, value=1)

    def on_tx_start_connect(self, cb):
        self.__on_tx_start = cb

    def on_tx_start_disconnect(self):
        self.__on_tx_start = None

    def on_tx_stop_connect(self, cb):
        self.__on_tx_stop = cb

    def on_tx_stop_disconnect(self):
        self.__on_tx_stop = None

    def ctcss_detected(self):
        return self.pin_ctcss_rx.value()

    def ctcss_get_hw_pin(self):
        return self.pin_ctcss_rx

    def tx_start(self): 
        print("[DR1X] :: Will START TX now ...")
        if self.__on_tx_start != None:
            self.__on_tx_start()
        self.pin_remote.low()
        utime.sleep(0.25)
        self.pin_ptt.low()

    def tx_stop(self): 
        print("[DR1X] :: Will STOP TX now ...")
        self.pin_ptt.high()
        utime.sleep(0.25)
        self.pin_remote.high()
        if self.__on_tx_stop != None:
            self.__on_tx_stop()

"""
Test module
"""

if __name__ == "__main__":  

    print("Start DR1x tests")
    pin_led_id = Pin(18, Pin.OUT, None)
    
    def turn_led_on():
        pin_led_id.high()
        print("TX Start")
    
    def turn_led_off():
        pin_led_id.low()
        print("TX Stop")

    dr1x = DR1x()
    dr1x.on_tx_start_connect(turn_led_on)
    dr1x.on_tx_stop_connect(turn_led_off)

    while(True):
        dr1x.tx_start()
        utime.sleep(5)
        dr1x.tx_stop()
        utime.sleep(5)

