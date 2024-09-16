import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, subject: str, body: str, image_path: str = None):
    # 이메일 유효성 검사
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
    if not re.match(reg, to_email):
        print("받으실 메일 주소를 정확히 입력하십시오.")
        return
    
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "gdg.kangnam@gmail.com"  # 발신자 이메일
    smtp_password = os.getenv('GOOGLE_MAIL_PASSWORD')  # Gmail 앱 비밀번호
    
    try:
        # SMTP 연결 및 로그인
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(smtp_user, smtp_password)
        
        # 이메일 설정
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email

        # 메일 본문 내용 추가 (HTML 형식)
        body_part = MIMEText(body, "html")
        msg.attach(body_part)

        # 이미지 첨부 (선택 사항)
        if image_path:
            try:
                with open(image_path, 'rb') as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header('Content-ID', '<image1>')
                    img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                    msg.attach(img)
            except FileNotFoundError as e:
                print(f"Image file not found: {e}")
                return

        # 이메일 전송
        smtp.sendmail(smtp_user, to_email, msg.as_string())
        print("정상적으로 메일이 발송되었습니다.")
    
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    
    finally:
        # SMTP 연결 종료
        smtp.quit()