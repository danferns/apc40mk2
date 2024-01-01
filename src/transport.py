import mido
from setup_daw import dawport


controls = {
    "play": 91,
    "record": 93,
}


def is_transport(msg):
    return (
        (msg.type == "note_on" or msg.type == "note_off")
        and msg.note in controls.values()
        and msg.channel == 0
    )


playing = False


def transport_handler(msg):
    global playing
    if msg.note == controls["play"]:
        if msg.type == "note_on":
            if not playing:
                # send MMC play
                dawport.send(mido.Message("continue"))
                playing = True
            else:
                # send MMC stop
                dawport.send(mido.Message("stop"))
                playing = False

    if msg.note == controls["record"]:
        if msg.type == "note_on":
            # send MMC record
            dawport.send(mido.Message("record_start"))
        else:
            dawport.send(mido.Message("record_stop"))
