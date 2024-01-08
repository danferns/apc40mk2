import mido
from setup_daw import dawport
from setup_apc import outport


controls = {
    "play": 91,
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
                outport.send(msg)
                playing = True
            else:
                # send MMC stop
                dawport.send(mido.Message("stop"))
                outport.send(msg.copy(velocity=0))
                playing = False

