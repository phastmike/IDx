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

    def __init__(self, remote = 0, ptt = 1, ctcss = 2, ext1 = 3, ext3 = 4):
        self.pin_remote = Pin(remote, Pin.OUT, value=1)
        self.pin_ptt = Pin(ptt, Pin.OUT, value=1)
        self.pin_ctcss_rx = Pin(ctcss, Pin.IN, Pin.PULL_UP)
        self.pin_ext1 = Pin(ext1, Pin.OUT, value=0)
        self.pin_ext3 = Pin(ext3, Pin.OUT, value=1)

    def on_tx_start_connect(self, cb):
        self.__on_tx_start = cb

    def on_tx_start_disconnect(self):
        self.__on_tx_start = None

    def on_tx_stop_connect(self, cb):
        self.__on_tx_stop = cb

    def on_tx_stop_disconnect(self):
        self.__on_tx_stop = None

    def ctcss_detected(self):
        #return False
        return not self.pin_ctcss_rx.value()

    #delete
    def ctcss_get_hw_pin(self):
        return self.pin_ctcss_rx

    def tx_start(self): 
        #print("[DR1X] ::  TX  >>>")
        if self.__on_tx_start != None:
            self.__on_tx_start()
        self.pin_remote.low()
        utime.sleep(0.25)
        self.pin_ptt.low()

    def tx_stop(self): 
        #print("[DR1X] ::  RX <<<")
        self.pin_ptt.high()
        utime.sleep(0.25)
        self.pin_remote.high()
        if self.__on_tx_stop != None:
            self.__on_tx_stop()

    def set_irq_routine (self, routine):
        self.pin_ctcss_rx.irq(routine, Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)

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

