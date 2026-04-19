"""
Farm and Soil Health Models
"""

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Boolean, Date, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
try:
    from geoalchemy2 import Geography
    _HAS_GEOALCHEMY = True
except ImportError:
    Geography = None
    _HAS_GEOALCHEMY = False
from datetime import datetime
import uuid
import enum

from app.database import Base

class FarmSizeUnit(str, enum.Enum):
    ACRES = "acres"
    HECTARES = "hectares"
    BIGHAS = "bighas"

class IrrigationType(str, enum.Enum):
    RAINFED = "rainfed"
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    FLOOD = "flood"
    NONE = "none"

class CropSeason(str, enum.Enum):
    KHARIF = "kharif"
    RABI = "rabi"
    ZAID = "zaid"
    PERENNIAL = "perennial"

class Farm(Base):
    """Farm model with geospatial data"""
    __tablename__ = "farms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    farm_name = Column(String(100))
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True) if _HAS_GEOALCHEMY else Column(String, nullable=True)
    latitude = Column(Float(precision=8))
    longitude = Column(Float(precision=8))
    size = Column(Float, nullable=False)
    size_unit = Column(Enum(FarmSizeUnit), default=FarmSizeUnit.ACRES)
    soil_type = Column(String(50))
    irrigation_type = Column(Enum(IrrigationType))
    region = Column(String(50))
    district = Column(String(50))
    state = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="farms")
    soil_health_cards = relationship("SoilHealthCard", back_populates="farm", cascade="all, delete-orphan")
    crop_recommendations = relationship("CropRecommendation", back_populates="farm", cascade="all, delete-orphan")
    yield_predictions = relationship("YieldPrediction", back_populates="farm", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Farm {self.farm_name or self.id}>"

class SoilHealthCard(Base):
    """Soil Health Card model"""
    __tablename__ = "soil_health_cards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String)
    image_path = Column(String)
    
    # Primary nutrients
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    
    # Soil properties
    ph_value = Column(Float)
    electrical_conductivity = Column(Float)
    organic_carbon = Column(Float)
    
    # Secondary nutrients and micronutrients
    sulphur = Column(Float)
    zinc = Column(Float)
    iron = Column(Float)
    copper = Column(Float)
    manganese = Column(Float)
    boron = Column(Float)
    
    # Metadata
    tested_date = Column(Date)
    lab_name = Column(String(200))
    is_verified = Column(Boolean, default=False)
    ocr_confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="soil_health_cards")
    crop_recommendations = relationship("CropRecommendation", back_populates="soil_health_card")
    yield_predictions = relationship("YieldPrediction", back_populates="soil_health_card")
    
    def __repr__(self):
        return f"<SoilHealthCard {self.id}>"

class Crop(Base):
    """Crop master data"""
    __tablename__ = "crops"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_name = Column(String(100), unique=True, nullable=False)
    scientific_name = Column(String(150))
    season = Column(Enum(CropSeason))
    duration_days = Column(Integer)
    water_requirement = Column(String(20))
    
    # Optimal requirements
    optimal_ph_min = Column(Float)
    optimal_ph_max = Column(Float)
    optimal_temp_min = Column(Integer)
    optimal_temp_max = Column(Integer)
    
    # Market data
    avg_price_per_quintal = Column(Float)
    avg_cost_per_acre = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    crop_recommendations = relationship("CropRecommendation", back_populates="crop")
    yield_predictions = relationship("YieldPrediction", back_populates="crop")
    
    def __repr__(self):
        return f"<Crop {self.crop_name}>"
