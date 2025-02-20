from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from src.config import settings
from src.test_config import test_settings

class Base(DeclarativeBase):
    pass

# Выбираем настройки в зависимости от режима
if os.getenv('TESTING') == 'true':
    engine = create_engine(
        test_settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
