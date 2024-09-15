from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

from database import get_db
from models import User

# 비밀번호 해싱 및 검증을 위한 bcrypt 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
)

# Pydantic 모델 (로그인 요청의 바디로 사용)
class LoginRequest(BaseModel):
    email: str
    password: str


# 로그인 엔드포인트
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 이메일을 기반으로 사용자를 검색
    user = db.query(User).filter(User.email == request.email or User.password == request.password).first()

    # 사용자가 존재하지 않으면 예외 처리
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")


    # 로그인 성공 시 사용자 정보 반환
    return {"user":{"id":user.id, "email":user.email, "name":user.name, "dept":user.dept}, "result": True}
