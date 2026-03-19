import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-key'
    MAX_CONTENT_LENGTH = 256 * 1024 * 1024 * 1024

    DATABASE = os.path.join(BASE_DIR, "db.sqlite")
    VIDEO_FOLDER = os.path.join(BASE_DIR, "videos")
    HLS_FOLDER = os.path.join(BASE_DIR, "hls")
    KEY_FOLDER = os.path.join(BASE_DIR, "keys")
    THUMB_FOLDER = os.path.join(BASE_DIR, "thumbs")
    PREVIEW_FOLDER = os.path.join(BASE_DIR, "previews")
    PROTECTED_FOLDER = os.path.join(BASE_DIR, "protected")
    UPLOAD_PROFILE_FOLDER = "profiles"