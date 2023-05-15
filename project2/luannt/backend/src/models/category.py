from pydantic import BaseModel

class Category(BaseModel):
    name: str = None
    category: int = None
    enable: bool = True