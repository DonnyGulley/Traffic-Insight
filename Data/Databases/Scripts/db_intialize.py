from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data.Databases.Scripts.base import Base

# Set up the database engine
engine = create_engine("sqlite:///traffic_system.db")

# Create all tables
Base.metadata.create_all(engine)

# Set up a session factory
Session = sessionmaker(bind=engine)

def get_db():
    """Provides a database session."""
    db = Session()
    try:
        yield db
    finally:
        db.close()
