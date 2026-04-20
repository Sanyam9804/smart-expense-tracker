from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Vercel's Serverless environment is completely read-only EXCEPT for the /tmp directory.
# Vercel natively injects VERCEL_ENV environment variables
if os.environ.get("VERCEL_ENV") or os.environ.get("VERCEL_URL"):
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/expense_tracker.db"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./expense_tracker.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
