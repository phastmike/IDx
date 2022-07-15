"""

"""

import machine
import utime


class picoTemperature:

    def __init__(self):
        self.sensor_temp = machine.ADC(4)
        self.conversion_factor = 3.3 / (65535)

    def get_temperature(self):
        reading = self.sensor_temp.read_u16() * self.conversion_factor 
        temperature = 27 - ((reading - 0.706)/0.001721)
        return round(temperature, 1)

if __name__ == "__main__":
    while True:
        picoTemp = picoTemperature()
        temperature = picoTemp.get_temperature()
        print("Temperature: {}".format(temperature))
        utime.sleep(2)
