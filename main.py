'''

 Yaesu DR-1x Voice Identification Controller
 w/ Raspberry Pi Pico Board

 2022 CT1ENQ - José Miguel Fonte
         ARM - Associação de Rádioamadores do Minho - CS5ARM/CS1ARM/CT1ARM

 ARM team:
 CT1BDV Emanuel, CT1ENQ Miguel, CT1EYN Costa, CS7AFE Carlos, CT1EUK Freitas, CR7AQJ Soares

 Runs on Micropython version 1.18, 1.19.1

'''
import utime
import constants as const
import os as uos
import micropython
from hmi import HMI
from dr1x import DR1x
from machine import Pin, Timer
from wavePlayer import wavePlayer
from picoTemperature import picoTemperature
from temperatureAsAudio import temperatureAsAudio

    
if __name__ == "__main__":

    dr1x = DR1x()
    hmi = HMI()

    pico_temp = picoTemperature()
    taa = temperatureAsAudio()

    player = wavePlayer()
    audioId = const.AUDIO_PATH + const.AUDIO_ID_FILE
    audioAnn = const.AUDIO_PATH + const.AUDIO_ANN_FILE

    # init
    print("[Init] :: %s version %s by %s @ %s" % (const.APP_NAME, const.APP_VERSION, const.APP_AUTHOR, const.APP_YEAR))
    print("[Conf] :: ==================================================================")
    print("[Pico] :: CPU Freq: %.1f MHz" % (machine.freq() / 1000000))
    print("[Conf] :: Usage check duration: %d sec." % (const.USAGE_CHECK_DURATION))
    print("[Conf] :: Usage check frequency: %.1f Hz" % (const.SAMPLING_FREQ))
    print("[Conf] :: Usage check period: %.2f sec (%.1f ms)" % (const.SAMPLING_PERIOD_SEC, const.SAMPLING_PERIOD_MS))
    print("[Conf] :: Temperature threshold: %.1f degC" % (const.TEMPERATURE_THRESHOLD))
    print("[Conf] :: ID file %s %s" % (audioId, "found" if const.AUDIO_ID_FILE in uos.listdir(const.AUDIO_PATH) else "*** NOT FOUND ***"))
    print("[Conf] :: Announcement file %s %s" % (audioAnn, "found" if const.AUDIO_ANN_FILE in uos.listdir(const.AUDIO_PATH) else "*** NOT FOUND ***"))
    print("[Conf] :: ID interval: %d minutes (%d sec)" % (const.SLEEP_MIN, const.SLEEP_MIN * 60))
    print("[Conf] :: ==================================================================")

    hmi.led_pico_blink_enable()
    dr1x.on_tx_start_connect(hmi.led_id.high)
    dr1x.on_tx_stop_connect(hmi.led_id.low)

    def timer_callback(t):
        hmi.led_id.toggle()

    # IRQ Handler for CTCSS
    def irq_on_ctcss(pin):
        if pin.value() == 0:
            hmi.led_ctcss.high()
        else:
            hmi.led_ctcss.low()
        
    dr1x.set_irq_routine(irq_on_ctcss)

    
    # Local nested functions

    def play_id():
        try:
            print("[IDx ] :: Trying to play id ...")
            player.play(audioId)
        except:
            print("[Errr] :: exception in id file %s ..." % audioId)

    def check_temperature_and_inform_if_above(x_deg):
        # measure temperature
        # hardcoded minimum of 5 deg C
        temperature = pico_temp.get_temperature() + 7.0
        print("[Temp] :: Temperature %.1f C" % temperature)
        if (temperature <= 5.0 or temperature >= x_deg):
            print("[Warn] :: Temperature %.1f above %.1f :: Try playing temperature as audio ..." % (temperature, x_deg))
            utime.sleep(1)
            try:
                taa.play_temperature_as_audio(temperature)
            except:
                print("[Errr] :: exception in temperature audio ...")
            utime.sleep(0.25)

    def check_if_its_time_to_announce(every_ntimes, count):
        print("[Dbug] :: count is %d >= %d ? %s" % (count, every_ntimes, "Yes, will reset count to 0 ..." if count >= every_ntimes else "No ..."))
        if count >= every_ntimes:
            count = 0
            try:
                print("[IDx ] :: Trying to play announcement ...")
                player.play(audioAnn)
            except:
                print("[Warn] :: exception in announcement file audio/main_an.wav...")
        return count

    # ---
    # Repeater to boot - It takes around 6 sec. to boot
    # or human triggered ID reset - no delay
    # don't do nothing it's a good compromise
    # ---
    #utime.sleep(6)
    

    count_ann = 0

    try:
        while True:
            
            # Check repeater in use
            count = 0
            print("[Info] :: Checking if repeater is free to ID ...")
            print("[Time] ::", end = " ")
            tim = machine.Timer(period=const.SAMPLING_PERIOD_MS * 4, callback=timer_callback)

            while True:
                count = count + 1

                # If there is some activity, start recount
                # Can be improved to be more smart then
                # a simple unique detection.
                # First approach, increase detection time
                if dr1x.ctcss_detected() == True:
                    count = 0
                    #print ("[Warn] :: CTCSS detected => Reset counter ...")

                utime.sleep_ms(const.SAMPLING_PERIOD_MS)

                if count % (const.SAMPLING_FREQ) == 0 and count != 0:
                    print ("%d" % (int) (count / const.SAMPLING_FREQ), end=" ")
                    #print ("[Time] :: Elapsed %d/%d sec." % ((int) (count / const.SAMPLING_FREQ), const.USAGE_CHECK_DURATION), end = " ")
                if count >= (const.USAGE_CHECK_DURATION * const.SAMPLING_FREQ):
                    print ("")
                    print ("[Info] :: Will ID Repeater ...")
                    tim.deinit()
                    break
                        
            # Start Tx
            dr1x.tx_start()
            utime.sleep(0.75)

            play_id()
            check_temperature_and_inform_if_above(const.TEMPERATURE_THRESHOLD)
            count_ann = check_if_its_time_to_announce(6, count_ann)

            #stop TX
            utime.sleep(0.75)
            dr1x.tx_stop()

            # Wait most of 10 minutes
            print("[Info] :: *********************************************")
            print("[Info] :: * Will *** LONG SLEEP *** until next ID ... *")
            print("[Info] :: *********************************************")
            utime.sleep((const.SLEEP_MIN * 60) - const.USAGE_CHECK_DURATION)
            
            count_ann += 1

            
    except KeyboardInterrupt:
        print("[Warn] :: Ctrl + c : Exit mainloop ...")
        hmi.led_pico_blink_disable()
        player.stop()
        
        
