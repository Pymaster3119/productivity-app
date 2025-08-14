import os
import subprocess
from config import config
sound_process = None

def start_sound():
    global sound_process
    stop_sound()
    sound_file = config.alarm_sound_file
    cmd = ['ffplay', '-loop', '-1', '-nodisp', '-autoexit', sound_file]
    sound_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Playing focus sound: {sound_file} (using ffplay)")

def stop_sound():
    global sound_process

    if sound_process:
        sound_process.terminate()
        sound_process.wait(timeout=2.0)
        sound_process = None