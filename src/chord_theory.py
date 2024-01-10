class ChordShape:
    MAJOR = (0, 4, 7)
    MINOR = (0, 3, 7)
    SUS4 = (0, 5, 7)
    MAJOR_SEVENTH = (0, 4, 7, 11)
    MINOR_SEVENTH = (0, 3, 7, 10)


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
