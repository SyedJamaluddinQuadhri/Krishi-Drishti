"""
Farm and Soil Health Card schemas
"""

from pydantic import BaseModel, Field, validator, field_serializer
from typing import Optional, Any
from datetime import datetime, date
from enum import Enum

class FarmSizeUnitEnum(str, Enum):
    ACRES = "acres"
    HECTARES = "hectares"
    BIGHAS = "bighas"

class IrrigationTypeEnum(str, Enum):
    RAINFED = "rainfed"
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    FLOOD = "flood"
    NONE = "none"

class FarmCreate(BaseModel):
    """Schema for creating a farm"""
    farm_name: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    size: float = Field(..., gt=0)
    size_unit: FarmSizeUnitEnum = FarmSizeUnitEnum.ACRES
    soil_type: Optional[str] = None
    irrigation_type: Optional[IrrigationTypeEnum] = None
    region: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None

class FarmResponse(BaseModel):
    """Farm response schema"""
    id: str
    farm_name: Optional[str]
    latitude: float
    longitude: float
    size: float
    size_unit: str
    soil_type: Optional[str]
    irrigation_type: Optional[str]
    region: Optional[str]
    district: Optional[str]
    state: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_id(self, v: Any) -> str:
        return str(v) if v else v

class SoilHealthCardCreate(BaseModel):
    """Schema for creating/updating soil health card"""
    nitrogen: Optional[float] = Field(None, ge=0)
    phosphorus: Optional[float] = Field(None, ge=0)
    potassium: Optional[float] = Field(None, ge=0)
    ph_value: Optional[float] = Field(None, ge=0, le=14)
    electrical_conductivity: Optional[float] = Field(None, ge=0)
    organic_carbon: Optional[float] = Field(None, ge=0)
    sulphur: Optional[float] = Field(None, ge=0)
    zinc: Optional[float] = Field(None, ge=0)
    iron: Optional[float] = Field(None, ge=0)
    copper: Optional[float] = Field(None, ge=0)
    manganese: Optional[float] = Field(None, ge=0)
    boron: Optional[float] = Field(None, ge=0)
    tested_date: Optional[date] = None
    lab_name: Optional[str] = None

class SoilHealthCardResponse(BaseModel):
    """Soil Health Card response schema"""
    id: str
    farm_id: str
    nitrogen: Optional[float]
    phosphorus: Optional[float]
    potassium: Optional[float]
    ph_value: Optional[float]
    electrical_conductivity: Optional[float]
    organic_carbon: Optional[float]
    sulphur: Optional[float]
    zinc: Optional[float]
    iron: Optional[float]
    copper: Optional[float]
    manganese: Optional[float]
    boron: Optional[float]
    tested_date: Optional[date]
    lab_name: Optional[str]
    is_verified: bool
    ocr_confidence: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

    @field_serializer('id', 'farm_id')
    def serialize_uuids(self, v: Any) -> str:
        return str(v) if v else v

class SHCUploadResponse(BaseModel):
    """Response after SHC image upload and OCR"""
    success: bool
    message: str
    shc_id: str
    extracted_data: SoilHealthCardCreate
    ocr_confidence: float
    image_url: str
