'''

 Yaesu DR-1x Voice Identification Controller
 w/ Raspberry Pi Pico Board

 2022 CT1ENQ - José Miguel Fonte
         ARM - Associação de Rádioamadores do Minho - CS5ARM/CS1ARM/CT1ARM

 Equipa da ARM:
 CT1BDV Emanuel, CT1ENQ Miguel, CT1EYN Costa, CS7AFE Carlos, CT1EUK Freitas, CR7AQJ Soares

 Power could be drawn from DE/H-15 Plug, 13.8V 2A (Fuse 3A) and regulated to 5V
 Not much electronics needed, direct interfacing does work with internal pull-ups
 
 Runs on Micropython version 1.18, 1.19.1

'''
import utime
import os as uos
from hmi import HMI
from dr1x import DR1x
from machine import Pin
from wavePlayer import wavePlayer
from picoTemperature import picoTemperature
from temperatureAsAudio import temperatureAsAudio

# for PIO Blinky
import time
import rp2


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


version = "0.1"
author = "CT1ENQ"
app = "Pico IDx"
    
if __name__ == "__main__":

    # init
    print("[Init] :: %s version %s by %s @ 2022" % (app, version, author))
    
    # Instantiate a state machine with the blink program, at 2000Hz, with set bound to Pin(25) (LED on the rp2 board)
    # Run the state machine, the internal LED should blink.
    sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))
    sm.active(1)
    
    hmi = HMI()
    audioPath = "audio/"
    temperature_threshold = 30.0
    pico_temp = picoTemperature()
    taa = temperatureAsAudio()
    
    # Could use hmi methods instead of direct
    # reference to the led/pin

    dr1x = DR1x()
    dr1x.on_tx_start_connect(hmi.led_id.high)
    dr1x.on_tx_stop_connect(hmi.led_id.low)

    # IRQ Handler for CTCSS
    def irq_on_ctcss(pin):
        if pin.value() == 0:
            pin_led_ctcss.high()
        else:
            pin_led_ctcss.value(0)
        
    #pin_dr1x_ctcss_rx.irq(irq_on_ctcss, Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)
    dr1x.ctcss_get_hw_pin().irq(irq_on_ctcss, Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)

    # Init Leds 
    hmi.led_ctcss.low()
    hmi.led_id.low()
    
    #init audio player
    player = wavePlayer()
    audioId = audioPath + "main_id.wav"
    
    count_1h = 0
    
    try:
        while True:
            # Check repeater in use
            count = 0
            print("[Info] :: Checking if repeater is free to ID...")
            while True:
                count = count + 1
                if dr1x.ctcss_detected() == 0:
                    count = 0
                    print("[Warn] :: CTCSS detected, busy? => Reset counter")
                #utime.sleep(0.05)
                utime.sleep_ms(50)
                hmi.led_id.value(not hmi.led_id.value())
                if count % 20 == 0:
                    print ("[Time] :: Elapsed %d/10 sec." % ((int) (count / 20)))
                if count >= 200:
                    print ("[Info] :: Will ID Repeater now by playing %s file..." % audioId)
                    break
                        
            # Start Tx
            dr1x.tx_start()
            utime.sleep(0.75)

            # Play ID
            #audioId = audioPath.join("main_id.wav")
            
            try:
                player.play(audioId)
            except:
                print("[Errr] :: exception in id file audio/main_id.wav...")
            
            # measure temperature
            temperature = pico_temp.get_temperature() + 7
            #print("Temperature %.1f C" % temperature)
            if (temperature <= 5 or temperature >= temperature_threshold):
                print("[Warn] :: Temperature %.1f above %.1f :: Playing temperature as audio..." % (temperature, temperature_threshold))
                utime.sleep(1)
                taa.play_temperature_as_audio(temperature)
                utime.sleep(0.25)
            
            # Play Announcement
            #audioAnnouncement = audioPath.join("main_an.wav")
            #if audioAnnouncement in uos.listdir():

            # If one hour elapsed, play the announcement if exists
            if count_1h >= 6:
                count_1h = 0
                try:
                    player.play(audioPath + "main_an.wav")
                except:
                    print("[Warn] :: exception in announcement file audio/main_an.wav...")
            #else:
            #    print("count_1h = %d" % count_1h)
            
            #stop TX
            utime.sleep(0.75)
            dr1x.tx_stop()

            # Wait most of 10 minutes
            #utime.sleep(590)
            print("[Info] :: Will sleep until next ID...")
            utime.sleep(60)
            
            # If 1 hour elapsed then play the announcement if it exists
            count_1h += 1

            
    except KeyboardInterrupt:
        print("[Warn] :: Ctrl + c : Exit mainloop...")
        sm.active(0)
        player.stop()
        
        
