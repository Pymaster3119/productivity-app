from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import configparser
from config import config
import diary_database
from flask import send_from_directory
import focus_stats

app = Flask(__name__)

@app.route('/api/focus_stats')
def api_focus_stats():
    stats = focus_stats.get_stats()
    return jsonify(stats)

@app.route('/')
def index():
    """Serve the index.html file with current config values and diary entries"""
    # Fetch diary entries from the database
    try:
        entries = diary_database.get_all_entries()  # Should return a list of dicts with 'date' and 'text'
    except Exception:
        entries = []
    return render_template('index.html', config=config, diary_entries=entries)

@app.route('/update-config', methods=['POST'])
def update_config():
    """Update the configuration file with form data"""
    try:
        # Load the current config file
        config_parser = configparser.ConfigParser()
        config_file = 'appsetings.cfg'
        if os.path.exists(config_file):
            config_parser.read(config_file)
        sections = ['Timer', 'AI_Detection', 'Audio', 'Notifications']
        for section in sections:
            if not config_parser.has_section(section):
                config_parser.add_section(section)
        
        # Update Timer settings
        config_parser.set('Timer', 'default_duration_minutes', str(request.form.get('default_duration_minutes', 30)))
        config_parser.set('AI_Detection', 'confidence_threshold', str(request.form.get('confidence_threshold', 0.8)))
        config_parser.set('AI_Detection', 'nms_confidence_threshold', str(request.form.get('nms_confidence_threshold', 0.5)))
        config_parser.set('AI_Detection', 'nms_iou_threshold', str(request.form.get('nms_iou_threshold', 0.4)))
        config_parser.set('AI_Detection', 'input_width', str(request.form.get('input_width', 320)))
        config_parser.set('AI_Detection', 'input_height', str(request.form.get('input_height', 320)))
        config_parser.set('AI_Detection', 'scale_factor', str(1/255.0))  # Keep this constant
        config_parser.set('Audio', 'alarm_sound_file', str(request.form.get('alarm_sound_file', 'BEEPING_NOISE_ALARM_CLOCK_Iw5.wav')))
        show_countdown = 'show_countdown' in request.form
        ask_diary_entry = 'ask_diary_entry' in request.form
        config_parser.set('Notifications', 'show_countdown', str(show_countdown).lower())
        config_parser.set('Notifications', 'countdown_update_interval', str(request.form.get('countdown_update_interval', 1)))
        config_parser.set('Notifications', 'ask_diary_entry', str(ask_diary_entry).lower())
        
        # Write the updated configuration back to the file & Reload
        with open(config_file, 'w') as f:
            config_parser.write(f)
        config.load_config()
        
        # After update, also show diary entries
        try:
            entries = diary_database.get_all_entries()
        except Exception:
            entries = []
        return render_template('index.html', config=config, diary_entries=entries, message="Configuration updated successfully!", message_type="success")
    except Exception as e:
        try:
            entries = diary_database.get_all_entries()
        except Exception:
            entries = []
        return render_template('index.html', config=config, diary_entries=entries, message=f"Error updating configuration: {str(e)}", message_type="error")

@app.route('/static/styles.css')
def serve_static_css():
    return send_from_directory('templates', 'styles.css')
if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)