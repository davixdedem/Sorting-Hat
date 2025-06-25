        
import os
import wave
import subprocess
from tools import Tools

class Player():
    
    def __init__(self):
        self.tools = Tools()

    def play_audio(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        try:
            # Use aplay for WAV files and mpg123 for MP3 files
            if path.lower().endswith('.wav'):
                subprocess.Popen(['aplay', path])
            elif path.lower().endswith('.mp3'):
                subprocess.Popen(['mpg123', path])
            else:
                raise RuntimeError(f"Unsupported audio format: {path}")
            self.tools.printandlog(f"Playing audio: {path}")
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")

    # Keep the old method for backward compatibility
    def play_wav(self, path):
        return self.play_audio(path)

    def get_audio_duration(self, path):
        try:
            if path.lower().endswith('.wav'):
                return self.get_wav_duration(path)
            elif path.lower().endswith('.mp3'):
                return self.get_mp3_duration(path)
            else:
                self.tools.printandlog(f"Unsupported audio format for duration detection: {path}")
                return 0
        except Exception as e:
            self.tools.printandlog(f"Error reading audio duration: {e}")
            return 0

    def get_wav_duration(self, path):
        try:
            with wave.open(path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                framerate = wav_file.getframerate()
                duration = frames / float(framerate)
                self.tools.printandlog(f"WAV duration: {duration}")
                return duration
        except Exception as e:
            self.tools.printandlog(f"Error reading wav duration: {e}")
            return 0

    def play_mp3(self, path):
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
                check=True
            )
            return f"Played MP3: {path}"
        except subprocess.CalledProcessError as e:
            self.tools.printandlog(f"Error playing mp3: {e}")
            return f"Error playing MP3: {e}"
        
    def get_mp3_duration(self, path):
        try:
            result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                                   '-of', 'csv=p=0', path], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                self.tools.printandlog(f"MP3 duration: {duration}")
                return duration
            else:
                self.tools.printandlog(f"Error getting MP3 duration: {result.stderr}")
                return 0
        except Exception as e:
            self.tools.printandlog(f"Error reading mp3 duration: {e}")
            return 0              
