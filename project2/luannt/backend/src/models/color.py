from pydantic import BaseModel

class Color(BaseModel):
    label: str = None
    enable: bool = True