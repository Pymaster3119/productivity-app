import configparser
import os

class Config:
    def __init__(self, config_file='appsetings.cfg'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
    
    # Timer settings
    @property
    def default_duration_minutes(self):
        return self.config.getfloat('Timer', 'default_duration_minutes', fallback=30)
    
    @property
    def default_break_minutes(self):
        return self.config.getfloat('Timer', 'default_break_minutes', fallback=5)
    
    @property
    def camera_trigger_update_interval(self):
        return self.config.getint('Timer', 'camera_trigger_update_interval', fallback=1)
    
    # AI Detection settings
    @property
    def confidence_threshold(self):
        return self.config.getfloat('AI_Detection', 'confidence_threshold', fallback=0.75)
    
    @property
    def nms_confidence_threshold(self):
        return self.config.getfloat('AI_Detection', 'nms_confidence_threshold', fallback=0.5)
    
    @property
    def nms_iou_threshold(self):
        return self.config.getfloat('AI_Detection', 'nms_iou_threshold', fallback=0.4)
    
    @property
    def input_width(self):
        return self.config.getint('AI_Detection', 'input_width', fallback=416)
    
    @property
    def input_height(self):
        return self.config.getint('AI_Detection', 'input_height', fallback=416)
    
    @property
    def scale_factor(self):
        return self.config.getfloat('AI_Detection', 'scale_factor', fallback=1/255.0)
    
    # Audio settings
    @property
    def alarm_sound_file(self):
        return self.config.get('Audio', 'alarm_sound_file', fallback='BEEPING_NOISE_ALARM_CLOCK_Iw5.wav')
    
    # Notification settings
    @property
    def show_countdown(self):
        return self.config.getboolean('Notifications', 'show_countdown', fallback=True)
    
    @property
    def countdown_update_interval(self):
        return self.config.getint('Notifications', 'countdown_update_interval', fallback=60)
    
    @property
    def ask_diary_entry(self):
        return self.config.getboolean('Notifications', 'ask_diary_entry', fallback=True)
    
    @property
    def clickup_token(self):
        return self.config.get('Clickup', 'token', fallback=None)

# Create a global config instance
config = Config()
