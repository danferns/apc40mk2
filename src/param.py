import mido
from setup_apc import outport

params = {
    "velocity": 64,
    "chord-center": 64,
    "strum": 0,
}

# order of knobs above the matrix
param_knobs = ["velocity", "chord-center", "strum"]


def message_to_knob(msg):
    return msg.control - 48


def knob_to_param(knob):
    return param_knobs[knob]


def is_param_update(msg):
    return (
        msg.type == "control_change"
        and msg.channel == 0
        and msg.control in range(48, 56)
    )


def update_param(msg):
    knob = message_to_knob(msg)
    if is_param_update(msg) and knob < len(param_knobs):
        params[knob_to_param(knob)] = msg.value


for i, param in enumerate(param_knobs):
    outport.send(
        mido.Message("control_change", channel=0, control=i + 48, value=params[param])
    )
