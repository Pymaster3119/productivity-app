import time
from pync import Notifier
import math
import subprocess
import sounds
from config import config
import diary_database

# constant group identifier for timer notifications to replace previous alerts
TIMER_GROUP = "workify.timer"

def countdown_timer(duration_minutes=None, update_interval=None):
    if duration_minutes is None:
        duration_minutes = config.default_duration_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval
    
    total_seconds = duration_minutes * 60
    while total_seconds > 0:
        mins, secs = divmod(math.ceil(total_seconds), 60)
        if config.show_countdown:
            Notifier.notify(f"{mins:02d}:{secs:02d} remaining", title="Workify", group=TIMER_GROUP)
        sleep_time = min(update_interval, total_seconds)
        time.sleep(sleep_time)
        total_seconds -= sleep_time

def ask_diary_entry():
    if not config.ask_diary_entry:
        return None
        
    script = 'display dialog "Please write what you accomplished in this session:" default answer "" with title "Workify Log"'
    osa = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if osa.returncode == 0:
        for part in osa.stdout.split(","):
            if part.strip().startswith("text returned:"):
                return part.strip().split("text returned:")[1]
    return None

def start_focus_timer(duration_minutes=None, update_interval=None, callback = None):
    if duration_minutes is None:
        duration_minutes = config.default_duration_minutes
    if update_interval is None:
        update_interval = config.camera_trigger_update_interval
        
    Notifier.notify(f"Starting {duration_minutes}-minute focus session", title="Workify", group=TIMER_GROUP)
    countdown_timer(duration_minutes=duration_minutes, update_interval=update_interval)
    callback()
    Notifier.notify(f"{duration_minutes}-minute session finished!", title="Workify", group=TIMER_GROUP)
    entry = ask_diary_entry()
    if entry:
        diary_database.add_diary_entry(entry)

def break_notification_start(duration_minutes=None, update_interval=None, callback=None):
    if duration_minutes is None:
        duration_minutes = config.default_break_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval

    Notifier.notify(f"Starting {duration_minutes}-minute break", title="Workify", group=TIMER_GROUP)

def break_notification_interim(total_seconds, duration_minutes=None, update_interval=None, callback=None):
    if duration_minutes is None:
        duration_minutes = config.default_break_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval

    mins, secs = divmod(math.ceil(duration_minutes - total_seconds), 60)
    Notifier.notify(f"{mins:02d}:{secs:02d} remaining in break", title="Workify", group=TIMER_GROUP)
