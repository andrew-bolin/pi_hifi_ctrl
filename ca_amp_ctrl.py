#!/usr/bin/python3

# Send RC5-encoded commands.
# Confirmed working with:
#   Cambridge Audio azur 540A v2


#############
# CONSTANTS #
#############

RC5_PER = 889 # half-bit period (microseconds)
CA_RC5_SYS = 16

# dictionary of possible commands, mapped to the code we need to send
cmd = {
        'aux': 4,
        'cd': 5,
        'tuner': 3,
        'dvd': 1,
        'av': 2,
        'tapemon': 0,
        'vol-': 17,
        'vol+': 16,
        'mute': 13,
        'standby': 12,
        'bright': 18,
        'source+': 19,
        'source-': 20,
        'clipoff': 21,
        'clipon': 22,
        'muteon': 50,
        'muteoff': 51,
        'ampon': 14,
        'ampoff': 15
        }

#############
# Functions #
#############

# build RC5 message, return as int
def build_rc5(sys, cmd):

    RC5_START = 0b110
    RC5_SYS = int(sys)
    RC5_CMD = int(cmd)

    # RC-5 message has a 3-bit start sequence, a 5-bit system ID, and a 6-bit command.
    RC5_MSG = ((RC5_START & 0b111) << 11) | ((RC5_SYS & 0b11111) << 6) | (RC5_CMD & 0b111111)
    
    return RC5_MSG

# manchester encode waveform. Period is the half-bit period in microseconds.
def wave_mnch(DATA, PIN, PERIOD):
    pi.set_mode(PIN, pigpio.OUTPUT) # set GPIO pin to output.

    # create msg
    # syntax: pigpio.pulse(gpio_on, gpio_off, delay us)
    msg = []
    for i in bin(DATA)[2:]: # this is a terrible way to iterate over bits... but it works.
        if i=='1':
            msg.append(pigpio.pulse(0,1<<PIN,PERIOD)) # L
            msg.append(pigpio.pulse(1<<PIN,0,PERIOD)) # H
        else:
            msg.append(pigpio.pulse(1<<PIN,0,PERIOD)) # H
            msg.append(pigpio.pulse(0,1<<PIN,PERIOD)) # L

    msg.append(pigpio.pulse(0,1<<PIN,PERIOD)) # return line to idle condition.
    pi.wave_add_generic(msg)
    wid = pi.wave_create()
    return wid

# check for positive integer
def posint(n):
    try:
        if int(n)>0:
            return int(n)
        else:
            raise ValueError
    except ValueError:
            msg = str(n) + " is not a positive integer"
            raise argparse.ArgumentTypeError(msg)

##############
# Start here #
##############

import pigpio
import sys
import argparse

pi = pigpio.pi()

# Build argument parser
parser = argparse.ArgumentParser(description="Control Cambridge Audio amplifiers.")
parser.add_argument('--pin', nargs='?', default=4, type=int)
parser.add_argument('--repeat', nargs='?', default=1, type=posint)
parser.add_argument('command', nargs=1, choices=cmd.keys())
args = parser.parse_args()

command = args.command[0].lower()
print("Sending '" + command + "' command to pin " + str(args.pin))

if args.repeat != 1:
    print(str(args.repeat) + " times")

# generate RC5 message (int)
rc5_msg = build_rc5(CA_RC5_SYS, cmd[command])
# generate digital manchester-encoded waveform
wid = wave_mnch(rc5_msg, args.pin, RC5_PER)

for i in range(args.repeat):
    cbs = pi.wave_send_once(wid)

sys.exit(0)
