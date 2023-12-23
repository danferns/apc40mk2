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
