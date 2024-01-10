from apc_leds import clear_leds, display_color_palette  # noqa: F401
from apc_matrix import is_matrix, matrix_handler
from device_control import device_control_handler, is_device_control
from param import is_param_update, update_param
from setup_apc import inport
from transport import is_transport, transport_handler

from threading import Thread


clear_leds()
# display_color_palette()


def handle_message(msg):
    if is_matrix(msg):
        matrix_handler(msg)
    elif is_param_update(msg):
        update_param(msg)
    elif is_transport(msg):
        transport_handler(msg)
    elif is_device_control(msg):
        device_control_handler(msg)


for msg in inport:
    print(msg)
    message_thread = Thread(target=handle_message, args=(msg,))
    message_thread.start()
