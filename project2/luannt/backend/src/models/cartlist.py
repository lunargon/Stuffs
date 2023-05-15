from pydantic import BaseModel

class CartList(BaseModel):
    product_id: int
    quantity: int
    color: str = None