from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import timedelta, datetime
from passlib.context import CryptContext
from passlib.hash import bcrypt
from jose import jwt

from database import get_db
from database.models import User

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "mysecretkey"

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username: str, db):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(username: str, password: str, db):
    user = get_user(username, db)
    if not user:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Não é mais necessário ter um banco de dados fake com usuários, pois usamos a base real agora
# fake_users_db = {"john": {"username": "john","hashed_password": "$2b$12$yW9XGGGajx2QV7sbnfN2wuaaRvm4D4n4vrG4q.w/3bXv1Sndlnh7S", # password: secret "disabled": False,},
#                           }}

def get_password_hash(password):
    return bcrypt.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

# Não precisamos mais desta função, pois agora buscamos o usuário na base de dados
# def get_user(username: str):
#     user_dict = fake_users_db.get(username)
#     if user_dict:
#         return user_dict
#     return None

@router.post("/login")
def login(form_data: HTTPBasicCredentials = Depends(security), db=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user.username}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
