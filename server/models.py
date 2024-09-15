import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoleEnum(enum.Enum):
    Admin = "Admin"
    CoreMember = "CoreMember"
    Lead = "Lead"

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    role = Column(Enum(RoleEnum, create_type=True), nullable=False, default=RoleEnum.CoreMember)  # Role column using Enum


    # Relationship with Coupon (One-to-Many)
    coupons = relationship('Coupon', back_populates='create_user')


# Coupon Model
class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coupon_number = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUID for coupon_number
    is_used = Column(Boolean, default=False, nullable=False)
    create_user_email = Column(String, nullable=False)
    create_user_name = Column(String, nullable=False)
    discount_price = Column(Integer, nullable=False, default=5000)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    create_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # User.id와 연결
    create_user = relationship('User', back_populates='coupons')  # 사용자와의 관계 정의
