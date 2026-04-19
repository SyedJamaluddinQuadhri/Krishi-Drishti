# app/models/otp.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base

class OTPCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), index=True, nullable=False)
    country_code = Column(String(5), default="+91")
    otp_code = Column(String(6), nullable=False)
    purpose = Column(String(20), nullable=False)  # 'registration' or 'login'
    is_verified = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
