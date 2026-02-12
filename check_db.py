import sys
import os

# Add backend to path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.db.database import engine
from sqlalchemy import text

def check_live_data():
    try:
        with engine.connect() as conn:
            print("--- Latest 5 Transactions ---")
            result = conn.execute(text("SELECT * FROM transactions ORDER BY id DESC LIMIT 5"))
            for row in result:
                print(row)
            
            print("\n--- Latest 5 Predictions ---")
            result = conn.execute(text("SELECT * FROM predictions ORDER BY id DESC LIMIT 5"))
            for row in result:
                print(row)
                
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == "__main__":
    check_live_data()
