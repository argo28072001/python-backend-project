from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from kafka import KafkaProducer
import json
from prometheus_client import Counter, Histogram
import time

from src.db.database import get_db
from src.db.models import Order as OrderModel
from src.api.models import Order, OrderCreate
from src.config import settings

router = APIRouter()

# Метрики
order_counter = Counter('orders_created_total', 'Total orders created')
order_latency = Histogram('order_processing_seconds', 'Time spent processing order')

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[settings.KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@router.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    with order_latency.time():
        db_order = OrderModel(
            customer_name=order.customer_name,
            total_amount=order.total_amount,
            status="PENDING"
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Отправка события в Kafka
        producer.send(settings.KAFKA_TOPIC, {
            "order_id": db_order.id,
            "customer_name": db_order.customer_name,
            "total_amount": db_order.total_amount
        })
        
        order_counter.inc()
        return db_order

@router.get("/orders/", response_model=List[Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders
