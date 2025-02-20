from pydantic_settings import BaseSettings, SettingsConfigDict

class TestSettings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "test_orders"
    
    model_config = SettingsConfigDict(env_file=".env")

test_settings = TestSettings() 