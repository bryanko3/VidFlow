from flask import Blueprint, render_template, session, redirect, request
import os
from werkzeug.utils import secure_filename

from config import Config
from core.database import connect

from models.user_model import get_user, update_user_bio
from models.video_model import get_user_videos, get_total_likes_by_user
from models.subscribe_model import get_subscribers, get_subscribed_channels, is_subscribed
from models.like_model import get_liked_videos_by_user

profile_routes = Blueprint("profile", __name__)


@profile_routes.route("/profile")
def profile():

    user_id = session.get("user")
    sort = request.args.get("sort", "latest")

    if not user_id:
        return redirect("/login")

    user = get_user(user_id)

    videos = get_user_videos(user_id, sort)

    subscribers = get_subscribers(user_id)

    total_likes = get_total_likes_by_user(user_id)

    liked_videos = get_liked_videos_by_user(user_id)

    subscribed_channels = get_subscribed_channels(user_id)

    return render_template(
        "profile.html",
        user=user,
        videos=videos,
        sort=sort,
        subscribers=subscribers,
        total_likes=total_likes,
        liked_videos=liked_videos,
        subscribed_channels=subscribed_channels
    )


@profile_routes.route("/channel/<int:user_id>")
def channel(user_id):

    user = get_user(user_id)

    videos = get_user_videos(user_id)

    subscribers = get_subscribers(user_id)

    total_likes = get_total_likes_by_user(user_id)

    subscribed = False

    if "user" in session:
        subscribed = is_subscribed(session["user"], user_id)

    return render_template(
        "channel.html",
        user=user,
        videos=videos,
        subscribers=subscribers,
        total_likes=total_likes,
        subscribed=subscribed
    )

@profile_routes.route("/profile/update_bio", methods=["POST"])
def update_bio():

    if "user" not in session:
        return redirect("/login")

    bio_text = request.form.get("bio", "").strip()
    user_id = session["user"]

    update_user_bio(user_id, bio_text)

    return redirect("/profile")

@profile_routes.route("/profile/update_image", methods=["POST"])
def update_image():

    if "user" not in session:
        return redirect("/login")

    file = request.files.get("profile_image")

    if file and file.filename != "":

        filename = secure_filename(file.filename)

        filename = f"{session['user']}_{filename}"

        path = os.path.join(Config.UPLOAD_PROFILE_FOLDER, filename)

        file.save(path)

        db = connect()
        c = db.cursor()

        c.execute("""
        UPDATE users
        SET profile_image=?
        WHERE id=?
        """, (filename, session["user"]))

        db.commit()
        db.close()

        session["profile_image"] = filename

    return redirect("/profile")

@profile_routes.route("/profile/delete_image", methods=["POST"])
def delete_image():

    if "user" not in session:
        return redirect("/login")

    db = connect()
    c = db.cursor()

    c.execute("""
    UPDATE users
    SET profile_image=NULL
    WHERE id=?
    """, (session["user"],))

    db.commit()
    db.close()

    session["profile_image"] = None

    return redirect("/profile")

@profile_routes.route("/profile/update_status", methods=["POST"])
def update_status():

    if "user" not in session:
        return redirect("/login")

    status = request.form.get("status")

    if status not in ["public","private"]:
        return redirect("/profile")

    db = connect()
    c = db.cursor()

    c.execute("""
    UPDATE users
    SET profile_status=?
    WHERE id=?
    """,(status, session["user"]))

    db.commit()
    db.close()

    return redirect("/profile")