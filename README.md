# pi_hifi_ctrl
# Raspberry Pi Hi-Fi Amplifier Control

This project aims to breathe new life into old Hi-Fi amplifiers/receivers, by adding network (or automatic) control via a Raspberry Pi.

## Supported Amplifiers:

* Cambridge Audio azur 540A/640A v2, 840A v2

If you have another Cambridge Audio amplifier, please contact me, I'll do my best to find the relevant documentation and add support for it.

## Dependencies:

* **Python 3** (apt-get install python3)
* **pigpio library**, with *pigpiod* running (see https://github.com/joan2937/pigpio/ or http://abyz.co.uk/rpi/pigpio/).
* **cec-utils** (apt-get install cec-utils) if **/usr/bin/cec-client** is not already installed.

## Wiring:
* Pick an unused GPIO pin on your Pi (the default is GPIO 4). 
* Connect your pin to the signal wire of an RCA cable, and a ground to the shield.
* Plug the RCA cable in to the "Ctrl In" socket on your Cambridge Audio amplifier.

## ca_amp_ctrl.py Usage:

ca_amp_ctrl.py is used to send a command to the amplifier.

    ca_amp_ctrl.py [-h] [--pin [GPIO number]] [--repeat [positive integer]] command

Exactly one command must be specified.

| Command        | Function     | 
| ------------- |-------------| 
| **ampon**      | power on | 
| **ampoff**, **standby** | power off |
| **aux**, **av**, **cd**, **dvd**, **tapemon**, **tuner** | source selections ("av" is the "DMP/MP3" input) |
| **source+**, **source-** | select next/previous source |
| **tapemon** | toggle tape monitoring |
| **vol+**, **vol-** | increase/decrease volume (a small increment) |
| **mute**, **muteon**, **muteoff** | mute toggle/on/off |
| **clipon**, **clipoff** | probably turns on/off clipping protection (untested) |
| **bright** | *maybe display brightness?* |

The other optional arguments are:

**-h** merely shows brief usage help  
**--pin [GPIO number]** to specify the GPIO pin to transmit on (default: 4)  
**--repeat [positive integer]** to repeat the command (e.g. vol+/vol- only move the volume a very small amount)  

## cec_stream.py Usage:

cec_stream.py is used to receive commands from a TV via HDMI and forward them on to the amplifier. The amplifier will turn on & off when the TV does, and will respond to the TV's volume & mute buttons.

Copy cec_stream.py into /home/pi/cec/ and startup_cec in /etc/init.d/ , then run:

    sudo update-rc.d startup_cec defaults

It will then start/stop when you boot/shutdown.
Plug an HDMI cable from your pi into the TV, preferably via the "ARC" HDMI port.
