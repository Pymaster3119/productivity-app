# Breakify

## 1. Overview
The Productivity App is a desktop application designed to help users manage their time, focus, and daily activities more efficiently. It combines features like a diary, focus statistics, alarm clock, and object detection to create a holistic productivity environment.

## 2. Purpose
The app aims to:
- Enhance user productivity by tracking focus sessions.
- Provide a digital diary for daily reflections.
- Offer reminders and alarms to maintain schedules.
- Use computer vision for object detection (e.g., for focus monitoring).

## 3. Target Audience
- Students seeking better study habits.
- Professionals aiming to optimize work sessions.
- Anyone interested in self-improvement and productivity tracking.

## 4. Main Features
- **Focus Timer & Stats:** Track and analyze focus sessions.
- **Diary:** Write and store daily entries securely.
- **Alarm Clock:** Set alarms with custom sounds.
- **Object Detection:** Uses YOLOv4 for real-time camera-based detection.
- **Menubar Integration:** Quick access to features from the system menubar.

## 5. Technical Overview
- **Language:** Python 3.10+
- **Database:** SQLite (`diary.db`)
- **Computer Vision:** YOLOv4 (with pre-trained weights)
- **UI:** Menubar-based (likely using PyObjC, PyQt, or Tkinter)
- **Audio:** Custom alarm sounds

## 6. Installation Guide
### Prerequisites
- Python 3.10 or newer
- pip (Python package manager)
- macOS

### Steps
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Productivity\ App
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```sh
   pip install opencv-python numpy flask pyobjc pyqt5
   ```
3. **Download YOLO Weights:**
   Ensure `yolov4.weights`, `yolov4-tiny.weights`, and config files are present in the root directory. If not, they will be automatically downloaded

4. **Initialize the database:**
   ```sh
   python init_db.py
   ```

5. **Run the application:**
   ```sh
   python menubar.py
   ```

## 7. Configuration
- **appsettings.cfg:** Main configuration file for app settings (edit as needed).
- **focus_stats.json:** Stores focus session data.
- **diary.db:** SQLite database for diary entries.
- **config.py:** Contains application constants and configuration logic.

## 8. Usage Guide
- **Menubar:** Launches app features from the system menubar.
- **Diary:** Add/view entries via the UI or command line.
- **Focus Timer:** Start/stop focus sessions; stats are saved automatically.
- **Alarm:** Set alarms; custom sound (`BEEPING_NOISE_ALARM_CLOCK_Iw5.wav`) will play.
- **Object Detection:** Use `scancamera.py` to start camera-based detection.

## 9. File Reference
- `menubar.py`: Main entry point; handles UI and feature integration.
- `diary_database.py`: Diary CRUD operations and DB logic.
- `focus_stats.py`: Focus session tracking and stats.
- `sounds.py`: Audio playback for alarms.
- `scancamera.py`: Camera and object detection logic.
- `config.py`: App configuration and constants.
- `init_db.py`: Initializes the SQLite database.
- `runserver.py`: (If present) Flask server for web-based features.
- `templates/`: HTML/CSS for the web UI.
- `*.cfg`, `*.weights`, `*.names`: Model and app configuration files.