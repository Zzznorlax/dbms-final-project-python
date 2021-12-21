from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.config import get_settings

engine = create_engine(get_settings().SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
