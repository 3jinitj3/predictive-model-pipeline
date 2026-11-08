from pydantic import BaseModel



class UserRoles(BaseModel):
    developer: int = 1
    buyer: int = 4
    accountant: int = 5
    it_technician: int = 6
    hr_manager: int = 7
    logistics_clerk: int = 8
    owner: int = 9
    closer: int = 10