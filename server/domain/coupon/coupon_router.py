from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from database import get_db
from models import Coupon, User

import uuid

router = APIRouter(
    prefix="/api/coupon",
    tags=["Coupon"],
)

# Pydantic 모델 (쿠폰 생성 요청의 바디로 사용)
class CouponCreateRequest(BaseModel):
    id: int
    email: str
    name: str

# 쿠폰 생성 엔드포인트
@router.post("/create")
def create_coupon(request: CouponCreateRequest, db: Session = Depends(get_db)):
    # 이메일을 기반으로 사용자가 존재하는지 확인
    user = db.query(User).filter(User.id == request.id).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # 사용자가 이미 2개 이상의 쿠폰을 가지고 있는지 확인
    coupon_count = db.query(Coupon).filter(Coupon.create_user_email == request.email).count()

    if coupon_count >= 2:
        raise HTTPException(status_code=400, detail="User already has 2 or more coupons")

    # 쿠폰 생성
    new_coupon = Coupon(
        create_user_email=request.email,
        create_user_name=request.name,
        create_user_id=user.id
    )

    # 쿠폰을 데이터베이스에 저장
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return {"coupon_number": new_coupon.coupon_number, "result": True}
