"""
Weather cache model
"""

from sqlalchemy import Column, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from app.database import Base

class WeatherCache(Base):
    """Weather data cache"""
    __tablename__ = "weather_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    weather_data = Column(JSONB, nullable=False)
    forecast_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<WeatherCache {self.latitude},{self.longitude}>"
