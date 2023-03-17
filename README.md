# IDx
A Yaesu DR-1x Voice Identification Controller w/ a Raspberry Pi Pico Board

![IDx](https://github.com/phastmike/IDx_hardware/raw/master/images/img1.jpg "Hardware Implementation")

## Description

This project, also known as picoIDx or simply IDx, is based around the Raspberry Pi Pico (RP2040). It uses some digital
GPIOs to control the repeater for voice identification purposes. 

The original YAESU option is very limited. 

### Features

- [x] ID "every" 10 minutes
- [x] ID **only** if the repeater is not in use (Detects CTCSS/C4FM)
- [x] Remove ISD voice record/play board dependency by using PWM Audio
- [x] Leds for hmi [ **On | CTCSS/C4FM Detect | TX ID** *(Blinks during ID tryout)* ]
- [x] Telemetry
- [x] Announcements

Improvements that could be implemented:

- Agressive mode (ID immediately Vs relaxed ID, wait x seconds without signals on the input)
- Improved ID tryout by averaging instead of a single CTCSS/C4FM detection

## Implementation

The controller it's very basic, it checks CTCSS/C4FM pin for activity on the repeater and
also counts minutes until ID. Reaching time to ID it will wait for a, user defined, small amount
of seconds without any activity on the repeater input. Any activity will reset the
counter, so the controller holds the ID transmition up to the moment where the defined amount of
seconds elapsed without any reception and then play the ID.

In this project we decided to go along with micropython.

The advantage of using the Pico and specially the Python
SDK is that the filesystem is already there amongst others.

This is crucial for the audio files being used for ID, temperature to audio 
conversion and announcements.

These files are located in the `audio/` folder. Annoucements are programatically
defined as being played every 6 IDs which equates to 1 hour when using ID intervals
of 10 minutes:

```python
...
count_ann = check_if_its_time_to_announce(6, count_ann)
...
```

If we don't want announcements, simply delete the annoucement file `main_ann.wav`.
The ID file is `main_id.wav` and all the configurations are listed in `constants.py`.

### Sample debug output

If this controller is connected to a PC, you can check the debug output via
thonny or any other REPL tool. Here is a sample:

```text
[Init] :: Pico IDx version 1.0 by CT1ENQ @ 2022
[Conf] :: ==================================================================
[Pico] :: CPU Freq: 125.0 MHz
[Conf] :: Usage check duration: 8 sec.
[Conf] :: Usage check frequency: 20.0 Hz
[Conf] :: Usage check period: 0.05 sec (50.0 ms)
[Conf] :: Temperature threshold: 35.0 degC
[Conf] :: ID file audio/main_id.wav found
[Conf] :: Announcement file audio/main_an.wav *** NOT FOUND ***
[Conf] :: ID interval: 10 minutes (600 sec)
[Conf] :: ==================================================================
[HMI ] :: Led Pico started blinking
[Info] :: Checking if repeater is free to ID ...
[Time] :: Elapsed 1/8 sec.
[Time] :: Elapsed 2/8 sec.
[Time] :: Elapsed 3/8 sec.
[Time] :: Elapsed 4/8 sec.
[Time] :: Elapsed 5/8 sec.
[Time] :: Elapsed 6/8 sec.
[Time] :: Elapsed 7/8 sec.
[Time] :: Elapsed 8/8 sec.
[Info] :: Will ID Repeater ...
[DR1X] :: Will START TX now ...
[IDx ] :: Trying to play id ...
[Temp] :: Temperature 27.5 C
[Dbug] :: count is 0 >= 6 ? No ...
[DR1X] :: Will STOP TX now ...
[Info] :: *****************************************************
[Info] :: Will *** SLEEP *** 592 seconds until next ID ... 
[Info] :: *****************************************************
```

### PWM Audio

The PWM audio code came from:

- https://github.com/danjperron/PicoAudioPWM

with dependencies from:

- https://github.com/joeky888/awesome-micropython-lib/tree/master/Audio

## Hardware

**The hardware schematic is available on [another repository](https://github.com/phastmike/IDx_hardware)** but some insights are
needed on the software side, namely the pinout used for the repeater signals and
HMI (Human Machine Interface) LEDs.

Power is drawn from DE/H-15 Plug, 13.8V 2A (Fuse 3A) and regulated to 5V.
Not many electronics needed, direct interfacing does work with internal pull-ups.
**We can have both VCC, from radio and USB VCC as voltage supply** but the power switch
it's only controlling the supply coming from the radio.

The PWM Audio goes thru a low pass filter and the volume control it's a simple
resistive voltage divider.

Three leds present some information to the user:

```text
    LED     LED     LED
    [1]     [2]     [3] 

    ON     CTCSS    ID
          DETECTED   *

            ooo
          o  |  o
         o   |   o
          o     o
            ooo

           VOLUME
            POT


(*) Blinks while checking if channel is free for ID
```

### LED Pinout

The **Power On Led** is connected directly to the regulator, so **it will not light up
when the circuit is powered only by USB**.

- The CTCSS/C4FM detect led it's controlled by GPIO 17 (Pin 22)
- The ID Led it's controlled by GPIO 18 (Pin 24).

### DB/DE/DH 15 Pin VGA like connector

Cable colours as used in our DR-1X:

|DE-15 Pin|Colour|Action|J plug|GPIO|
|---------|------|------|------|----|
|1|Blue|Remote|1|0|
|2|White/Blue|PTT|2|1|
|3|White/Brown|CTCSS Detect |3|2|
|4|---|SQL Detect|---|---|
|5|Brown|GND|4|---|
|6|---|TONE IN|---|---|
|7|Green|AF IN|5|5 (+6 and 7)|
|8|---|DISC OUT|---|---|
|9|---|AF OUT|---|---|
|10|---|GND|---|---|
|11|White/Orange|EXT1 (*operating mode*)|6|3|
|12|---|EXT2 (*operating mode*)|---|---|
|13|White/Green|EXT3 (*CTCSS RX control*)|7|4|
|14|---|EXT4 (*CTCSS TX control*)|---|---|
|15|Orange|VCC (*13.8V/2A Fused at 3A*)|8|---|


Operating mode is intended as FM Fix/FM Fix which means:

- EXT 1: Low
- EXT 2: High

That's the reason we don't use pin 12, high by default.

These EXT pins are not mandatory to use as the repeater can be used to operate
in non remote mode.

## Author

CT1ENQ Miguel

## Support

ARM - Associação de Rádioamadores do Minho - CS5ARM/CS1ARM/CT1ARM

This project would not be possible without the help of the ARM repeater group,
listed below in alphabetic order: 

- CT1BDV Emanuel, 
- CT1EUK Freitas,
- CT1EYN Costa,
- CS7AFE Carlos,
- CS7ALF Constantino,
- CR7AQJ Soares.

## Links
- TextToSpeech: https://wideo.co/text-to-speech/

---

Done in 2022. CT1ENQ - José Miguel Fonte
