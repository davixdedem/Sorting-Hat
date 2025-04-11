import os
import time
import threading
from tools import Tools
from player import Player
from motion import Motion
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

ALLOWED_IPS = {
    '127.0.0.1',
    '192.168.50.6'
}

tools = Tools()
player = Player()
motion = Motion()

TRACKS_DIR = "tracks"  
lock = threading.Lock()
is_playing = False  

def is_allowed(ip):
    return ip in ALLOWED_IPS

@app.before_request
def limit_remote_addr():
    ip = request.remote_addr
    if not is_allowed(ip):
        tools.printandlog(f"Access denied for IP: {ip}")
        abort(403)

def activate_motion_for_duration(duration):
    global is_playing  
    tools.printandlog(f"Motion ON for {duration:.2f} seconds")
    motion.on()
    is_playing = True  
    time.sleep(duration)
    motion.off()
    is_playing = False 
    tools.printandlog("Motion OFF")

@app.route('/api/play_track', methods=['POST'])
def play_track():
    global is_playing 
    if is_playing:
        return jsonify({"status": "error", "message": "Another track is currently being played. Please wait."}), 400
    data = request.get_json()
    if not data or 'track_id' not in data:
        return jsonify({"status": "error", "message": "Missing 'track_id' in request"}), 400
    track_id = str(data['track_id'])
    speech_time = data.get('speech_time')
    audio_path = os.path.join(TRACKS_DIR, f"{track_id}.wav")
    if not os.path.isfile(audio_path):
        return jsonify({"status": "error", "message": f"Unknown track id: {track_id}"}), 404
    try:
        with lock:
            if is_playing:
                return jsonify({"status": "error", "message": "Another track is currently being played. Please wait."}), 400
            is_playing = True  
            duration = float(speech_time) if speech_time else player.get_wav_duration(audio_path)
            threading.Thread(target=activate_motion_for_duration, args=(duration,)).start()
            result = player.play_wav(path=audio_path)
        return jsonify({"status": "ok", "message": result}), 200
    except Exception as e:
        tools.printandlog(f"Error playing track: {e}")
        is_playing = False  
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
