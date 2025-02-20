from kafka import KafkaConsumer
import json
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db.models import Order
from src.config import settings
import time

def process_order():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id="order_processor_group"
    )

    for message in consumer:
        order_data = message.value
        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_data["order_id"]).first()
            if order:
                # Имитация обработки
                time.sleep(2)
                order.status = "PROCESSED"
                db.commit()
        finally:
            db.close()

if __name__ == "__main__":
    process_order()
