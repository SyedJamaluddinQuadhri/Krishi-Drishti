"""
OTP Service - SMS sending via Twilio or Msg91
"""

import httpx
import logging
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def send_otp(phone: str, country_code: str, otp_code: str) -> bool:
    """
    Send OTP via configured service (Twilio or Msg91)
    """
    try:
        if settings.OTP_SERVICE == "twilio":
            return await send_otp_twilio(phone, country_code, otp_code)
        elif settings.OTP_SERVICE == "msg91":
            return await send_otp_msg91(phone, country_code, otp_code)
        else:
            logger.warning(f"Unknown OTP service: {settings.OTP_SERVICE}")
            # For development, log the OTP
            logger.info(f"[DEV MODE] OTP for {phone}: {otp_code}")
            return True
            
    except Exception as e:
        logger.error(f"Error sending OTP: {e}")
        return False

async def send_otp_twilio(phone: str, country_code: str, otp_code: str) -> bool:
    """
    Send OTP using Twilio
    """
    try:
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            logger.warning("Twilio credentials not configured")
            logger.info(f"[DEV MODE] OTP for {phone}: {otp_code}")
            return True
        try:
            from twilio.rest import Client
        except ImportError:
            logger.error(
                "Twilio package not installed. Install with: pip install twilio or configure a different OTP service."
            )
            logger.info(f"[DEV MODE] OTP for {phone}: {otp_code}")
            return True

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Your Krishi Drishti verification code is: {otp_code}. Valid for {settings.OTP_EXPIRY_MINUTES} minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=f"{country_code}{phone}"
        )
        
        logger.info(f"OTP sent via Twilio: {message.sid}")
        return True
        
    except Exception as e:
        logger.error(f"Twilio error: {e}")
        return False

async def send_otp_msg91(phone: str, country_code: str, otp_code: str) -> bool:
    """
    Send OTP using Msg91
    """
    try:
        if not settings.MSG91_AUTH_KEY:
            logger.warning("Msg91 credentials not configured")
            logger.info(f"[DEV MODE] OTP for {phone}: {otp_code}")
            return True
        
        url = "https://api.msg91.com/api/v5/otp"
        
        payload = {
            "template_id": "your_template_id",  # Create template in Msg91 dashboard
            "mobile": country_code + phone,
            "authkey": settings.MSG91_AUTH_KEY,
            "otp": otp_code,
            "otp_expiry": settings.OTP_EXPIRY_MINUTES
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info(f"OTP sent via Msg91 to {phone}")
                return True
            else:
                logger.error(f"Msg91 error: {response.text}")
                return False
                
    except Exception as e:
        logger.error(f"Msg91 error: {e}")
        return False
