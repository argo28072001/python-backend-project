import requests
import random
import time
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Конфигурация
API_URL = "http://localhost:8000/api/v1"
CUSTOMERS = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Davis"]
MIN_AMOUNT = 10.0
MAX_AMOUNT = 1000.0
REQUEST_INTERVAL = 2  # секунды между запросами

def create_random_order():
    """Создает случайный заказ"""
    order_data = {
        "customer_name": random.choice(CUSTOMERS),
        "total_amount": round(random.uniform(MIN_AMOUNT, MAX_AMOUNT), 2)
    }
    
    try:
        response = requests.post(f"{API_URL}/orders/", json=order_data)
        response.raise_for_status()
        order = response.json()
        logging.info(f"Created order: ID={order['id']}, Customer={order['customer_name']}, Amount=${order['total_amount']}")
        return order
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create order: {e}")
        return None

def get_orders():
    """Получает список всех заказов"""
    try:
        response = requests.get(f"{API_URL}/orders/")
        response.raise_for_status()
        orders = response.json()
        logging.info(f"Retrieved {len(orders)} orders")
        return orders
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get orders: {e}")
        return []

def simulate_load():
    """Симулирует нагрузку на сервис"""
    logging.info("Starting load simulation...")
    
    while True:
        try:
            # Создаем новый заказ
            order = create_random_order()
            
            # Периодически запрашиваем список заказов
            if random.random() < 0.3:  # 30% шанс
                orders = get_orders()
            
            # Случайная пауза между запросами
            sleep_time = random.uniform(0.5, REQUEST_INTERVAL)
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            logging.info("Simulation stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    simulate_load()
    