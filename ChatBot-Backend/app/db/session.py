from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine( settings.DATABASE_URL,pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False, #Prevents SQLAlchemy from automatically sending changes to the database before queries are executed
    bind=engine # Connects the session factory to the database engine so all sessions know which database to use.
)
