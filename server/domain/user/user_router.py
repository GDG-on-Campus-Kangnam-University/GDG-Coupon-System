from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api/user",
)

class LoginRequest(BaseModel):
    id: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.id).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid ID or password")

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid ID or password")

    return {"id": user.id, "message": "Login successful"}
