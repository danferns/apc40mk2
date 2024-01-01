from apc_leds import clear_leds
from apc_matrix import is_matrix, matrix_handler
from param import is_param_update, update_param
from setup_apc import inport
# from transport import is_transport, transport_handler


def init():
    clear_leds()
    # for i in range(0, 40):  # uncomment to view color palette
    #     led_on(i, color_palette(i), Beat.CONSTANT)
    # return


event_listeners = [
    {"check": is_matrix, "action": matrix_handler},
    {"check": is_param_update, "action": update_param},
    # {"check": is_transport, "action": transport_handler},
]


init()

for msg in inport:
    print(msg)
    for listener in event_listeners:
        if listener["check"](msg):
            listener["action"](msg)
            break
