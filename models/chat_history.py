from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base  # Ensure this is the correct import

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ensuring a valid reference
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    # Relationship with User
    user = relationship("User", back_populates="chat_history")
