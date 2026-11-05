from pydantic import BaseModel



class TokenData(BaseModel):
    user_id: int
    username: str
    login_id: int


