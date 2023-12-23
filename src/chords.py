class ChordShape:
    MAJOR = [0, 4, 7]
    MINOR = [0, 3, 7]
    SUS4 = [0, 5, 7]
    MAJOR_SEVENTH = [0, 4, 7, 11]
    MINOR_SEVENTH = [0, 3, 7, 10]


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


