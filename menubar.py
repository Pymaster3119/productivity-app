import time
from pync import Notifier
import subprocess

def ask_diary_entry():
    script = 'display dialog "Please write what you accomplished in this session:" default answer "" with title "Workify Log"'
    osa = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if osa.returncode == 0:
        for part in osa.stdout.split(","):
            if part.strip().startswith("text returned:"):
                return part.strip().split("text returned:")[1]
    return None

def start_focus_timer():
    Notifier.notify("30-minute session finished!", title="Workify")
    entry = ask_diary_entry()
    if entry:
        print(entry)

if __name__ == "__main__":
    start_focus_timer()