# Database connection setup for the API
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create base class for SQLAlchemy models
Base = declarative_base()

# Database connection parameters with defaults
DB_NAME = os.getenv("DB_NAME", "commerce_data")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Create the database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine to connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create a session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get a database session
# Used by FastAPI to manage database connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 