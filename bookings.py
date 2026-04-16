from flask import Blueprint, request, jsonify
from db import get_connection

bookings = Blueprint("bookings", __name__)

@bookings.route("/book", methods=["POST"])
def create_booking():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bookings (user_id, service, booking_date, booking_time) VALUES (?, ?, ?, ?)",
        data["user_id"], data["service"], data["booking_date"], data["booking_time"]
    )
    conn.commit()

    return jsonify({"message": "Booking created"})


@bookings.route("/my-bookings/<int:user_id>")
def my_bookings(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT service, booking_date, booking_time, status FROM bookings WHERE user_id=?",
        user_id
    )

    result = []
    for row in cursor.fetchall():
        result.append({
            "service": row[0],
            "date": str(row[1]),
            "time": str(row[2]),
            "status": row[3]
        })

    return jsonify(result)