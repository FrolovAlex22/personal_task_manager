from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: str = None
    hash_password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str