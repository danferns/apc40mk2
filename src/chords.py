from setup_daw import note_on, note_off
from param import params


class ChordShape:
    MAJOR = (0, 4, 7)
    MINOR = (0, 3, 7)
    SUS4 = (0, 5, 7)
    MAJOR_SEVENTH = (0, 4, 7, 11)
    MINOR_SEVENTH = (0, 3, 7, 10)


def y_to_chord(y):
    return {
        0: ChordShape.MAJOR,
        1: ChordShape.MINOR,
        2: ChordShape.SUS4,
        3: ChordShape.MAJOR_SEVENTH,
        4: ChordShape.MINOR_SEVENTH,
    }[y]


def x_to_root(x):
    return {
        1: 0,
        2: 2,
        3: 4,
        4: 5,
        5: 7,
        6: 9,
        7: 11,
    }[x]


def chord_to_notes(root, shape):
    octave = 5
    notes = []
    for note in shape:
        notes.append(12 * octave + note + root)

    return notes


chords_held = []


def play_chord(root, shape):
    notes = chord_to_notes(root, shape)
    for note in notes:
        note_on(note, params["velocity"])

    chords_held.append({"root": root, "shape": shape})


def release_chord(root, shape):
    this_chord_notes = set(chord_to_notes(root, shape))
    other_chords_notes = set()
    chords_held.remove({"root": root, "shape": shape})
    for chord in chords_held:
        other_chords_notes.update(chord_to_notes(chord["root"], chord["shape"]))

    # only release notes that are not held down by other chords simultaneously
    notes_to_release = this_chord_notes - other_chords_notes

    for note in notes_to_release:
        note_off(note)

