from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # Ensure this is the correct import

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    # Relationship with ChatHistory
    chat_history = relationship("ChatHistory", back_populates="user")
