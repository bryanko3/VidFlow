from flask import Blueprint,request,redirect,session

from models.comment_model import add_comment,delete_comment

comment_routes = Blueprint("comments",__name__)

@comment_routes.route("/comment/<int:video_id>",methods=["POST"])
def comment(video_id):

    if "user" not in session:
        return redirect("/login")

    text = request.form["text"]

    add_comment(video_id,session["user"],text)

    return redirect("/watch/"+str(video_id))


@comment_routes.route("/comment/delete/<int:comment_id>/<int:video_id>")
def delete(comment_id,video_id):

    if "user" not in session:
        return redirect("/login")

    delete_comment(comment_id,session["user"])

    return redirect("/watch/"+str(video_id))