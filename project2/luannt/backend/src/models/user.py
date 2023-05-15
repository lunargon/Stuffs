from pydantic import BaseModel, constr, EmailStr, AnyUrl

regex_phone_number = constr(regex="[0-9]{9,10}")

class UserModel(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None
    phone: regex_phone_number = None
    first_name: str = None
    last_name: str = None
    permission: bool = False
    avatar: AnyUrl = None
    created_at: str = None
    enable: bool = True
    wallet: int = 0