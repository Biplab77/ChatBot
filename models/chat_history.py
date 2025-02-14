from app.database import Base  # Now it should work

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
