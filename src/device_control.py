from setup_daw import dawcontrolport
from setup_apc import outport


def is_device_control(msg):
    is_channel_0 = msg.channel == 0
    is_device_knob = msg.type == "control_change" and msg.control in range(16, 24)
    is_device_button = msg.type == "note_on" and msg.note in range(58, 66)
    return is_channel_0 and (is_device_knob or is_device_button)

# store the on/off states of buttons to make them toggleable
button_states = [False] * 8


def get_button_index(msg):
    return msg.note - 58


def device_control_handler(msg):
    if msg.type == "control_change":
        dawcontrolport.send(msg)
    elif msg.type == "note_on":
        button = get_button_index(msg)
        if button_states[button]:
            dawcontrolport.send(msg.copy(note=button + 58, velocity=0))
            outport.send(msg.copy(note=button + 58, velocity=0))
            button_states[button] = False
        else:
            dawcontrolport.send(msg)
            outport.send(msg)
            button_states[button] = True
