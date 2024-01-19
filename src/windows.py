import os
import math
import threading

VOLUME_INCREMENT = math.floor(65535 / 100)

def is_windows_message(msg):
    if (msg.type == "control_change" and msg.channel == 0 and msg.control == 47):
        return True

def control_volume(value):
        if (value >= 64):
            # volume down
            os.system(f"nircmd.exe changesysvolume -{VOLUME_INCREMENT * (128 - value)}")           
        elif (value < 64):
            # volume up
            os.system(f"nircmd.exe changesysvolume {VOLUME_INCREMENT * (value)}")


def windows_handler(msg):
    if (msg.type == "control_change" and msg.channel == 0 and msg.control == 47):
        thread = threading.Thread(target=control_volume, args=(msg.value,))
        thread.start()