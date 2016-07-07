# pi_hifi_ctrl
Raspberry Pi Hi-Fi Amplifier Control

This project aims to breathe new life into old Hi-Fi amplifiers/receivers, by adding network (or automatic) control via a Raspberry Pi.

Currently supported:

* Cambridge Audio azur 540A/640A v2

Dependencies:
Python 3 (apt-get install python3)
The pigpio library must be installed, and pigpiod running. 
See https://github.com/joan2937/pigpio/ or http://abyz.co.uk/rpi/pigpio/

Wiring:
Pick an unused GPIO pin on your Pi (the default is GPIO 4). 
Connect your pin to the signal wire of an RCA cable, and a ground to the shield.
Plug the RCA cable in to the "Ctrl In" socket on your Cambridge Audio amplifier.

Usage:

    ca_amp_ctrl.py [-h] [--pin [PIN]] [--repeat [REPEAT]] command

Where command is exactly one of:
{av,vol+,standby,clipon,source-,aux,tuner,ampon,mute,muteoff,clipoff,dvd,source+,bright,vol-,tapemon,cd,ampoff,muteon}

-h merely shows the usage information
--pin [GPIO number] is used to specify the GPIO pin to transmit on (default: 4)
--repeat [positive integer] is used to repeat the command (e.g. vol+/vol- only move the volumet a very small amount)
