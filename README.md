# Order Management System

Система управления заказами с использованием FastAPI, Kafka и PostgreSQL.

## Технологический стек

- **FastAPI** - веб-фреймворк для создания API
- **PostgreSQL** - база данных
- **Kafka** - брокер сообщений
- **Prometheus + Grafana** - мониторинг
- **Docker & Docker Compose** - контейнеризация
- **pytest** - тестирование

## Функциональность

### 1. API Сервис (FastAPI)
Доступен по адресу `http://localhost:8000`

Основные эндпоинты:
- `POST /api/v1/orders/` - создание нового заказа
  ```json
  {
    "customer_name": "John Doe",
    "total_amount": 100.50
  }
  ```
- `GET /api/v1/orders/` - получение списка всех заказов
- `GET /health` - проверка работоспособности сервиса
- `GET /metrics` - метрики Prometheus
- `GET /docs` - Swagger UI с документацией API

### 2. Consumer (Обработчик заказов)
- Слушает Kafka топик "orders"
- Получает новые заказы
- Обрабатывает их (в текущей реализации просто меняет статус на "PROCESSED")
- Обновляет статус заказа в базе данных

### 3. База данных (PostgreSQL)
Структура таблицы orders:
- `id` - уникальный идентификатор
- `customer_name` - имя клиента
- `total_amount` - сумма заказа
- `status` - статус заказа (PENDING/PROCESSED)
- `created_at` - время создания
- `updated_at` - время обновления

### 4. Мониторинг
- **Prometheus** (`http://localhost:9090`)
  - Собирает метрики:
    - `orders_created_total` - количество созданных заказов
    - `order_processing_seconds` - время обработки заказов

- **Grafana** (`http://localhost:3000`)
  - Визуализация метрик
  - Default credentials: admin/admin

## Установка и запуск

### Предварительные требования
- Docker
- Docker Compose

### Запуск проекта

Запустить проект:
docker compose up --build

## Примеры использования

### 1. Создание заказа

```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
-H "Content-Type: application/json" \
-d '{"customer_name": "John Doe", "total_amount": 100.50}'
```

### 2. Получение списка заказов
```
curl http://localhost:8000/api/v1/orders/
```

### 3. Симуляция работы сервиса
```
python scripts/simulate_load.py
```

### 4. Мониторинг в Grafana

Доступ к дашборду:
1. Откройте http://localhost:3000
2. Войдите с учетными данными:
   - Логин: admin
   - Пароль: admin
3. Перейдите в раздел Dashboards -> Order Metrics

Дашборд отображает:
- Количество созданных заказов в секунду
- Среднее время обработки заказов
- Графики изменения метрик во времени

### Метрики в Prometheus

Доступные метрики:
- `orders_created_total` - общее количество созданных заказов
- `order_processing_seconds` - время обработки заказов
- `http_requests_total` - количество HTTP запросов

Доступ к Prometheus:
1. Откройте http://localhost:9090
2. Используйте вкладку Graph для просмотра метрик
3. Настроенные алерты доступны во вкладке Alerts

### 5. Настроенные алерты

1. **HighOrderRate**
   - Срабатывает при высокой скорости создания заказов
   - Порог: > 10 заказов в секунду за 5 минут
   - Уровень: warning

2. **SlowOrderProcessing**
   - Срабатывает при медленной обработке заказов
   - Порог: < 95% заказов обрабатываются дольше 5 секунд
   - Уровень: warning
