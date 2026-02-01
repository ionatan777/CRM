from app.db.session import SessionLocal, engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE messages ADD COLUMN is_read BOOLEAN DEFAULT FALSE"))
            conn.commit()
            print("Migration successful: Added is_read column")
        except Exception as e:
            print(f"Migration failed (maybe column exists): {e}")

if __name__ == "__main__":
    migrate()
