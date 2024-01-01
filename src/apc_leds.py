from setup_apc import outport

import mido


class Beat:
    CONSTANT = 0
    ONESHOT = {
        24: 1,
        16: 2,
        8: 3,
        4: 4,
        2: 5,
    }
    PULSING = {
        24: 6,
        16: 7,
        8: 8,
        4: 9,
        2: 10,
    }
    BLINKING = {
        24: 11,
        16: 12,
        8: 13,
        4: 14,
        2: 15,
    }


def led_on(note, color, beat_channel):
    msg = mido.Message("note_on", note=note, velocity=color, channel=beat_channel)
    outport.send(msg)


def led_off(note):
    msg = mido.Message("note_off", note=note, velocity=0, channel=0)
    outport.send(msg)


def clear_leds():
    for i in range(0, 127):
        led_off(i)


def color_palette(i):
    level = i - i % 2
    add = 4 + level
    return i + add


def display_color_palette():
    for i in range(0, 40):
        led_on(i, color_palette(i), Beat.CONSTANT)
