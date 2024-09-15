from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship with Coupon (One-to-Many)
    coupons = relationship('Coupon', back_populates='create_user')


# Coupon Model
class Coupon(Base):
    __tablename__ = 'coupons'

    coupon_number = Column(String, primary_key=True, unique=True, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    create_user_email = Column(String, ForeignKey('users.email'), nullable=False)
    create_user_name = Column(String, nullable=False)
    discount_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship with User
    create_user = relationship('User', back_populates='coupons')

