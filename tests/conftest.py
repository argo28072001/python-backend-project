import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from fastapi.testclient import TestClient
import os
from src.test_config import test_settings
from src.db.database import get_db

# Устанавливаем флаг тестирования
os.environ['TESTING'] = 'true'

# Создаем тестовый движок базы данных
engine = create_engine(
    test_settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# После настройки базы данных импортируем приложение
from src.main import app

# Переопределяем зависимость get_db для тестов
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
