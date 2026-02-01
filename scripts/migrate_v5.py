from app.db.session import engine, Base
from app.models.tag import Tag
from app.models.note import Note
from app.models.contact import Contact # Ensure relationship is loaded

def migrate():
    print("Creating new tables for Tags and Notes...")
    # This will create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Migration successful.")

if __name__ == "__main__":
    migrate()
