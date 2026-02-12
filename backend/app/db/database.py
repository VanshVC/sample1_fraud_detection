from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# PostgreSQL connection
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True
    )
except Exception as e:
    print(f"Error creating SQLAlchemy engine with URL: {settings.DATABASE_URL}")
    print("Please check that your DATABASE_URL environment variable is correctly set without quotes or spaces.")
    raise e
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
