# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from Data.Databases.Script.base import Base

# Base = declarative_base()

# class Feedback(Base):
#     __tablename__ = "feedback"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     content = Column(String, nullable=False)
    
#     # Lazy import of User inside the relationship definition to avoid circular import
#     def __init__(self):
#         from Data.Databases.user import User  # Import here to avoid circular dependency
#         self.user = relationship("User", back_populates="feedback")

#     def __repr__(self):
#         return f"<Feedback(id={self.id}, user_id={self.user_id}, content='{self.content}')>"



from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from Data.Databases.Script.base import Base

# Base is imported, so no need to reassign declarative_base()

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    
    # Relationship with User (avoiding circular import issues)
    user = relationship("User", back_populates="feedback", lazy="select")

    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, content='{self.content}')>"