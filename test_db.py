import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=Student_booking_db;"
        "UID=sa;"
        "PWD=StrongPass123!;"
    )
    print("✅ Connected Successfully!")
    conn.close()
except Exception as e:
    print("❌ Error:", e)