from flask import Blueprint, request, jsonify
from db import get_connection
import hashlib

auth = Blueprint("auth", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)",
        data["full_name"], data["email"], hash_password(data["password"])
    )
    conn.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, full_name FROM users WHERE email=? AND password=?",
        data["email"], hash_password(data["password"])
    )

    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "user_id": user[0],
        "full_name": user[1]
    })