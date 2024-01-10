from threading import Thread
import time

from setup_daw import note_on, note_off
from param import params
from chord_theory import ChordShape


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

def strum_chord(notes, velocity):
    notes.sort() # strum up
    delay = params["strum"] / 127
    delay *= 5 # max duration
    for note in notes:
        note_on(note, velocity)
        time.sleep(delay)

def play_chord(root, shape):
    notes = chord_to_notes(root, shape)
    strum_thread = Thread(target=strum_chord, args=(notes, params["velocity"]))
    strum_thread.start()
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
