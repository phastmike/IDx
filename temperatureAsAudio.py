"""
 - Does not support negative values.
"""

from wavePlayer import wavePlayer

class temperatureAsAudio:
    
    def __init__(self):
        self.audioPath = "audio/temperature/"
        self.player = wavePlayer()    

    def get_audio_file_from_number(self, number):
        if number == 1:
            return self.audioPath + "one.wav"
        elif number == 2:
            return self.audioPath + "two.wav"
        elif number == 3:
            return self.audioPath + "three.wav"
        elif number == 4:
            return self.audioPath + "four.wav"
        elif number == 5:
            return self.audioPath + "five.wav"
        elif number == 6:
            return self.audioPath + "six.wav"
        elif number == 7:
            return self.audioPath + "seven.wav"
        elif number == 8:
            return self.audioPath + "eigth.wav"
        elif number == 9:
            return self.audioPath + "nine.wav"
        elif number == 0:
            return self.audioPath + "zero.wav"
        else:
            return None
            
    def play_temperature_as_audio(self, temperature):
        self.player.play(self.audioPath + "temperature.wav")
        

        hundreds = int(temperature / 100)
        if (hundreds > 0):
            self.player.play(self.get_audio_file_from_number(hundreds))
        temperature -= hundreds * 100

        dozens = int(temperature / 10)
        if (dozens > 0 or hundreds > 0):
            self.player.play(self.get_audio_file_from_number(dozens))
        temperature -= dozens * 10
        
        units = int(temperature)
        self.player.play(self.get_audio_file_from_number(units))
        temperature -= units
        
        reminder = round (temperature * 10)
        if (reminder) > 0:
            self.player.play(self.audioPath + "dot.wav")
            self.player.play(self.get_audio_file_from_number(reminder))
            
        self.player.play(self.audioPath + "degres.wav")
        
if __name__ == "__main__":  
    maestro = temperatureAsAudio()
    for i in range(0,11):
        print("%d = %s" % (i, maestro.get_audio_file_from_number(i)))
    for i in range(0,10):
        file = maestro.get_audio_file_from_number(i)
        print(file)
        #maestro.player.play(file)
    
    maestro.play_temperature_as_audio(102.2)
    maestro.play_temperature_as_audio(23.5)
    maestro.play_temperature_as_audio(8)
