"""
Pydantic schemas for request/response validation
"""

from app.schemas.auth import *
from app.schemas.farm import *
from app.schemas.recommendation import *

__all__ = [
    # Auth
    "OTPRequest",
    "OTPVerifyRequest",
    "TokenResponse",
    "UserResponse",
    
    # Farm
    "FarmCreate",
    "FarmResponse",
    "SoilHealthCardCreate",
    "SoilHealthCardResponse",
    "SHCUploadResponse",
    
    # Recommendation
    "CropRecommendationResponse",
    "YieldPredictionResponse",
    "OptimizationRecommendationResponse"
]
