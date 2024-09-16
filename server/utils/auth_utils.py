from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, RoleEnum

def check_user_permission(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role not in [RoleEnum.Admin, RoleEnum.Lead]:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    
    return user
