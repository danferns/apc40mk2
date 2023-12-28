from setup_apc import inport

from apc_leds import clear_leds, Beat, color_palette, led_on
from apc_matrix import is_matrix, matrix_to_note, note_to_matrix

from chords import chord_to_notes, play_chord, release_chord, x_to_root, y_to_chord
from param import is_param_update, update_param


BACKGROUND_COLOR = color_palette(matrix_to_note(1, 4))
FOREGROUND_COLOR = color_palette(matrix_to_note(5, 2))
HIGHLIGHT_COLOR1 = color_palette(matrix_to_note(0, 4))
HIGHLIGHT_COLOR2 = color_palette(matrix_to_note(2, 3))
HIGHLIGHT_COLOR3 = color_palette(matrix_to_note(3, 2))


def init():
    clear_leds()
    # for i in range(0, 40): # uncomment to view color palette
    #     led_on(i, color_palette(i), Beat.CONSTANT)
    # return

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
            play_chord(root, chord_shape)

            # highlight chords that have at least one note in common
            for mx in range(1, 8):
                for my in range(0, 5):
                    if mx == x and my == y:
                        continue

                    notes_of_iter_chord = set(chord_to_notes(root, chord_shape))
                    notes_of_this_chord = set(
                        chord_to_notes(x_to_root(mx), y_to_chord(my))
                    )
                    n_common_notes = len(
                        notes_of_iter_chord.intersection(notes_of_this_chord)
                    )
                    if n_common_notes == 1:
                        led_on(matrix_to_note(mx, my), HIGHLIGHT_COLOR1, Beat.CONSTANT)
                    elif n_common_notes == 2:
                        led_on(matrix_to_note(mx, my), HIGHLIGHT_COLOR2, Beat.CONSTANT)
                    elif n_common_notes >= 3:
                        led_on(matrix_to_note(mx, my), HIGHLIGHT_COLOR3, Beat.CONSTANT)
                    else:
                        led_on(matrix_to_note(mx, my), BACKGROUND_COLOR, Beat.CONSTANT)

        case "note_off":
            # led_on(msg.note, FOREGROUND_COLOR, Beat.PULSING[8])
            release_chord(root, chord_shape)


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
