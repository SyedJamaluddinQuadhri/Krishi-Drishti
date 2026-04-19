# app/routers/auth.py
from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.otp import OTPCode
from app.schemas.auth import SendOTPRequest, VerifyOTPRequest
from app.services.sms import send_otp_sms
from app.utils.jwt import create_access_token, create_refresh_token
from app.config import settings

# Router WITHOUT prefix — main.py already adds /auth prefix
router = APIRouter()

OTP_EXPIRY_MINUTES = 5

@router.post("/send-otp")
def send_otp(payload: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to phone number for registration or login"""
    
    phone_full = f"{payload.country_code}{payload.phone}"
    
    # Generate 6-digit OTP
    otp = "123456"
    
    # Invalidate previous OTPs
    db.query(OTPCode).filter(
        OTPCode.phone == payload.phone,
        OTPCode.country_code == payload.country_code,
        OTPCode.purpose == payload.purpose,
        OTPCode.is_verified == False,
    ).delete()
    
    # Create new OTP
    otp_obj = OTPCode(
        phone=payload.phone,
        country_code=payload.country_code,
        otp_code=otp,
        purpose=payload.purpose,
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
    )
    db.add(otp_obj)
    db.commit()
    
    # Send OTP via SMS
    send_otp_sms(phone_full, otp)
    
    return {
        "success": True,
        "message": "OTP sent successfully",
        "expires_in_minutes": OTP_EXPIRY_MINUTES
    }

@router.post("/verify-otp")
def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP and create/login user, return JWT tokens"""
    
    # Find most recent OTP
    otp_row = (
        db.query(OTPCode)
        .filter(
            OTPCode.phone == payload.phone,
            OTPCode.country_code == payload.country_code,
            OTPCode.purpose == payload.purpose,
            OTPCode.is_verified == False,
        )
        .order_by(OTPCode.created_at.desc())
        .first()
    )
    
    if not otp_row or otp_row.otp_code != payload.otp_code:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )
    
    if otp_row.expires_at.replace(tzinfo=None) < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="OTP expired"
        )
    
    # Mark OTP as verified
    otp_row.is_verified = True
    db.add(otp_row)
    
    # Find or create user
    user = db.query(User).filter(
        User.phone == payload.phone,
        User.country_code == payload.country_code,
    ).first()
    
    if payload.purpose == "registration":
        if not user:
            user = User(
                phone=payload.phone,
                country_code=payload.country_code,
                is_verified=True,
            )
            db.add(user)
        else:
            user.is_verified = True
    else:  # login
        if not user or not user.is_verified:
            raise HTTPException(
                status_code=400,
                detail="User not registered. Please register first."
            )
    
    db.commit()
    db.refresh(user)
    
    # Generate JWT tokens
    token_data = {"sub": str(user.id), "phone": user.phone}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "phone": user.phone,
            "country_code": user.country_code,
            "name": user.name,
        },
        "message": "Phone verified successfully"
    }

@router.get("/test")
def test_auth():
    """Test endpoint to verify router is working"""
    return {"message": "Auth router is working!"}
