from flask import Blueprint, session, jsonify
from models.like_model import toggle_like, get_like_count

like_routes = Blueprint("likes", __name__)

@like_routes.route("/like/<int:video_id>", methods=["POST"])
def like(video_id):
    if "user" not in session:
        return jsonify({"error":"You must be logged in"}), 403

    user_id = session["user"]
    liked = toggle_like(video_id, user_id)  # True면 좋아요, False면 취소
    total = get_like_count(video_id)

    return jsonify({"likes": total, "liked": liked})