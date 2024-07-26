import setup_apc

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
    setup_apc.outport.send(msg)


def led_off(note):
    msg = mido.Message("note_off", note=note, velocity=0, channel=0)
    setup_apc.outport.send(msg)


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


def pastel_hues(i):
    huesAtlightness65 = [
        4,
        8,
        109,
        12,
        113,
        73,
        16,
        88,
        20,
        24,
        89,
        28,
        32,
        90,
        36,
        40,
        91,
        44,
        93,
        116,
        48,
        94,
        52,
        56,
    ]
    return huesAtlightness65[i]


def bright_hues(i):
    huesAtlightness50 = [
        5,
        72,
        60,
        84,
        9,
        108,
        96,
        13,
        74,
        110,
        98,
        86,
        75,
        17,
        21,
        87,
        25,
        29,
        77,
        33,
        37,
        78,
        41,
        92,
        79,
        45,
        67,
        80,
        49,
        81,
        53,
        95,
        57,
    ]
    return huesAtlightness50[i]
