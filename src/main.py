from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.db.database import engine, Base
from src.api.routes import router

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Инициализируем FastAPI приложение
app = FastAPI(title="Order Management System")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем метрики Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Подключаем роуты
app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 