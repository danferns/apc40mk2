params = {
    "velocity": 127,
}

param_knobs = {  # channel: { control: param }
    0: {
        48: "velocity",
    }
}


def is_param_update(msg):
    return (
        msg.type == "control_change"
        and msg.channel in param_knobs
        and msg.control in param_knobs[msg.channel]
    )


def update_param(msg):
    if is_param_update(msg):
        params[param_knobs[msg.channel][msg.control]] = msg.value
