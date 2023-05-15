from pydantic import BaseModel

class Brand(BaseModel):
    id: int = None
    name: str = None
    enable: bool = True