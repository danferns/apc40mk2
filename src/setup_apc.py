import mido


# setting up the ports

APC = "APC40 mkII"
inport, outport = None, None


for port in mido.get_input_names():
    if APC in port:
        inport = mido.open_input(port)
        print("Opened input port: " + port)
        break


for port in mido.get_output_names():
    if APC in port:
        outport = mido.open_output(port)
        print("Opened output port: " + port)
        break


if inport is None or outport is None:
    print("Could not find APC40 mkII")
    exit()


# enter ableton mode


class Mode:
    GENERIC = 0x40
    ABLETON = 0x41
    ABLETON_ALT = 0x42


# Refer to "Outbound Message Type 0: Introduction" of the APC40 mkII Communication Protocol

outport.send(
    mido.Message(
        "sysex",
        data=[0x47, 0x7F, 0x29, 0x60, 0x00, 0x04, Mode.ABLETON, 0x08, 0x02, 0x01],
    )
)
