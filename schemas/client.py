from typing import Optional
from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    gender: str
    cpf: str
    rg: str
    address: str
    marital_status: str
    income: Optional[float] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    balance: float
    has_loan: bool
    has_credit_card: bool

    class Config:
        orm_mode = True

class ClientUpdate(BaseModel):
    name: Optional[str]
    gender: Optional[str]
    cpf: Optional[str]
    rg: Optional[str]
    address: Optional[str]
    marital_status: Optional[str]
    income: Optional[float]
    balance: Optional[float]
    has_loan: Optional[bool]
    has_credit_card: Optional[bool]