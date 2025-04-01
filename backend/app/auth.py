import logging
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app.database import (
    create_user,
    verify_user_credentials,
)

auth = Blueprint("auth", __name__)


logger = logging.getLogger(__name__)



@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    user = create_user(username, email, password)
    if not user:
        return jsonify({"error": "User already exists"}), 409

    login_user(user)
    return jsonify({"message": "User registered and logged in", "user": user.username})

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = verify_user_credentials(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    login_user(user)
    return jsonify({"message": "Login successful", "user": user.username})

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@auth.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    })
