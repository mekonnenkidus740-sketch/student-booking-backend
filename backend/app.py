import os
import datetime
import jwt
import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
app.config['SECRET_KEY'] = 'super_secret_key_change_this'

uri = os.getenv("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# MODELS
# -----------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(200))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.String(50))

# -----------------------------
# HELPERS
# -----------------------------
def mask_last_name(last_name):
    if not last_name:
        return ""
    return last_name[0] + "*" * (len(last_name) - 1)

def generate_token(user_id):
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return "Server is working!"

# -----------------------------
# 🔥 RESET DATABASE (TEMP)
# -----------------------------
@app.route("/reset-db")
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database reset done"

# -----------------------------
# REGISTER (FIXED)
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        first = data.get("firstName", "").strip()
        last = data.get("lastName", "").strip()
        input_value = data.get("input", "").strip().lower()
        password = data.get("password", "").strip()

        if not first or not last or not input_value or not password:
            return jsonify({"message": "All fields required"}), 400

        masked_last = mask_last_name(last)

        email = None
        username = None

        # detect email
        if "@" in input_value:
            email = input_value
        else:
            username = input_value

        # check existing user
        existing = Student.query.filter(
            (Student.email == email) |
            (Student.username == username)
        ).first()

        if existing:
            return jsonify({"message": "User already exists"}), 400

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        student = Student(
            first_name=first,
            last_name=masked_last,
            email=email,
            username=username,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        print("REGISTER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# -----------------------------
# LOGIN (JWT)
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        input_value = data.get("input")
        password = data.get("password")
        student = Student.query.filter(
            (Student.email == input_value) |
            (Student.username == input_value)
        ).first()

        if student and bcrypt.checkpw(
            password.encode('utf-8'),
            student.password.encode('utf-8')
        ):
            token = generate_token(student.id)

            return jsonify({
                "message": "Login successful",
                "token": token,
                "firstName": student.first_name,
                "lastName": student.last_name
            }), 200

        return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# -----------------------------
# PROFILE (Protected)
# -----------------------------
@app.route("/profile", methods=["GET"])
def profile():
    try:
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        data = verify_token(token)
        user = Student.query.get(data["user_id"])

        return jsonify({
            "firstName": user.first_name,
            "lastName": user.last_name
        })

    except Exception:
        return jsonify({"message": "Invalid token"}), 401

# -----------------------------
# BOOKING (Protected)
# -----------------------------
@app.route("/book", methods=["POST"])
def book():
    try:
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        data_token = verify_token(token)
        user_id = data_token["user_id"]

        data = request.get_json()
        date = data.get("date")

        booking = Booking(user_id=user_id, date=date)

        db.session.add(booking)
        db.session.commit()

        return jsonify({"message": "Booked successfully"}), 200

    except Exception as e:
        print("BOOK ERROR:", str(e))
        return jsonify({"message": "Unauthorized"}), 401

# -----------------------------
# INIT DB
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)