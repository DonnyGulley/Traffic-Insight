from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Data.Databases.Script.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=True)

    # Define the relationship with Feedback
    feedback = relationship("Feedback", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', location='{self.location}')>"
