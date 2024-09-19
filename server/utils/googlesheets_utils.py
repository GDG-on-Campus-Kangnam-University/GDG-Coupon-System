from googleapiclient import discovery
from google.oauth2 import service_account
from sqlalchemy.orm import Session
from models import Coupon
from utils.email_utils import send_email
from utils.add_text_to_png import add_text_to_png
from email_data.email_template import generate_gdg_welcome_email

def generate_output_path(coupon_number):
    return f"coupon_data/gdg_coupon/{coupon_number}.png"

class GooglesheetUtils:
    def __init__(self) -> None:
        self.spreadsheet_id = '1NNP9Jk9HEI5d_PsLK0K9PSkYGc60CYU7vTrg12EHHwA'
        self.credentials = service_account.Credentials.from_service_account_file(
            'google_sheets.json', 
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)

    def is_coupon_valid(self, coupon_code: str, db: Session):
        coupon = db.query(Coupon).filter(Coupon.coupon_number == coupon_code).first()
        if not coupon:
            return True, 0
        
        if coupon.is_used:
            return False, None
        
        return True, coupon.discount_price

    def read_and_update_spreadsheet(self, db: Session):
        # Apply Response와 Finance Sheet 데이터 가져오기
        apply_range = 'Apply Response!C:J'
        finance_range = 'Finance Sheet!B:G'
        
        apply_data = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=apply_range).execute().get('values', [])
        finance_data = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=finance_range).execute().get('values', [])
        
        if not apply_data or not finance_data:
            print("No data found.")
            return

        updates_apply = []
        updates_finance = []
       
        # 학번 매칭 및 쿠폰 유효성 확인
        for i, apply_row in enumerate(apply_data[1:], start=2):  # Apply Response 1행 헤더 제외      
            name = apply_row[0] if len(apply_row) > 0 else ''
            email = apply_row[1] if len(apply_row) > 1 else ''
            student_id_apply = apply_row[3] if len(apply_row) > 3 else ''  # 학번
            coupon_code = apply_row[6] if len(apply_row) > 6 else ''  # 쿠폰 번호, 존재하지 않으면 빈 문자열
            processed = apply_row[7] if len(apply_row) > 7 else None  # 처리 상태, 값이 없으면 None

            if processed != None:
                continue
            
            # 학번으로 Finance Sheet에서 찾기
            matching_finance = next((row for row in finance_data if (row[0] == student_id_apply and row[5] == 'FALSE')), None)
            if not matching_finance:
                continue
            
            # 쿠폰 유효성 확인
            is_valid, discount_price = self.is_coupon_valid(coupon_code, db)
            if not is_valid:
                # 쿠폰이 유효하지 않음
                updates_finance.append({
                    'range': f'Finance Sheet!E{finance_data.index(matching_finance) + 1}',  # 초대 상태 업데이트
                    'values': [['Coupon Error']]
                })
                updates_apply.append({
                    'range': f'Apply Response!J{i}',  # 처리 상태 업데이트
                    'values': [['Coupon Error']]
                })
                continue

            # 금액 확인: 15,000 - discount_price == Finance Sheet 금액
            expected_amount = 15000 - discount_price
            try:
                # 값이 있고, 숫자일 경우 정수 변환, 그렇지 않으면 0으로 설정
                actual_amount = int(matching_finance[2]) if matching_finance[2].strip() else 0
            except (ValueError, IndexError, AttributeError) as e:
                print(f"Error converting actual_amount: {e}")
                actual_amount = 0  # 기본값 0 또는 다른 값을 설정
                
            if expected_amount != actual_amount:
                # 금액 불일치
                updates_finance.append({
                    'range': f'Finance Sheet!E{finance_data.index(matching_finance) + 1}',
                    'values': [['Price Different', actual_amount-expected_amount]]
                })
                updates_apply.append({
                    'range': f'Apply Response!J{i}',
                    'values': [['Price Different']]
                })
                continue
            
            coupon = db.query(Coupon).filter(Coupon.coupon_number == coupon_code).first()
            if coupon:
                coupon.is_used = True
                db.commit()  # 변경 사항을 DB에 커밋
                db.refresh(coupon)  # 업데이트된 내용을 세션에서 다시 읽어옵니다.
                print(f"Coupon {coupon.coupon_number} has been marked as used.")
            
            # 쿠폰 생성
            new_coupon = Coupon(
                create_user_email=email,
                create_user_name=name,
                create_user_id=9,
                discount_price=5000
            )

            db.add(new_coupon)
            db.commit()
            db.refresh(new_coupon)
            
            image_path = "coupon_data/coupon_5000.png"  # 입력 이미지 경로
            output_path = generate_output_path(new_coupon.coupon_number)  # 출력 이미지 경로
            text = str(new_coupon.coupon_number)  # 삽입할 텍스트

            add_text_to_png(image_path, output_path, text)

            subject = "GDG on Campus Kangnam University 가입을 환영합니다!"
            body = generate_gdg_welcome_email(name, new_coupon.coupon_number)

            # 모든 조건이 충족되면 이메일 발송
            email_sent = send_email(email, subject, body, output_path)
    
            if not email_sent:
                # 이메일 발송 실패 시 상태 업데이트 (필요시 쿠폰 복구 등 추가 처리 가능)
                updates_apply.append({
                    'range': f'Apply Response!J{i}',
                    'values': [['Email Failed']]
                })
                continue  # 이메일 발송에 실패해도 다음 루프로 넘어감
            
            updates_finance.append({
                    'range': f'Finance Sheet!E{finance_data.index(matching_finance) + 1}',
                    'values': [['Invited Sent']]
                })
            # 처리 완료로 업데이트
            updates_apply.append({
                'range': f'Apply Response!J{i}',
                'values': [['Invited Sent']]
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

        print(f"Updated {len(updates_apply)} rows in Apply Response and {len(updates_finance)} rows in Finance Sheet.")
        return updates_apply, updates_finance
    
    # def get_emails_from_sheet(self):
    #     sheet_range = 'Notification!C:D'  # C열의 이메일 정보 가져오기
        
    #     result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=sheet_range).execute()
    #     print(result)
    #     return result.get('values', [])
    
    # def update_status_in_sheet(self, row_number, status):
    #     # D열에 상태를 업데이트하는 함수
    #     range_ = f'Notification!D{row_number}'  # D열의 특정 셀
    #     body = {
    #         'values': [[status]]  # 업데이트할 값
    #     }
    #     self.service.spreadsheets().values().update(
    #         spreadsheetId=self.spreadsheet_id, 
    #         range=range_, 
    #         valueInputOption='RAW', 
    #         body=body
    #     ).execute()
