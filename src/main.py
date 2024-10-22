from apc_leds import clear_leds, display_color_palette  # noqa: F401
from apc_matrix import is_matrix, matrix_handler
from device_control import device_control_handler, is_device_control
from param import is_param_update, update_param
from setup_apc import listen_for_apc_messages, on_apc_connect
from transport import is_transport, transport_handler
from windows import is_windows_message, windows_handler


def handle_message(msg):
    print(msg)
    if is_matrix(msg):
        matrix_handler(msg)
    elif is_param_update(msg):
        update_param(msg)
    elif is_transport(msg):
        transport_handler(msg)
    elif is_device_control(msg):
        device_control_handler(msg)
    elif is_windows_message(msg):
        windows_handler(msg)


on_apc_connect(clear_leds)
listen_for_apc_messages(handle_message)
