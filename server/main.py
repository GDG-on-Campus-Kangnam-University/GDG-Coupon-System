import os

from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from domain.user import user_router
from domain.coupon import coupon_router

from pprint import pprint
from googleapiclient import discovery
from google.oauth2 import service_account

import smtplib  # 이메일 전송을 위한 모듈
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from models import Coupon
from database import get_db

import schedule
import time
import threading
from dotenv import load_dotenv
from datetime import datetime, timedelta

from models import Coupon, User, RoleEnum


load_dotenv()

app = FastAPI()

# Google Sheets 유틸리티 클래스
class GooglesheetUtils:
    def __init__(self) -> None:
        # 스프레드시트 ID 설정
        self.spreadsheet_id = '1AmDSojXOQX5Fwz7B8P4qY8xzBUK63QF5fhn6zUI5Uq4'

        self.credentials = service_account.Credentials.from_service_account_file(
            './google_sheets.json',  # 실제 서비스 계정 파일 경로 입력
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)

    # 쿠폰이 유효한지 확인하는 함수
    def is_coupon_valid(self, coupon_code: str, db: Session):
        coupon = db.query(Coupon).filter(Coupon.coupon_number == coupon_code).first()
        if not coupon or coupon.is_used:
            return False, None
        return True, coupon.discount_price

    def send_email(self, to_email: str, subject: str, body: str, image_path: str = None):
        # 이메일 유효성 검사
        reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
        if not re.match(reg, to_email):
            print("받으실 메일 주소를 정확히 입력하십시오.")
            return
        
        # Gmail SMTP 서버 연결
        gmail_smtp = "smtp.gmail.com"
        gmail_port = 465
        smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)

        # Gmail 계정과 비밀번호 설정
        my_account = "gdg.kangnam@gmail.com"  # 발신자 이메일
        my_password = os.getenv('GOOGLE_MAIL_PASSWORD') # Gmail 앱 비밀번호 또는 일반 비밀번호
        
        try:
            # 로그인
            smtp.login(my_account, my_password)
            
            # 메일 설정
            msg = MIMEMultipart()
            msg["Subject"] = subject  # 메일 제목
            msg["From"] = my_account
            msg["To"] = to_email

            # 메일 본문 내용 추가
            content_part = MIMEText(body, "plain")
            msg.attach(content_part)

            # 이미지 첨부 (optional)
            if image_path:
                try:
                    with open(image_path, 'rb') as file:
                        img = MIMEImage(file.read())
                        img.add_header('Content-Disposition', 'attachment', filename=image_path)
                        msg.attach(img)
                except FileNotFoundError as e:
                    print(f"Image file not found: {e}")
                    return

            # 이메일 전송
            smtp.sendmail(my_account, to_email, msg.as_string())
            print("정상적으로 메일이 발송되었습니다.")
        
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
        
        finally:
            # SMTP 서버 종료
            smtp.quit()

    # Google Sheets 데이터를 읽고 업데이트하는 함수
    def read_and_update_spreadsheet(self, db: Session):
        # Apply Sheet와 Finance Sheet 데이터 가져오기
        apply_range = 'Apply Sheet!C:J'
        finance_range = 'Finance Sheet!B:D'
        
        apply_data = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=apply_range).execute().get('values', [])
        finance_data = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=finance_range).execute().get('values', [])
        
        if not apply_data or not finance_data:
            print("No data found.")
            return

        updates_apply = []
        updates_finance = []
       
        # 학번 매칭 및 쿠폰 유효성 확인
        for i, apply_row in enumerate(apply_data[1:], start=2):  # Apply Sheet 1행 헤더 제외
            email = apply_row[1] if len(apply_row) > 1 else ''
            student_id_apply = apply_row[3] if len(apply_row) > 3 else ''  # 학번
            coupon_code = apply_row[6] if len(apply_row) > 6 else ''  # 쿠폰 번호, 존재하지 않으면 빈 문자열
            processed = apply_row[7] if len(apply_row) > 7 else None  # 처리 상태, 값이 없으면 None

            # J열이 True라면 건너뛰기
            if processed == 'True':
                continue

            # 학번으로 Finance Sheet에서 찾기
            matching_finance = next((row for row in finance_data if row[0] == student_id_apply), None)
            if not matching_finance:
                continue
            
            # 쿠폰 유효성 확인
            is_valid, discount_price = self.is_coupon_valid(coupon_code, db)
            if not is_valid:
                # 쿠폰이 유효하지 않음
                updates_finance.append({
                    'range': f'Finance Sheet!D{finance_data.index(matching_finance) + 1}',  # 초대 상태 업데이트
                    'values': [['Coupon Error']]
                })
                updates_apply.append({
                    'range': f'Apply Sheet!J{i}',  # 처리 상태 업데이트
                    'values': [['True']]
                })
                continue

            # 금액 확인: 15,000 - discount_price == Finance Sheet 금액
            expected_amount = 15000 - discount_price
            try:
                # 값이 있고, 숫자일 경우 정수 변환, 그렇지 않으면 0으로 설정
                actual_amount = int(matching_finance[1]) if matching_finance[1].strip() else 0
            except (ValueError, IndexError, AttributeError) as e:
                print(f"Error converting actual_amount: {e}")
                actual_amount = 0  # 기본값 0 또는 다른 값을 설정
                
            if expected_amount != actual_amount:
                # 금액 불일치
                updates_finance.append({
                    'range': f'Finance Sheet!D{finance_data.index(matching_finance) + 1}',
                    'values': [['Price Different', actual_amount-expected_amount]]
                })
                updates_apply.append({
                    'range': f'Apply Sheet!J{i}',
                    'values': [['True']]
                })
                continue
            
            coupon = db.query(Coupon).filter(Coupon.coupon_number == coupon_code).first()
            if coupon:
                coupon.is_used = True
                db.commit()  # 변경 사항을 DB에 커밋
                db.refresh(coupon)  # 업데이트된 내용을 세션에서 다시 읽어옵니다.
                print(f"Coupon {coupon.coupon_number} has been marked as used.")
            else:
                continue

            # 모든 조건이 충족되면 이메일 발송
            self.send_email(email, "Invitation", "You have been successfully invited!")
            
            updates_finance.append({
                    'range': f'Finance Sheet!D{finance_data.index(matching_finance) + 1}',
                    'values': [['Invited Sent']]
                })
            # 처리 완료로 업데이트
            updates_apply.append({
                'range': f'Apply Sheet!J{i}',
                'values': [['True']]
            })

        # 시트 업데이트 요청
        if updates_apply:
            body_apply = {
                'valueInputOption': 'RAW',
                'data': updates_apply
            }
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body_apply).execute()
        
        if updates_finance:
            body_finance = {
                'valueInputOption': 'RAW',
                'data': updates_finance
            }
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body_finance).execute()

        print(f"Updated {len(updates_apply)} rows in Apply Sheet and {len(updates_finance)} rows in Finance Sheet.")
        return updates_apply, updates_finance


# Google Sheets 데이터 읽기 및 업데이트 함수
def fetch_and_update_google_sheets_data():
    db = next(get_db())  # DB 세션 생성
    sheet_utils = GooglesheetUtils()
    try:
        updates_apply, updates_finance = sheet_utils.read_and_update_spreadsheet(db)
    finally:
        db.close()  # 세션 종료
        
    return updates_apply, updates_finance

# 30분 간격으로 실행할 시간을 설정하는 함수
def schedule_next_run():
    now = datetime.now()
    # 현재 시간을 기준으로 0분 또는 30분에 맞추기
    next_minute = 30 if now.minute < 30 else 0
    next_hour = now.hour if now.minute < 30 else (now.hour + 1) % 24

    # 다음 실행 시간을 계산
    next_run_time = now.replace(minute=next_minute, second=0, microsecond=0)
    if next_minute == 0 and now.minute >= 30:  # 만약 다음 시간이 0분으로 넘어갈 경우
        next_run_time += timedelta(hours=1)

    # 실행까지 남은 시간 계산
    delay = (next_run_time - now).total_seconds()

    # 첫 실행 후 매 30분마다 실행
    time.sleep(delay)
    fetch_and_update_google_sheets_data()
    schedule.every(30).minutes.do(fetch_and_update_google_sheets_data)

# 스케줄러를 실행하는 함수
def run_scheduler():
    schedule_next_run()  # 첫 실행을 예약
    while True:
        schedule.run_pending()
        time.sleep(1)
        
# 서버 실행 시 스케줄러 시작
@app.on_event("startup")
def startup_event():
    fetch_and_update_google_sheets_data()
    # 스케줄러를 별도의 스레드로 실행
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # 메인 프로그램이 종료되면 스레드도 자동 종료
    scheduler_thread.start()
    
def check_user_permission(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role not in [RoleEnum.Admin, RoleEnum.Lead]:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")

    return user

# FastAPI 엔드포인트 추가 (사용자가 요청을 보내면 실행)
@app.post("/update-sheets")
def update_google_sheets_data(user_id: int, db: Session = Depends(get_db)):
    # 유저 권한 체크
    check_user_permission(user_id, db)

    try:
        updates_apply, updates_finance = fetch_and_update_google_sheets_data()
        return {"message": f"Updated {len(updates_apply)} rows in Apply Sheet and {len(updates_finance)} rows in Finance Sheet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(coupon_router.router)