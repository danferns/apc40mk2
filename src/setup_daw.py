import mido

DAW = "FL Studio"
dawport = None

for port in mido.get_output_names():
    if DAW in port:
        dawport = mido.open_output(port)
        print("Opened output port: " + port)
        break


if dawport is None:
    print("Could not find FL Studio")
    exit()


def note_on(note, vel=127, channel=0):
    dawport.send(mido.Message("note_on", note=note, velocity=vel, channel=channel))


def note_off(note, channel=0):
    dawport.send(mido.Message("note_off", note=note, velocity=0, channel=channel))
