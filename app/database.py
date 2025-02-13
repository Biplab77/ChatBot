from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variables
DATABASE_URL = os.getenv("postgresql://postgres:9803@localhost/chat_bot")

# Create the SQLAlchemy engine using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating model classes
Base = declarative_base()