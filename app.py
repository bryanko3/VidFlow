from flask import Flask, send_from_directory
import os

from config import Config
from core.database import init_db

from routes.auth_routes import auth_routes
from routes.video_routes import video_routes
from routes.search_routes import search_routes
from routes.comment_routes import comment_routes
from routes.like_routes import like_routes
from routes.subscribe_routes import subscribe_routes
from routes.profile_routes import profile_routes

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

from core.database import connect

@app.context_processor
def inject_categories():

    db = connect()

    categories = db.execute("SELECT * FROM categories").fetchall()

    db.close()

    return dict(categories=categories)

app.register_blueprint(auth_routes)
app.register_blueprint(video_routes)
app.register_blueprint(search_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(like_routes)
app.register_blueprint(subscribe_routes)
app.register_blueprint(profile_routes)

# @app.route("/videos/<filename>")
# def videos(filename):
#     return send_from_directory(Config.VIDEO_FOLDER, filename)

@app.route("/thumbs/<filename>")
def thumbs(filename):
    return send_from_directory(Config.THUMB_FOLDER, filename)

@app.route("/previews/<filename>")
def previews(filename):
    return send_from_directory(Config.PREVIEW_FOLDER, filename)

@app.route("/profiles/<filename>")
def profiles(filename):
    return send_from_directory(Config.UPLOAD_PROFILE_FOLDER, filename)

if __name__ == "__main__":

    init_db()

    os.makedirs(Config.VIDEO_FOLDER, exist_ok=True)
    os.makedirs(Config.THUMB_FOLDER, exist_ok=True)
    os.makedirs(Config.PREVIEW_FOLDER, exist_ok=True)
    os.makedirs(Config.UPLOAD_PROFILE_FOLDER, exist_ok=True)
    os.makedirs(Config.PROTECTED_FOLDER, exist_ok=True)
    os.makedirs(Config.HLS_FOLDER, exist_ok=True)
    os.makedirs(Config.KEY_FOLDER, exist_ok=True)

    app.run(host="0.0.0.0", port=5000, debug=True)