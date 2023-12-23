import mido

from setup_apc import inport
from setup_daw import dawport

from apc_leds import clear_leds, Beat, color_palette, led_on
from apc_matrix import is_matrix, matrix_to_note, note_to_matrix

from chords import x_to_root, y_to_chord
from param import is_param_update, params, update_param


BACKGROUND_COLOR = color_palette(matrix_to_note(1, 4))
FOREGROUND_COLOR = color_palette(matrix_to_note(5, 2))


def init():
    clear_leds()
    for x in range(1, 8):
        for y in range(0, 5):
            led_on(matrix_to_note(x, y), BACKGROUND_COLOR, Beat.CONSTANT)


def matrix_handler(msg):
    x, y = note_to_matrix(msg.note)
    if x == 0:
        return

    root = x_to_root(x)
    chord_shape = y_to_chord(y)
    match msg.type:
        case "note_on":
            led_on(msg.note, FOREGROUND_COLOR, Beat.ONESHOT[16])
            for note in chord_shape:
                dawport.send(
                    mido.Message(
                        "note_on",
                        note=root + note + 60,
                        velocity=params["velocity"],
                    )
                )

        case "note_off":
            led_on(msg.note, BACKGROUND_COLOR, Beat.CONSTANT)
            for note in chord_shape:
                dawport.send(
                    mido.Message("note_off", note=root + note + 60, velocity=0)
                )


event_listeners = [
    {"check": is_matrix, "action": matrix_handler},
    {"check": is_param_update, "action": update_param},
]


init()

for msg in inport:
    print(msg)
    for listener in event_listeners:
        if listener["check"](msg):
            listener["action"](msg)
            break
