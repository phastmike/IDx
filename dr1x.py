"""
DR1X class representing the repeater
"""

import utime
from machine import Pin

class DR1x:

    __on_tx_start = None
    __on_tx_stop  = None
    __on_check_usage_start = None
    __on_check_usage_stop = None
    __in_check_usage = False 

    def __init__(self):
        # init io pins
        self.pin_remote = Pin(0, Pin.OUT, Pin.PULL_UP, value=1)
        self.pin_ptt = Pin(1, Pin.OUT, Pin.PULL_UP, value=1)
        self.pin_ctcss_rx = Pin(2, Pin.IN, Pin.PULL_UP)
        self.pin_ext1 = Pin(3, Pin.OUT, Pin.PULL_UP, value=0)
        self.pin_ext3 = Pin(4, Pin.OUT, Pin.PULL_UP, value=1)
        #pin_led_ctcss = Pin(17, Pin.OUT, None, value=0)
        #pin_led_id = Pin(18, Pin.OUT, None, value=0)

    def on_tx_start_connect(self, cb):
        self.__on_tx_start = cb

    def on_tx_start_disconnect(self):
        self.__on_tx_start = None

    def on_tx_stop_connect(self, cb):
        self.__on_tx_stop = cb

    def on_tx_stop_disconnect(self):
        self.__on_tx_stop = None

    def on_check_usage_start_connect(self, cb):
        self.__on_check_usage_start = cb

    def on_check_usage_start_disconnect(self):
        self.__on_check_usage_start = None 

    def on_check_usage_stop_connect(self, cb):
        self.__on_check_usage_stop = cb

    def on_check_usage_stop_disconnect(self):
        self.__on_check_usage_stop = None 

    def tx_start(self): 
        if self.__on_tx_start != None:
            self.__on_tx_start()
        self.pin_remote.low()
        utime.sleep(0.25)
        self.pin_ptt.low()

    def tx_stop(self): 
        self.pin_ptt.high()
        utime.sleep(0.25)
        self.pin_remote.high()
        if self.__on_tx_stop != None:
            self.__on_tx_stop()

    def check_repeater_in_use(self, seconds=10):
        count = 0
        __in_check_usage = True 
        if self.__on_check_usage_start != None:
            self.__on_check_usage_start()

        print("[Info] :: Checking if repeater is free to ID...")

        while True:
            count = count + 1
            if self.pin_ctcss_rx.value() == 0:
                count = 0
                print("[Warn] :: CTCSS detected, busy? => Reset counter")

            utime.sleep_ms(50)

            #self.pin_led_id.value(not self.pin_led_id.value())

            if count % 20 == 0:
                print ("[Time] :: Elapsed %d/10 sec." % ((int) (count / 20)))
            if count >= 200:
                print ("[Info] :: Will ID Repeater now ...")
                if self.__on_check_usage_stop != None:
                    self.__on_check_usage_stop()
                __in_check_usage = False 
                break

if __name__ == "__main__":  

    import uasyncio as asyncio

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

    async def id_blink():
        while __in_check_usage: 
            pin_led_id.high()
            await asyncio.sleep(0.05)
            pin_led_id.low()
            await asyncio.sleep(0.05)
        
    dr1x.on_check_usage_start_connect(id_blink)

    while(True):
        dr1x.check_repeater_in_use() # asyncio wont work here. rethink
        dr1x.tx_start()
        utime.sleep(5)
        dr1x.tx_stop()
        utime.sleep(5)


