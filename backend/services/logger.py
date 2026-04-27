import os
from datetime import datetime
from config import LOG_FOLDER

LOG_FILE = os.path.join(LOG_FOLDER, "audit.log")

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")