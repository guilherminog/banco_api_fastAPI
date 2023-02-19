from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from database import models, database

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "mysecretkey"

security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not user.verify_password(password):
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
fake_users_db = {
    "john": {
        "username": "john",
        "hashed_password": "$2b$12$yW9XGGGajx2QV7sbnfN2wuaaRvm4D4n4vrG4q.w/3bXv1Sndlnh7S", # password: secret
        "disabled": False,
    },
}

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return user_dict

@router.post("/login")
def login(form_data: HTTPBasicCredentials = Depends(security)):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user["username"]}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, database.get_db())
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(current_user: models.User = Depends(database.get_current_user)):
    return {"username": current_user.username, "email": current_user.email}

