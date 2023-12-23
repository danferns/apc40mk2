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

