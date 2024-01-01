params = {
    "velocity": 127,
    "center": 64,
}

# order of knobs above the matrix
param_knobs = ["velocity"]

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
