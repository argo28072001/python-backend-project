from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:password@postgres:5432/orders"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:29092"
    KAFKA_TOPIC: str = "orders"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
