import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ARCHIVE_FOLDER = os.path.join(BASE_DIR, "archived_docs")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

DATABASE_PATH = os.path.join(BASE_DIR, "database", "iasw.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)