import mido

DAW_KEYS = "DAW Keys"
DAW_CONTROL = "DAW Control"

dawkeysport = None
dawcontrolport = None

for port in mido.get_output_names():
    if DAW_KEYS in port:
        dawkeysport = mido.open_output(port)
        print("Opened output port: " + port)
        break
    

for port in mido.get_output_names():
    if DAW_CONTROL in port:
        dawcontrolport = mido.open_output(port)
        print("Opened output port: " + port)
        break


if dawkeysport is None:
    print("Could not find DAW Keys port")
    exit()


if dawcontrolport is None:
    print("Could not find DAW Control port")
    exit()


def note_on(note, vel=127, channel=0):
    print("senidng note_on", note, vel, channel)
    dawkeysport.send(mido.Message("note_on", note=note, velocity=vel, channel=channel))


def note_off(note, channel=0):
    dawkeysport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))
