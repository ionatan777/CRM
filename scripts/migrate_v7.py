from app.db.session import engine, Base
from app.models.user import User

def migrate():
    print("Creating new tables for Users...")
    Base.metadata.create_all(bind=engine)
    print("Migration successful.")

if __name__ == "__main__":
    migrate()
