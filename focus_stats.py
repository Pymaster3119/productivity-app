# Tracks total focus and break time in seconds
import json
import os

STATS_FILE = 'focus_stats.json'

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {'focus_seconds': 0, 'break_seconds': 0}
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def add_focus_time(seconds):
    stats = load_stats()
    stats['focus_seconds'] += seconds
    save_stats(stats)

def add_break_time(seconds):
    stats = load_stats()
    stats['break_seconds'] += seconds
    save_stats(stats)

def get_stats():
    return load_stats()
