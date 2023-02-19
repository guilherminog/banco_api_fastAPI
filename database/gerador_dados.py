import random
import string

from sqlalchemy.orm import Session
from models import Client
from database.database import engine
from database.database import Base

def generate_random_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]
    cpf = cpf + [sum([((i + 1) * v) for i, v in enumerate(cpf)]) % 11 % 10]
    cpf = cpf + [sum([((i + 2) * v) for i, v in enumerate(cpf)]) % 11 % 10]
    return ''.join(map(str, cpf))

def generate_random_rg():
    rg = [random.randint(0, 9) for _ in range(9)]
    rg = rg + [sum([((i + 1) * v) for i, v in enumerate(rg)]) % 11 % 10]
    return ''.join(map(str, rg))

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_clients():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)

    for i in range(250):
        client = Client(
            name=generate_random_name(),
            gender=random.choice(['M', 'F']),
            cpf=generate_random_cpf(),
            rg=generate_random_rg(),
            address=f'Rua {generate_random_name()}',
            marital_status=random.choice(['single', 'married', 'divorced']),
            balance=random.uniform(0, 10000),
            has_loan=random.choice([True, False]),
            has_credit_card=random.choice([True, False]),
            income=random.uniform(1000, 10000)
        )
        session.add(client)

    session.commit()

generate_clients()
