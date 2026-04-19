# app/services/sms.py
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def send_otp_sms(phone_full: str, otp: str) -> None:
    if settings.ENVIRONMENT == "development":
        logger.info(f"[DEV] OTP for {phone_full}: {otp}")
        return

    try:
        from twilio.rest import Client
    except ImportError:
        logger.error(
            "Twilio package not installed. Install with: pip install twilio or set OTP service to a different provider."
        )
        return

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your Krishi Drishti OTP is {otp}. It is valid for 5 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_full,
        )
    except Exception as e:
        logger.error(f"Twilio error while sending SMS: {e}")
