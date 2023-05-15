from pydantic import BaseModel

class CartItem(BaseModel):
    product_id: int
    user: str
    color: str
    quantity: int
    created_at: str
    enable: bool = True