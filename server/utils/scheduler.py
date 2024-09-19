import schedule
import time
from datetime import datetime, timedelta
from utils.googlesheets_utils import GooglesheetUtils
from database import get_db

def fetch_and_update_google_sheets_data():
    db = next(get_db())  # DB 세션 생성
    sheet_utils = GooglesheetUtils()
    
    try:
        updates_apply, updates_finance = sheet_utils.read_and_update_spreadsheet(db)
    finally:
        db.close()  # 세션 종료
    return updates_apply, updates_finance

def should_skip_execution():
    now = datetime.now()
    # 새벽 1시부터 아침 9시까지는 실행하지 않음
    if 1 <= now.hour < 9:
        return True
    return False

def schedule_next_run():
    now = datetime.now()
    next_run_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    # 실행을 건너뛸 시간대인지 확인
    if should_skip_execution():
        print("현재는 실행 시간대가 아닙니다. 다음 실행 시간을 대기합니다.")
    else:
        print(f"다음 실행 시간: {next_run_time}")
        schedule.every().hour.at(":00").do(fetch_and_update_google_sheets_data)

    # 스케줄러가 실행될 때까지 대기
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scheduler():
    schedule_next_run()
    while True:
        schedule.run_pending()
        time.sleep(1)
