import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# -----------------------------
# DATABASE CONFIG
# -----------------------------
uri = os.getenv("DATABASE_URL")
print("DATABASE URL:", uri)

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# MODEL
# -----------------------------
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# -----------------------------
# HELPER
# -----------------------------
def mask_last_name(last_name):
    if not last_name:
        return ""
    return last_name[0] + "*" * (len(last_name) - 1)

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return "Server is working!"

# -----------------------------
# RESET DB (FIXED)
# -----------------------------
@app.route("/reset-db")
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database reset done"

# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        first = data.get("firstName")
        last = data.get("lastName")
        input_value = data.get("input")
        password = data.get("password")

        if not first or not last or not input_value or not password:
            return jsonify({"message": "All fields required"}), 400

        masked_last = mask_last_name(last)

        # Better email detection
        if "@" in input_value:
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

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

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
# LOGIN
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

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

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# -----------------------------
# CREATE TABLES
# -----------------------------
with app.app_context():
    print("Creating tables if not exist...")
    db.create_all()
    # -----------------------------
# RUN (for local only)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)