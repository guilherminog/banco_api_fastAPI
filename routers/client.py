from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models, database
from schemas import client as client_schema

router = APIRouter()

def get_db():
    db = None
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()

@router.post("/clients/", response_model=client_schema.Client)
def create_client(client: client_schema.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(
        name=client.name,
        gender=client.gender,
        cpf=client.cpf,
        rg=client.rg,
        address=client.address,
        marital_status=client.marital_status,
        income=client.income
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/clients/", response_model=List[client_schema.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    return clients

@router.get("/clients/{client_id}", response_model=client_schema.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/clients/{client_id}", response_model=client_schema.Client)
def update_client(client_id: int, client: client_schema.ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    for var, value in vars(client).items():
        if value is not None:
            setattr(db_client, var, value)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted successfully"}



'''
precisa atualizar classe ClientUpdate corretamente e 
que o importe esteja sendo feito de forma adequada 
no arquivo routers/client.py.
'''