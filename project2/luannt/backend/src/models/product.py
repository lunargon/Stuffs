from pydantic import BaseModel
from enum import Enum

class Product(BaseModel):
    id: int = None
    name: str = None
    images: list = None
    price: int = None
    original_price: int = None
    discount_rate: float = None
    quantity_sold: int = None
    day_ago_created: int = None
    specifications: list = None
    seller_id: int = None
    category_id: int = None
    brand_id: int = None
    color_options: list = None
    enable: bool = True