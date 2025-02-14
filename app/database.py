from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)


# Get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)
# Ensure DATABASE_URL is not None
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Create the SQLAlchemy engine using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating model classes
Base = declarative_base()