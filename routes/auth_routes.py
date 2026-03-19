from flask import Blueprint,render_template,request,redirect,session
import os
from werkzeug.utils import secure_filename

from config import Config
from core.security import hash_password,verify_password
from models.user_model import create_user,get_user_by_username

auth_routes=Blueprint("auth",__name__)


@auth_routes.route("/login",methods=["GET","POST"])
def login():

    error=None

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        user=get_user_by_username(username)

        if user and verify_password(password,user["password"]):

            session["user"]=user["id"]
            session["username"]=user["username"]
            session["profile_image"]=user["profile_image"]

            return redirect("/")

        else:
            error="Invalid username or password"

    return render_template("login.html",error=error)


@auth_routes.route("/logout")
def logout():

    session.pop("user",None)
    session.pop("username",None)
    session.pop("profile_image",None)

    return redirect("/")


@auth_routes.route("/register",methods=["GET","POST"])
def register():

    error=None

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]
        confirm=request.form["confirm"]

        if password!=confirm:
            error="Passwords do not match"
            return render_template("register.html",error=error)

        existing_user=get_user_by_username(username)

        if existing_user:
            error="Username already exists"
            return render_template("register.html",error=error)

        profile=request.files.get("profile_image")

        filename=None

        if profile and profile.filename!="":

            filename=secure_filename(profile.filename)

            save_path=os.path.join(Config.UPLOAD_PROFILE_FOLDER,filename)

            profile.save(save_path)

        hashed=hash_password(password)

        create_user(username,hashed,filename)

        return redirect("/login")

    return render_template("register.html",error=error)