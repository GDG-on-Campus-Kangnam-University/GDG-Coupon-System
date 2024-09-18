import os
import smtplib
import re
import time  # 대기 시간을 추가하기 위해 필요한 모듈
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, subject: str, body: str, image_path: str = None, wait_time: int = 10):
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
    if not re.match(reg, to_email):
        print("받으실 메일 주소를 정확히 입력하십시오.")
        return False  # 실패 시 False 반환
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "gdg.kangnam@gmail.com"
    smtp_password = os.getenv('GOOGLE_MAIL_PASSWORD')

    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(smtp_user, smtp_password)
        
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email
        body_part = MIMEText(body, "html")
        msg.attach(body_part)

        if image_path:
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<image1>')
                img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                msg.attach(img)

        smtp.sendmail(smtp_user, to_email, msg.as_string())
        print(f"정상적으로 {to_email}에게 메일이 발송되었습니다.")
        
        print(f"{wait_time}초 대기 후 다음 메일을 전송합니다.")
        time.sleep(wait_time)
        return True  # 성공 시 True 반환

    except (smtplib.SMTPException, FileNotFoundError) as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False  # 실패 시 False 반환
    
    finally:
        smtp.quit()