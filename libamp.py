"""
Send RC5-encoded commands to suit Cambridge Audio amplifiers.

Confirmed working with:
  Cambridge Audio azur 540A v2
"""

import pigpio

pi = pigpio.pi()


#############
# CONSTANTS #
#############

RC5_PER = 889  # half-bit period (microseconds)
CA_RC5_SYS = 16

# dictionary of supported models, each containing:
#   a dictionary of possible commands, mapped to the code we need to send
command_table = {
    "540A": {
        "aux": 4,
        "cd": 5,
        "tuner": 3,
        "dvd": 1,
        "av": 2,
        "tapemon": 0,
        "vol-": 17,
        "voldown": 17,
        "vol+": 16,
        "volup": 16,
        "mute": 13,
        "standby": 12,
        "bright": 18,
        "source+": 19,
        "source-": 20,
        "sourcenext": 19,
        "sourceprev": 20,
        "clipoff": 21,
        "clipon": 22,
        "muteon": 50,
        "muteoff": 51,
        "ampon": 14,
        "ampoff": 15,
    },
    "840A": {
        "source1": 4,
        "source2": 5,
        "source3": 3,
        "source4": 1,
        "source5": 2,
        "source6": 0,
        "source7": 6,
        "source8": 7,
        "tapemon": 7,
        "vol-": 17,
        "voldown": 17,
        "vol+": 16,
        "volup": 16,
        "mute": 13,
        "bright": 18,
        "source+": 8,
        "source-": 9,
        "sourcenext": 8,
        "sourceprev": 9,
        "muteon": 50,
        "muteoff": 51,
        "ampon": 14,
        "ampoff": 15,
        "spkselect": 20,
        "clipoff": 21,  # enters Balance mode
    },
    "CXA60": {
        "muteon": 50,
        "muteoff": 51,
        "vol+": 16,
        "vol-": 17,
        "poweron": 110,
        "poweroff": 111,
    },
}

all_models = {model for model in command_table}
all_commands = {command for model in all_models for command in command_table[model]}

#############
# Functions #
#############


def build_rc5(cmd: int) -> int:
    """Build an RC5 message"""
    RC5_START = 0b100 + (0b010 * (cmd < 64))
    RC5_SYS = int(CA_RC5_SYS)
    RC5_CMD = int(cmd)

    # RC-5 message has a 3-bit start sequence, a 5-bit system ID, and a 6-bit command.
    RC5_MSG = (
        ((RC5_START & 0b111) << 11) | ((RC5_SYS & 0b11111) << 6) | (RC5_CMD & 0b111111)
    )

    return RC5_MSG


def wave_mnch(DATA: int, PIN: int):
    """
    manchester encode waveform. Period is the half-bit period in microseconds.
    """
    pi.set_mode(PIN, pigpio.OUTPUT)  # set GPIO pin to output.

    # create msg
    # syntax: pigpio.pulse(gpio_on, gpio_off, delay us)
    msg = []

    # this is a terrible way to iterate over bits... but it works.
    for i in bin(DATA)[2:]:
        if i == "1":
            msg.append(pigpio.pulse(0, 1 << PIN, RC5_PER))  # L
            msg.append(pigpio.pulse(1 << PIN, 0, RC5_PER))  # H
        else:
            msg.append(pigpio.pulse(1 << PIN, 0, RC5_PER))  # H
            msg.append(pigpio.pulse(0, 1 << PIN, RC5_PER))  # L

    msg.append(pigpio.pulse(0, 1 << PIN, RC5_PER))  # return line to idle condition.
    pi.wave_add_generic(msg)
    wid = pi.wave_create()
    return wid


def posint(n):
    """check for positive integer"""
    try:
        if int(n) > 0:
            return int(n)
        else:
            raise ValueError
    except ValueError:
        msg = str(n) + " is not a positive integer"
        raise argparse.ArgumentTypeError(msg)


def execute(pin: int, command: str, repeat: int, model: str = "504A"):
    """execute a given command"""

    # generate RC5 message (int)
    rc5_msg = build_rc5(command_table[model][command])

    # generate digital manchester-encoded waveform
    wid = wave_mnch(rc5_msg, pin)

    for i in range(repeat):
        cbs = pi.wave_send_once(wid)
