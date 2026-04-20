from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ExpenseBase(BaseModel):
    amount: float
    category: str
    date: date
    description: str
    payment_mode: str

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    expenses: List[Expense] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
