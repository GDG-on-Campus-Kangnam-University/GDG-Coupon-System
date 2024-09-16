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

def schedule_next_run():
    now = datetime.now()
    next_minute = 30 if now.minute < 30 else 0
    # next_hour = now.hour if now.minute < 30 else (now.hour + 1) % 24
    next_run_time = now.replace(minute=next_minute, second=0, microsecond=0)
    if next_minute == 0 and now.minute >= 30:
        next_run_time += timedelta(hours=1)

    delay = (next_run_time - now).total_seconds()
    time.sleep(delay)
    fetch_and_update_google_sheets_data()
    schedule.every(30).minutes.do(fetch_and_update_google_sheets_data)

def run_scheduler():
    schedule_next_run()
    while True:
        schedule.run_pending()
        time.sleep(1)
