from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import db, User

users_bp = Blueprint("users", __name__)


@users_bp.route("/login")
def login_page():
    return render_template("login.html")


@users_bp.route("/sign_up")
def sign_up_page():
    return render_template("sign_up.html")
