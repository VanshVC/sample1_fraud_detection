import sqlite3
import os

db_path = r"c:\Users\vansh\Downloads\Fraud_Detection\backend\sql_app.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    print("Last 5 Transactions:")
    for row in rows:
        print(row)
    
    cur.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    print("\nLast 5 Predictions:")
    for row in rows:
        print(row)
    conn.close()
else:
    print("DB not found at", db_path)
