
import time
from pync import Notifier
import math
import subprocess
import sounds
from config import config
import diary_database
import speech_recognition as sr

# constant group identifier for timer notifications to replace previous alerts
TIMER_GROUP = "breakify.timer"

def countdown_timer(duration_minutes=None, update_interval=None):
    if duration_minutes is None:
        duration_minutes = config.default_duration_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval
    
    total_seconds = duration_minutes * 60
    while total_seconds > 0:
        mins, secs = divmod(math.ceil(total_seconds), 60)
        if config.show_countdown:
            Notifier.notify(f"{mins:02d}:{secs:02d} remaining", title="Breakify", group=TIMER_GROUP)
        sleep_time = min(update_interval, total_seconds)
        time.sleep(sleep_time)
        total_seconds -= sleep_time

def ask_diary_entry():
    if not config.ask_diary_entry:
        return None
        
    script = ('display dialog "Please write what you accomplished in this session:\n\n(Click Speak to use speech-to-text)" '
              'default answer "" with title "Breakify Log" buttons {"Cancel", "Speak", "OK"} default button "OK"')
    osa = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if osa.returncode == 0:
        output = osa.stdout
        if 'button returned:Speak' in output:
            # Loop for speech recognition until user does not hit Cancel
            while True:
                listen_script = 'display dialog "Listening... Please speak now." buttons {"Cancel"} default button "Cancel" giving up after 2'
                listen_proc = subprocess.Popen(["osascript", "-e", listen_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening for diary entry...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                # Close the 'Listening...' dialog
                listen_proc.terminate()
                try:
                    text = recognizer.recognize_google(audio)
                    # Show the recognized text in a dialog for confirmation
                    confirm_script = f'display dialog "Recognized: {text}\n\nClick OK to save or Cancel to try again." buttons {{"Cancel", "OK"}} default button "OK"'
                    confirm_osa = subprocess.run(["osascript", "-e", confirm_script], capture_output=True, text=True)
                    if confirm_osa.returncode == 0 and 'button returned:OK' in confirm_osa.stdout:
                        return text
                    # If Cancel, loop again for new speech
                except Exception as e:
                    error_script = f'display dialog "Sorry, could not recognize speech. Please try again. ({str(e)})" buttons {{"OK"}} default button "OK"'
                    subprocess.run(["osascript", "-e", error_script])
        elif 'button returned:OK' in output:
            for part in output.split(","):
                if part.strip().startswith("text returned:"):
                    return part.strip().split("text returned:")[1]
    return None

def start_focus_timer(duration_minutes=None, update_interval=None, callback = None):
    if duration_minutes is None:
        duration_minutes = config.default_duration_minutes
    if update_interval is None:
        update_interval = config.camera_trigger_update_interval
        
    Notifier.notify(f"Starting {duration_minutes}-minute focus session", title="Breakify", group=TIMER_GROUP)
    countdown_timer(duration_minutes=duration_minutes, update_interval=update_interval)
    callback()
    Notifier.notify(f"{duration_minutes}-minute session finished!", title="Breakify", group=TIMER_GROUP)
    entry = ask_diary_entry()
    if entry:
        diary_database.add_diary_entry(entry)

def break_notification_start(duration_minutes=None, update_interval=None, callback=None):
    if duration_minutes is None:
        duration_minutes = config.default_break_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval

    Notifier.notify(f"Starting {duration_minutes}-minute break", title="Breakify", group=TIMER_GROUP)

def break_notification_interim(total_seconds, duration_minutes=None, update_interval=None, callback=None):
    if duration_minutes is None:
        duration_minutes = config.default_break_minutes
    if update_interval is None:
        update_interval = config.countdown_update_interval

    mins, secs = divmod(math.ceil(duration_minutes - total_seconds), 60)
    Notifier.notify(f"{mins:02d}:{secs:02d} remaining in break", title="Breakify", group=TIMER_GROUP)

if __name__ == "__main__":
    ask_diary_entry()