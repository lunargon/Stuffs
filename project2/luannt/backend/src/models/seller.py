from pydantic import BaseModel

class Seller(BaseModel):
    id: int = None
    name: str = None
    address: str = None
    enable: bool = True