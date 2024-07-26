from apc_leds import Beat, bright_hues, color_palette, led_on
from chord_player import (
    chord_to_notes,
    play_chord,
    release_chord,
    x_to_root,
    y_to_chord,
)
from chord_theory import chord_transition_dissonance


def matrix_to_note(x, y):
    return 8 * y + x


def note_to_matrix(note):
    return (note % 8, note // 8)


def is_matrix(msg):
    return (
        (msg.type == "note_on" or msg.type == "note_off")
        and msg.note < 40
        and msg.channel == 0
    )


ACTIVE_CHORD_COLOR = color_palette(matrix_to_note(5, 2))

# based on the matrix color palette
DISSONANCE_COLORS = [
    (3, 2),
    (1, 2),
    (7, 1),
    (5, 1),
    (0, 4),
    (6, 3),
    (3, 1),
    (0, 1),
    (7, 0),
    (5, 0),
    (5, 3),
    (3, 0),
    (4, 3),
    (1, 0),
    (3, 3),
    (7, 5),
    (7, 2),
]


def matrix_handler(msg):
    x, y = note_to_matrix(msg.note)
    if x == 0:
        return

    root = x_to_root(x)
    chord_shape = y_to_chord(y)

    match msg.type:
        case "note_on":
            led_on(msg.note, ACTIVE_CHORD_COLOR, Beat.ONESHOT[16])
            play_chord(root, chord_shape)

            # color chords based on dissonance
            for mx in range(1, 8):
                for my in range(0, 5):
                    if mx == x and my == y:
                        continue

                    notes_of_active_chord = set(chord_to_notes(root, chord_shape))
                    notes_of_iter_chord = set(
                        chord_to_notes(x_to_root(mx), y_to_chord(my))
                    )
                    dissonance = chord_transition_dissonance(
                        notes_of_active_chord, notes_of_iter_chord
                    )

                    norm_diss = min(dissonance, 14) / 14
                    hueIndex = int(20 * (1 - norm_diss**1.5))

                    led_on(
                        matrix_to_note(mx, my),
                        bright_hues(hueIndex),
                        Beat.CONSTANT,
                    )

        case "note_off":
            release_chord(root, chord_shape)
