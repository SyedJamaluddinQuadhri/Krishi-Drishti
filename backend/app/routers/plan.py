"""
Yield prediction and optimization router
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.schemas.recommendation import YieldPredictionResponse, OptimizationRecommendationResponse
from app.models.farm import Farm, SoilHealthCard, Crop
from app.models.recommendation import YieldPrediction, OptimizationRecommendation
from app.models.user import User
from app.services.ml_service import predict_yield, optimize_yield
from app.services.weather_service import get_weather_data
from app.utils.jwt import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{crop_name}", response_model=YieldPredictionResponse)
async def get_yield_plan(
    crop_name: str,
    farm_id: str = Query(..., description="Farm ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get yield prediction and optimization plan for a specific crop
    """
    try:
        # Validate farm
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
                detail="No verified Soil Health Card found"
            )
        
        # Get crop details
        crop = db.query(Crop).filter(Crop.crop_name.ilike(crop_name)).first()
        
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crop '{crop_name}' not found in database"
            )
        
        # Get weather data
        weather_data = await get_weather_data(farm.latitude, farm.longitude, db)
        
        # Prepare input features
        features = {
            'crop_name': crop.crop_name,
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
            'land_size': farm.size,
            'soil_type': farm.soil_type or 'loam',
            'irrigation_type': farm.irrigation_type.value if farm.irrigation_type else 'rainfed'
        }
        
        # Get baseline yield prediction
        baseline = predict_yield(features)
        
        # Calculate baseline financials
        baseline_yield_total = baseline['yield_per_acre'] * farm.size
        baseline_cost = crop.avg_cost_per_acre * farm.size if crop.avg_cost_per_acre else 0
        baseline_revenue = baseline_yield_total * (crop.avg_price_per_quintal or 0) / 100  # Convert kg to quintal
        baseline_profit = baseline_revenue - baseline_cost
        
        # Get optimization recommendations
        optimization_result = optimize_yield(features, baseline['yield_per_acre'])
        
        # Calculate optimized financials
        optimized_yield_total = optimization_result['optimized_yield'] * farm.size
        optimized_cost = baseline_cost * (1 + optimization_result['cost_increase_percent'] / 100)
        optimized_revenue = optimized_yield_total * (crop.avg_price_per_quintal or 0) / 100
        optimized_profit = optimized_revenue - optimized_cost
        
        # Create yield prediction record
        yield_pred = YieldPrediction(
            farm_id=farm.id,
            shc_id=shc.id,
            crop_id=crop.id,
            crop_name=crop.crop_name,
            baseline_yield=baseline['yield_per_acre'],
            baseline_cost=baseline_cost,
            baseline_revenue=baseline_revenue,
            baseline_profit=baseline_profit,
            optimized_yield=optimization_result['optimized_yield'],
            optimized_cost=optimized_cost,
            optimized_revenue=optimized_revenue,
            optimized_profit=optimized_profit,
            yield_increase_percent=optimization_result['yield_increase_percent'],
            cost_increase_percent=optimization_result['cost_increase_percent'],
            roi_improvement=((optimized_profit - baseline_profit) / baseline_cost * 100) if baseline_cost > 0 else 0,
            model_version="v1.0",
            prediction_confidence=baseline.get('confidence', 0.85),
            weather_data=weather_data
        )
        
        db.add(yield_pred)
        db.flush()
        
        # Save optimization recommendations
        opt_recommendations = []
        for rec in optimization_result['recommendations']:
            opt_rec = OptimizationRecommendation(
                yield_prediction_id=yield_pred.id,
                recommendation_type=rec['type'],
                priority=rec['priority'],
                action_description=rec['action'],
                expected_impact=rec['impact'],
                cost_impact=rec.get('cost_impact', 0),
                yield_impact=rec.get('yield_impact', 0),
                timing=rec.get('timing', ''),
                resources_needed=rec.get('resources', ''),
                implementation_difficulty=rec.get('difficulty', 'medium')
            )
            db.add(opt_rec)
            opt_recommendations.append(opt_rec)
        
        db.commit()
        db.refresh(yield_pred)
        
        # Prepare response
        response_data = {
            'id': str(yield_pred.id),
            'crop_name': yield_pred.crop_name,
            'baseline_yield': yield_pred.baseline_yield,
            'baseline_cost': yield_pred.baseline_cost,
            'baseline_revenue': yield_pred.baseline_revenue,
            'baseline_profit': yield_pred.baseline_profit,
            'optimized_yield': yield_pred.optimized_yield,
            'optimized_cost': yield_pred.optimized_cost,
            'optimized_revenue': yield_pred.optimized_revenue,
            'optimized_profit': yield_pred.optimized_profit,
            'yield_increase_percent': yield_pred.yield_increase_percent,
            'cost_increase_percent': yield_pred.cost_increase_percent,
            'roi_improvement': yield_pred.roi_improvement,
            'prediction_confidence': yield_pred.prediction_confidence,
            'weather_data': yield_pred.weather_data,
            'optimization_recommendations': [
                OptimizationRecommendationResponse.from_orm(rec) 
                for rec in opt_recommendations
            ],
            'created_at': yield_pred.created_at
        }
        
        logger.info(f"Generated yield plan for {crop_name} on farm {farm_id}")
        
        return YieldPredictionResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating yield plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
