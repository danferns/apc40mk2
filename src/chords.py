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
        0: ChordShape.MAJOR_SEVENTH,
        1: ChordShape.MAJOR,
        2: ChordShape.SUS4,
        3: ChordShape.MINOR,
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
    center = params["chord-center"]
    octave = center // 12
    notes = []
    for note in shape:
        real_note = note + root + octave * 12
        real_note_octave_high = real_note + 12
        real_note_octave_low = real_note - 12
        if abs(real_note_octave_high - center) < abs(real_note - center):
            real_note = real_note_octave_high
        elif abs(real_note_octave_low - center) < abs(real_note - center):
            real_note = real_note_octave_low

        notes.append(real_note)

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


"""
for chord trasition from chord A to chord B 

for each note from chord B
find the smallest circle-of-fifths distance from any note from chord A
add these up to get a transition-dissonance score
higher values mean more dissonant chord change.
"""

circle_of_fifths = [
    0,  # C
    7,  # G
    2,  # D
    9,  # A
    4,  # E
    11,  # B
    6,  # Gb
    1,  # Db
    8,  # Ab
    3,  # Eb
    10,  # Bb
    5,  # F
]


def circle_of_fifths_distance(note1, note2):
    return abs(circle_of_fifths.index(note1 % 12) - circle_of_fifths.index(note2 % 12))


def chord_transition_dissonance(chord1, chord2):
    return sum(
        [
            min([circle_of_fifths_distance(note1, note2) for note1 in chord1])
            for note2 in chord2
        ]
    )
