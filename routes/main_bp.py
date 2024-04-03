from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]


@main_bp.route("/")
def hello_world():
    return "<h1>Hello, Sanlam! 😀</h1>"


@main_bp.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)
