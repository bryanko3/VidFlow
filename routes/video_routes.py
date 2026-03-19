from flask import Blueprint, render_template, request, redirect, session, send_file, send_from_directory, abort
import os

from models.video_model import create_video, get_video, increase_views, delete_video, get_user_videos, get_total_likes_by_user
from models.user_model import get_user
from services.video_service import create_thumbnail
from models.comment_model import get_comments
from models.like_model import get_like_count, user_liked
from core.utils import generate_filename
from core.database import connect
from services.video_watermark_service import create_protected_video
from services.hls_service import create_hls

from config import Config

video_routes = Blueprint("video", __name__)


@video_routes.route("/")
def index():

    db = connect()

    category_param = request.args.get("categories", "")
    search_q = request.args.get("q", "")

    if category_param:
        category_ids = [int(x) for x in category_param.split(",")]
    else:
        category_ids = []

    query = """
        SELECT videos.*, users.username, categories.name as category,
               COUNT(likes.id) as likes
        FROM videos
        JOIN users ON users.id = videos.user_id
        LEFT JOIN categories ON categories.id = videos.category_id
        LEFT JOIN likes ON likes.video_id = videos.id
    """

    conditions = []
    params = []

    if search_q:
        conditions.append("videos.title LIKE ?")
        params.append(f"%{search_q}%")

    if category_ids:
        placeholders = ",".join("?" for _ in category_ids)
        conditions.append(f"videos.category_id IN ({placeholders})")
        params.extend(category_ids)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY videos.id ORDER BY videos.created_at DESC"

    videos = db.execute(query, params).fetchall()

    categories = db.execute("SELECT * FROM categories").fetchall()

    db.close()

    return render_template("index.html", videos=videos, categories=categories)


@video_routes.route("/watch/<int:video_id>")
def watch(video_id):

    video = get_video(video_id)

    if not video:
        return "Video not found", 404

    comments = get_comments(video_id)

    increase_views(video_id)

    uploader = get_user(video["user_id"])

    uploader_videos = get_user_videos(video["user_id"])
    uploader_videos = [v for v in uploader_videos if v["id"] != video_id]

    return render_template(
        "watch.html",
        video=video,
        comments=comments,
        get_like_count=get_like_count,
        user_liked=user_liked,
        uploader=uploader,
        uploader_videos=uploader_videos
    )


@video_routes.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect("/login")

    db = connect()

    if request.method == "POST":

        file = request.files.get("video")
        thumb_file = request.files.get("thumbnail")
        if not file:
            return "No file uploaded", 400

        title = request.form.get("title")
        description = request.form.get("description", "")
        category_id = request.form.get("category_id")

        if not category_id:
            return "Category required", 400

        filename = generate_filename(file.filename)

        thumb_filename = None

        if thumb_file and thumb_file.filename != "":

            ext = thumb_file.filename.lower().split(".")[-1]

            if ext in ["jpg","jpeg","png"]:

                thumb_filename = f"{filename}.jpg"

                thumb_path = os.path.join(Config.THUMB_FOLDER, thumb_filename)

                thumb_file.save(thumb_path)
                
        save_path = os.path.join(Config.VIDEO_FOLDER, filename)
        file.save(save_path)

        if not thumb_filename:
            create_thumbnail(save_path, filename)

        create_video(
            session["user"],
            title,
            filename,
            category_id,
            description,
            thumb_filename
        )

        user = get_user(session["user"])
        if not user:
            return "Invalid user session", 400

        protected_path = os.path.join(Config.PROTECTED_FOLDER, filename)
        create_protected_video(
            save_path,
            protected_path,
            user["username"],
            "static/watermark.png"
        )

        hls_output = os.path.join(Config.HLS_FOLDER, f"{session['user']}_{filename}")
        create_hls(save_path, hls_output)

        return redirect("/")

    categories = db.execute("SELECT * FROM categories").fetchall()
    return render_template("upload.html", categories=categories)


@video_routes.route("/stream/<int:video_id>")
def stream(video_id):
    if "user" not in session:
        abort(403)

    video = get_video(video_id)
    if not video:
        return "Video not found", 404

    video_path = os.path.join(Config.VIDEO_FOLDER, video["filename"])
    if not os.path.exists(video_path):
        return "Video file missing", 404

    return send_file(
        video_path,
        mimetype="video/mp4",
        conditional=True
    )

@video_routes.route("/hls/<path:filename>")
def hls_stream(filename):
    if "user" not in session:
        abort(403)

    return send_from_directory(Config.HLS_FOLDER, filename)

    # ref = request.headers.get("Referer", "")
    # if f"/watch/" not in ref:
    #     abort(403)

    # key_path = os.path.join(Config.HLS_FOLDER, folder, "enc.key")
    # if not os.path.exists(key_path):
    #     abort(404)

    # return send_file(key_path, mimetype="application/octet-stream")


@video_routes.route("/delete/<int:video_id>", methods=["POST"])
def delete(video_id):

    if "user" not in session:
        return redirect("/login")

    delete_video(video_id, session["user"])

    return redirect("/profile")


@video_routes.route("/channel/<int:user_id>")
def channel(user_id):

    db = connect()

    user = get_user(user_id)

    sort = request.args.get("sort", "latest")

    videos = get_user_videos(user_id, sort=sort)

    subscribers = db.execute(
        "SELECT COUNT(*) FROM subscriptions WHERE channel_id=?",
        (user_id,)
    ).fetchone()[0]

    total_likes = get_total_likes_by_user(user_id)

    db.close()

    return render_template(
        "channel.html",
        user=user,
        videos=videos,
        subscribers=subscribers,
        total_likes=total_likes
    )

@video_routes.route("/key/<filename>")
def hls_key(filename):

    if "user" not in session:
        abort(403)

    return send_from_directory(Config.KEY_FOLDER, filename)