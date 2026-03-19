from flask import Blueprint, session, redirect, jsonify
from models.subscribe_model import toggle_subscription

subscribe_routes = Blueprint("subscribe", __name__)

@subscribe_routes.route("/subscribe/<int:channel_id>")
def subscribe(channel_id):

    if "user" not in session:
        return redirect("/login")

    if session["user"] == channel_id:
        return jsonify({"status": "self"})

    subscribed = toggle_subscription(session["user"], channel_id)

    return jsonify({
        "subscribed": subscribed
    })