from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    customer_name: str
    total_amount: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
