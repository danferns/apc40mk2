from threading import Thread, Lock
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
notes_held = {}  # note -> chord[]

hold_release_lock = Lock()

def hold_note_of_chord(note, root, shape):
    hold_release_lock.acquire()
    if {"root": root, "shape": shape} in chords_held:
        if note not in notes_held:
            notes_held[note] = []
        notes_held[note].append({"root": root, "shape": shape})
        note_on(note, params["velocity"])
    hold_release_lock.release()


def release_note_of_chord(note, root, shape):
    hold_release_lock.acquire()
    if note in notes_held:
        if {"root": root, "shape": shape} in notes_held[note]:
            notes_held[note].remove({"root": root, "shape": shape})
            if len(notes_held[note]) == 0:
                note_off(note)
    
    hold_release_lock.release()


def delay_time():
    return params["strum"] / 127 * 5

def strum_chord(notes, root, shape):
    notes.sort()  # strum up
    for note in notes:
        # this will internally check if the chord is still held
        hold_note_of_chord(note, root, shape)
        # computing delay here means we use the realtime knob value
        time.sleep(delay_time())


def play_chord(root, shape):
    notes = chord_to_notes(root, shape)
    strum_thread = Thread(target=strum_chord, args=(notes, root, shape))
    strum_thread.start()
    chords_held.append({"root": root, "shape": shape})


def release_chord(root, shape):
    chord_notes = set(chord_to_notes(root, shape))
    for note in chord_notes:
        release_note_of_chord(note, root, shape)
    chords_held.remove({"root": root, "shape": shape})
