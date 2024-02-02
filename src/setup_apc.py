import mido
import time


# setting up the ports

APC = "APC40 mkII"
inport, outport = None, None


def connect_ports():
    global inport, outport
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
        return False

    else:
        enter_ableton_mode()
        return True


# Refer to "Outbound Message Type 0: Introduction" of the APC40 mkII Communication Protocol


class Mode:
    GENERIC = 0x40
    ABLETON = 0x41
    ABLETON_ALT = 0x42


def enter_ableton_mode():
    outport.send(
        mido.Message(
            "sysex",
            data=[0x47, 0x7F, 0x29, 0x60, 0x00, 0x04, Mode.ABLETON, 0x08, 0x02, 0x01],
        )
    )


# used to init apc from other modules

on_connect_callbacks = []


def on_apc_connect(callback):
    on_connect_callbacks.append(callback)


def fire_apc_connect_callbacks():
    for callback in on_connect_callbacks:
        callback()


# handling apc connects and disconnects

def apc_connected():
    return inport.name in mido.get_input_names()


def wait_till_apc_disconnects():
    global inport, outport
    while apc_connected():
        time.sleep(1)

    # clear callbacks and ports on disconnect
    inport.callback = None
    outport.callback = None
    inport = None
    outport = None


# try connecting to apc periodically
# if successfully connected, init the apc, and listen for messages until apc disconnects

def listen_for_apc_messages(handle_message):
    while True:
        if connect_ports():
            fire_apc_connect_callbacks()
            inport.callback = handle_message
            wait_till_apc_disconnects()

        time.sleep(1)
