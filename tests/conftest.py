import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.db.models import Order
from fastapi.testclient import TestClient
import os

# Устанавливаем флаг тестирования
os.environ['TESTING'] = 'true'

# После установки флага импортируем приложение
from src.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://admin:password@localhost:5432/test_db"

@pytest.fixture
def test_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
