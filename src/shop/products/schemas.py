from typing import List, Optional

from pydantic import BaseModel


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    category: Optional[str]
    price: int
    discount: Optional[int]


class AddProductRequestSchema(BaseModel):
    name: str
    category: str
    price: int
    discount: Optional[int] = 0


class ProductListResponseSchema(BaseModel):
    results: List[ProductResponseSchema]
