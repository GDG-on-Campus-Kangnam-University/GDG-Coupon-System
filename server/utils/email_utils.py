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
    my_password = os.getenv('GOOGLE_MAIL_PASSWORD') # Gmail 앱 비밀번호
    
    try:
        # 로그인
        smtp.login(my_account, my_password)
        
        # 메일 설정
        msg = MIMEMultipart()
        msg["Subject"] = subject
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
