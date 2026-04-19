"""
Recommendation and prediction schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CropRecommendationResponse(BaseModel):
    """Crop recommendation response"""
    id: str
    crop_name: str
    suitability_score: float
    rank: int
    recommendations_text: Optional[str]
    season: Optional[str]
    duration_days: Optional[int]
    water_requirement: Optional[str]
    avg_price_per_quintal: Optional[float]
    avg_cost_per_acre: Optional[float]
    weather_data: Optional[Dict[str, Any]]
    feature_importance: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OptimizationRecommendationResponse(BaseModel):
    """Optimization recommendation response"""
    id: str
    recommendation_type: str
    priority: int
    action_description: str
    expected_impact: Optional[str]
    cost_impact: Optional[float]
    yield_impact: Optional[float]
    timing: Optional[str]
    resources_needed: Optional[str]
    implementation_difficulty: Optional[str]
    
    class Config:
        from_attributes = True

class YieldPredictionResponse(BaseModel):
    """Yield prediction response"""
    id: str
    crop_name: str
    baseline_yield: float
    baseline_cost: Optional[float]
    baseline_revenue: Optional[float]
    baseline_profit: Optional[float]
    optimized_yield: Optional[float]
    optimized_cost: Optional[float]
    optimized_revenue: Optional[float]
    optimized_profit: Optional[float]
    yield_increase_percent: Optional[float]
    cost_increase_percent: Optional[float]
    roi_improvement: Optional[float]
    prediction_confidence: Optional[float]
    weather_data: Optional[Dict[str, Any]]
    optimization_recommendations: List[OptimizationRecommendationResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True
