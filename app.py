import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# -----------------------------
# DATABASE CONFIG (POSTGRESQL)
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "postgresql://student_db_r711_user:rEMCaZLa2FEbc76s9a5cV22WEHXOKEbQ@dpg-d7euktnaqgkc739tkm4g-a.oregon-postgres.render.com/student_db_r711"
)

# ✅ Fix for Render postgres:// issue
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# MODEL
# -----------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# -----------------------------
# MASK LAST NAME
# -----------------------------
def mask_last_name(last_name):
    if not last_name:
        return ""
    return last_name[0] + "*" * (len(last_name) - 1)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return "Server is working!"

# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    first = data.get("firstName")
    last = data.get("lastName")
    input_value = data.get("input")
    password = data.get("password")

    if not first or not last or not input_value or not password:
        return jsonify({"message": "All fields required"}), 400

    masked_last = mask_last_name(last)

    # detect email or username
    if "@gmail.com" in input_value:
        email = input_value
        username = None
    else:
        email = None
        username = input_value

    existing = Student.query.filter(
        (Student.email == email) | (Student.username == username)
    ).first()

    if existing:
        return jsonify({"message": "User already exists"}), 400

    # 🔐 hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    student = Student(
        first_name=first,
        last_name=masked_last,
        email=email,
        username=username,
        password=hashed_password.decode('utf-8')
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

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
        return jsonify({
            "message": "Login successful",
            "firstName": student.first_name,
            "lastName": student.last_name
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

# -----------------------------
# CHECK GOOGLE USER
# -----------------------------
@app.route("/check-google-user", methods=["POST"])
def check_google_user():
    data = request.json
    email = data.get("email")

    student = Student.query.filter_by(email=email).first()

    return jsonify({"exists": True if student else False})

# -----------------------------
# REGISTER GOOGLE USER
# -----------------------------
@app.route("/register-google", methods=["POST"])
def register_google():
    data = request.json

    first = data.get("firstName")
    last = data.get("lastName")
    email = data.get("email")

    masked_last = mask_last_name(last)
    existing = Student.query.filter_by(email=email).first()

    if existing:
        return jsonify({"message": "User already exists"}), 400

    student = Student(
        first_name=first,
        last_name=masked_last,
        email=email,
        username=None,
        password=""
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Google registration successful"}), 201

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)