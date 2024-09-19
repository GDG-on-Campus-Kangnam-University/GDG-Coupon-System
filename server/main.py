from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from database import get_db
from utils.scheduler import run_scheduler, fetch_and_update_google_sheets_data
from utils.auth_utils import check_user_permission
import threading
from sqlalchemy.orm import Session

from domain.user import user_router
from domain.coupon import coupon_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

@app.post("/update-sheets")
def update_google_sheets_data(user_id: int, db: Session = Depends(get_db)):
    check_user_permission(user_id, db)
    try:
        updates_apply, updates_finance = fetch_and_update_google_sheets_data()
        return {"message": f"Updated {len(updates_apply)} rows in Apply Sheet and {len(updates_finance)} rows in Finance Sheet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

origins = ["http://127.0.0.1:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(coupon_router.router)
app.mount("/static", StaticFiles(directory="../client/build/static"))

@app.get("/")
def index():
    return FileResponse("../client/build/index.html")
