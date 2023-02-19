from sqlalchemy import Boolean, Column, Float, Integer, String
from passlib.hash import pbkdf2_sha256
from database.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    rg = Column(String, unique=True, index=True)
    address = Column(String, index=True)
    marital_status = Column(String, index=True)
    balance = Column(Float, default=0)
    has_loan = Column(Boolean, default=False)
    has_credit_card = Column(Boolean, default=False)
    income = Column(Float)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.hashed_password)