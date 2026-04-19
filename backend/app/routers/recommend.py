# TODO: Implement logic here
"""
Crop recommendation router
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.schemas.recommendation import CropRecommendationResponse
from app.models.farm import Farm, SoilHealthCard, Crop
from app.models.recommendation import CropRecommendation
from app.models.user import User
from app.services.ml_service import predict_crop_suitability
from app.services.weather_service import get_weather_data
from app.utils.jwt import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/crops", response_model=List[CropRecommendationResponse])
async def get_crop_recommendations(
    farm_id: str = Query(..., description="Farm ID"),
    top_n: int = Query(default=10, ge=1, le=20, description="Number of recommendations"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-powered crop recommendations for a farm
    """
    try:
        # Validate farm and get latest SHC
        farm = db.query(Farm).filter(
            Farm.id == uuid.UUID(farm_id),
            Farm.user_id == current_user.id
        ).first()
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        # Get latest verified SHC
        shc = db.query(SoilHealthCard).filter(
            SoilHealthCard.farm_id == farm.id,
            SoilHealthCard.is_verified == True
        ).order_by(SoilHealthCard.created_at.desc()).first()
        
        if not shc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No verified Soil Health Card found. Please upload and verify SHC first."
            )
        
        # Get weather data
        weather_data = await get_weather_data(farm.latitude, farm.longitude, db)
        
        # Prepare input features
        features = {
            'nitrogen': shc.nitrogen or 0,
            'phosphorus': shc.phosphorus or 0,
            'potassium': shc.potassium or 0,
            'ph': shc.ph_value or 7.0,
            'ec': shc.electrical_conductivity or 0,
            'oc': shc.organic_carbon or 0,
            'sulphur': shc.sulphur or 0,
            'zinc': shc.zinc or 0,
            'iron': shc.iron or 0,
            'copper': shc.copper or 0,
            'manganese': shc.manganese or 0,
            'boron': shc.boron or 0,
            'temperature': weather_data.get('temperature', 25),
            'humidity': weather_data.get('humidity', 60),
            'rainfall': weather_data.get('rainfall', 100),
            'soil_type': farm.soil_type or 'loam'
        }
        
        # Get ML predictions
        predictions = predict_crop_suitability(features, top_n=top_n)
        
        # Save recommendations to database
        recommendations = []
        for idx, pred in enumerate(predictions):
            # Get crop details
            crop = db.query(Crop).filter(Crop.crop_name == pred['crop_name']).first()
            
            recommendation = CropRecommendation(
                farm_id=farm.id,
                shc_id=shc.id,
                crop_id=crop.id if crop else None,
                crop_name=pred['crop_name'],
                suitability_score=pred['suitability_score'],
                rank=idx + 1,
                model_version="v1.0",
                weather_data=weather_data,
                recommendations_text=pred.get('recommendations'),
                feature_importance=pred.get('feature_importance', {})
            )
            
            db.add(recommendation)
            recommendations.append(recommendation)
        
        db.commit()
        
        # Prepare response with crop details
        response = []
        for rec in recommendations:
            crop = db.query(Crop).filter(Crop.id == rec.crop_id).first()
            
            rec_dict = {
                'id': str(rec.id),
                'crop_name': rec.crop_name,
                'suitability_score': rec.suitability_score,
                'rank': rec.rank,
                'recommendations_text': rec.recommendations_text,
                'weather_data': rec.weather_data,
                'feature_importance': rec.feature_importance,
                'created_at': rec.created_at
            }
            
            if crop:
                rec_dict.update({
                    'season': crop.season.value if crop.season else None,
                    'duration_days': crop.duration_days,
                    'water_requirement': crop.water_requirement,
                    'avg_price_per_quintal': crop.avg_price_per_quintal,
                    'avg_cost_per_acre': crop.avg_cost_per_acre
                })
            
            response.append(CropRecommendationResponse(**rec_dict))
        
        logger.info(f"Generated {len(response)} crop recommendations for farm {farm_id}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
