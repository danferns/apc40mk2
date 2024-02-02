import mido
from setup_daw import dawcontrolport
import setup_apc

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
                dawcontrolport.send(mido.Message("continue"))
                setup_apc.outport.send(msg)
                playing = True
            else:
                # send MMC stop
                dawcontrolport.send(mido.Message("stop"))
                setup_apc.outport.send(msg.copy(velocity=0))
                playing = False

