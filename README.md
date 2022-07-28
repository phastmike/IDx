# picoIDx
A Yaesu DR-1x Voice Identification Controller w/ Raspberry Pi Pico Board

## Description

This project is based around the Raspberry Pi Pico (RP2040). It uses some digital
GPIOs to control the repeater for voice identification purposes. The original YAESU
option is very limited. 

### Requirements/Features

Notes:

- Agressive mode (ID immediately - Vs relaxed, wait x sec. after no in use)
- Improved ID tryout by averaging instead of a single switch :/

---

- ID "every" 10 minutes (*done*)
- ID **only** if the repeater is not in use (*done?)
- Remove ISD dependency by using PWM Audio (*done*)
- Leds for hmi (*done : On, CTCSS Detect, TX ID [Blink - ID tryout]*)
- Telemetry (*done - internal temperature*)
- Announcements (*done - How to schedule? Now it's repeating every hour*)

---

- *needs any hmi input?*
- *Suppose connection to PC (Hw)?*
- *Repo HW/SW or separated?*

## Implementation

The advantage of using the Pico and specially the Python
SDK is that the filesystem is already there amongst others.

Power is drawn from DE/H-15 Plug, 13.8V 2A (Fuse 3A) and regulated to 5V.
Not many electronics needed, direct interfacing does work with internal pull-ups.
Can have both VCC from radio and USB VCC as voltage supply and the power switch
it's controlling only the radio power supply.

The PWM Audio goes thru a low pass filter and the colume control it's a simple
resistive voltage divider.

Three leds present some information to the user:

1. Power On
2. CTCSS Detection
3. Tx Identification *(\*)*

*(\*) blinks while checking if the repeater it's in use*


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