from typing import Optional

from pydantic import BaseModel, Field


class AddNewOrderResponseSchema(BaseModel):
    status: str
    id: int


class AddOrderLineRequestSchema(BaseModel):
    product_id: int
    qty: Optional[int] = Field(gt=0, default=1)


class AddOrderLineResponseSchema(BaseModel):
    id: int
    order_id: int
    product_id: int
    qty: int
