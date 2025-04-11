import json
import logging
from pathlib import Path
from datetime import datetime

class Tools():
    def __init__(self):
        self.logging = self.load_config("logging","info")

    def load_config(self, key, fallback_value):
        try:
            script_dir = Path(__file__).resolve().parent 
            config_path = script_dir / "config.json"
            with config_path.open("r") as config_file:
                config_data = json.load(config_file)
                return config_data.get(key, fallback_value)
        except Exception as e:
            self.printandlog(f"Caught exception on load_config {key}: {e}", "warning")
            return False 

    def printandlog(self, msg, lvl="info"):
        try:
            script_dir = Path(__file__).resolve().parent 
            log_dir = script_dir / "log"
            log_dir.mkdir(parents=True, exist_ok=True) 
            log_file = log_dir / "sortingHat.log"
            logging.basicConfig(filename=log_file, level=logging.INFO)
            now = datetime.now()
            fullmsg = f"{now}   {lvl}: {msg}"
            logmsg = f"{now}   {msg}"
            print(fullmsg)
            if self.logging == "true":
                if lvl == "info":
                    logging.info(logmsg)
                elif lvl == "warning":
                    logging.warning(logmsg)
                elif lvl == "separator":
                    logging.info(f"----> {logmsg}")
            return True
        except Exception as e:
            print(f"Error in printandlog: {e}")
            return False  


