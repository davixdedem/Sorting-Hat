        
import os
import wave
import subprocess
from tools import Tools

class Player():
    
    def __init__(self):
        self.tools = Tools()

    def play_wav(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        try:
            subprocess.Popen(['aplay', path])
            self.tools.printandlog(f"Playing audio: {path}")
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")  

    def get_wav_duration(self, path):
        try:
            with wave.open(path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                framerate = wav_file.getframerate()
                duration = frames / float(framerate)
                self.tools.printandlog(f"Audio duration: {duration}")
                return duration
        except Exception as e:
            self.tools.printandlog(f"Error reading wav duration: {e}")
            return 0              
