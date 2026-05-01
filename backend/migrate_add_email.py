from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # 1️⃣ Add email column WITHOUT UNIQUE first
        db.session.execute(
            text('ALTER TABLE student ADD email VARCHAR(100) NULL')
        )
        db.session.commit()
        print("Email column added successfully (without UNIQUE).")
    except Exception as e:
        print(f"Error adding email column: {e}")