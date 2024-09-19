from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Coupon, User, RoleEnum
from utils.add_text_to_png import add_text_to_png

from utils.email_utils import send_email
from email_data.email_template import get_notification_email_template
from utils.googlesheets_utils import GooglesheetUtils, generate_output_path

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
    if user.role == RoleEnum.CoreMember:
        coupon_count = db.query(Coupon).filter(Coupon.create_user_email == request.email).count()

        if coupon_count >= 2:
            raise HTTPException(status_code=400, detail="User already has 2 or more coupons")

    # 쿠폰 생성
    new_coupon = Coupon(
        create_user_email=request.email,
        create_user_name=request.name,
        create_user_id=user.id,
        discount_price=5000
    )

    # 쿠폰을 데이터베이스에 저장
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    
    # 사용 예시
    image_path = "coupon_data/coupon_5000.png"  # 입력 이미지 경로
    output_path = generate_output_path(new_coupon.coupon_number)  # 출력 이미지 경로
    text = str(new_coupon.coupon_number)  # 삽입할 텍스트

    add_text_to_png(image_path, output_path, text)

    # subject = "GDG Kangnam University Core Member 특전"
    # body = get_notification_email_template(request.name, new_coupon.coupon_number, request.email)
    
    # send_email(request.email, subject, body, output_path)

    return {"coupon_number": new_coupon.coupon_number, "result": True}

# 쿠폰 조회 엔드포인트 (유저 ID로 유저가 가진 모든 쿠폰을 조회)
@router.get("/user/{user_id}")
def get_user_coupons(user_id: int, db: Session = Depends(get_db)):
    # 유저 조회
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 유저가 가진 모든 쿠폰 조회
    coupons = db.query(Coupon).filter(Coupon.create_user_id == user_id).all()

    # 쿠폰이 없을 때 처리
    if not coupons:
        return {"message": "This user has no coupons"}

    return {"user_id": user_id, "coupons": [coupon.coupon_number for coupon in coupons]}

def mask_coupon_number(coupon_number: str) -> str:
    if len(coupon_number) > 8:
        return coupon_number[:4] + "****" + coupon_number[-4:]
    return coupon_number

# 쿠폰 목록 조회 API
@router.get("/list")
def list_coupons(user_id: int, is_used: bool = None, db: Session = Depends(get_db)):
    # 유저를 조회
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 기본적으로 모든 쿠폰을 가져오되, 사용 여부에 따라 필터링 가능
    query = db.query(Coupon)
    if is_used is not None:
        query = query.filter(Coupon.is_used == is_used)

    coupons = query.all()

    # CoreMember일 경우 쿠폰 번호를 마스킹 처리
    if user.role == RoleEnum.CoreMember:
        return {
            "coupons": [
                {
                    "id": coupon.id,
                    "coupon_number": mask_coupon_number(coupon.coupon_number),
                    "is_used": coupon.is_used,
                    "create_user_email": coupon.create_user_email,
                    "create_user_name": coupon.create_user_name,
                    "discount_price": coupon.discount_price,
                    "created_at": coupon.created_at,
                    "updated_at": coupon.updated_at
                }
                for coupon in coupons
            ]
        }

    # Admin이나 Lead는 마스킹 없이 쿠폰 정보를 볼 수 있음
    return {
        "coupons": [
            {
                "id": coupon.id,
                "coupon_number": coupon.coupon_number,
                "is_used": coupon.is_used,
                "create_user_email": coupon.create_user_email,
                "create_user_name": coupon.create_user_name,
                "discount_price": coupon.discount_price,
                "created_at": coupon.created_at,
                "updated_at": coupon.updated_at
            }
            for coupon in coupons
        ]
    }

# @router.post("/send-email")
# def send_email_api(db: Session = Depends(get_db)):
    googlesheet_utils = GooglesheetUtils()
    
    # 구글 시트에서 이메일 목록 및 상태 정보 가져오기
    emails_data = googlesheet_utils.get_emails_from_sheet()

    # 이메일 보내기 작업 수행
    for index, row in enumerate(emails_data[1:], start=1):  # start=1로 1행부터 처리
        email = row[0] if len(row) > 0 else None
        
        if not email:
            continue  # 이메일이 없으면 건너뜀
        
        # 쿠폰 생성
        new_coupon = Coupon(
            create_user_email=email,
            create_user_name=email,
            create_user_id=9,
            discount_price=5000,
        )

        # 쿠폰을 데이터베이스에 저장
        db.add(new_coupon)
        db.commit()
        db.refresh(new_coupon)
        
        subject = "GDG On Campus Kangnam Univ. 오픈 알림"
        body = get_notification_email_template(new_coupon.coupon_number)
        
        image_path = "coupon_data/coupon_5000.png"  # 입력 이미지 경로
        output_path = generate_output_path(new_coupon.coupon_number)  # 출력 이미지 경로
        text = str(new_coupon.coupon_number)  # 삽입할 텍스트

        add_text_to_png(image_path, output_path, text)
        
        # 이메일 전송 함수 호출
        email_sent = send_email(email, subject, body, output_path)
        
        if not email_sent:
            # 전송 실패 시 구글 시트 D열에 상태 기록
            googlesheet_utils.update_status_in_sheet(index + 1, "Email Failed")
            continue  # 이메일 발송에 실패해도 다음 루프로 넘어감
        
        # 성공적으로 전송된 경우에도 필요 시 상태 업데이트 가능
        googlesheet_utils.update_status_in_sheet(index + 1, "Email Sent")

    return {"message": "Email processing completed."}