"""
Authentication schemas
"""

from pydantic import BaseModel, Field, validator, constr
from typing import Optional , Annotated
from datetime import datetime
import re



PhoneStr =Annotated[str, Field(min_length=10, max_length=15, pattern=r"^\d+$")]

class SendOTPRequest(BaseModel):
    phone: PhoneStr
    country_code: str = "+91"
    purpose: str = "registration"  # or "login"

class VerifyOTPRequest(BaseModel):
    phone: PhoneStr
    country_code: str = "+91"
    otp_code: constr(min_length=4, max_length=6)
    purpose: str = "registration"

class OTPRequest(BaseModel):
    """Request schema for sending OTP"""
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    country_code: str = Field(default="+91", description="Country code")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        if not re.match(r'^\d{10,15}$', v.replace('+', '')):
            raise ValueError('Invalid phone number format')
        return v

class OTPVerifyRequest(BaseModel):
    """Request schema for verifying OTP"""
    phone: str = Field(..., min_length=10, max_length=15)
    otp_code: str = Field(..., min_length=6, max_length=6)
    country_code: str = Field(default="+91")

class TokenResponse(BaseModel):
    """Response schema for authentication tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"

class UserResponse(BaseModel):
    """User response schema"""
    id: str
    phone: str
    country_code: str
    name: Optional[str]
    preferred_language: str
    created_at: datetime
    
    class Config:
        from_attributes = True
