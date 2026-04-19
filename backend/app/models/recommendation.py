"""
Recommendation and Prediction Models
"""

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base

class CropRecommendation(Base):
    """Crop recommendation model"""
    __tablename__ = "crop_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    shc_id = Column(UUID(as_uuid=True), ForeignKey("soil_health_cards.id"))
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=True)
    crop_name = Column(String(100), nullable=False)
    suitability_score = Column(Float)
    rank = Column(Integer)
    model_version = Column(String(20))
    weather_data = Column(JSONB)
    recommendations_text = Column(String)
    feature_importance = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="crop_recommendations")
    soil_health_card = relationship("SoilHealthCard", back_populates="crop_recommendations")
    crop = relationship("Crop", back_populates="crop_recommendations")
    
    def __repr__(self):
        return f"<CropRecommendation {self.crop_name} - {self.suitability_score}>"

class YieldPrediction(Base):
    """Yield prediction model"""
    __tablename__ = "yield_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)
    shc_id = Column(UUID(as_uuid=True), ForeignKey("soil_health_cards.id"))
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=False)
    crop_name = Column(String(100), nullable=False)
    
    # Baseline prediction
    baseline_yield = Column(Float, nullable=False)
    baseline_cost = Column(Float)
    baseline_revenue = Column(Float)
    baseline_profit = Column(Float)
    
    # Optimized prediction
    optimized_yield = Column(Float)
    optimized_cost = Column(Float)
    optimized_revenue = Column(Float)
    optimized_profit = Column(Float)
    yield_increase_percent = Column(Float)
    cost_increase_percent = Column(Float)
    roi_improvement = Column(Float)
    
    # Model metadata
    model_version = Column(String(20))
    prediction_confidence = Column(Float)
    weather_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="yield_predictions")
    soil_health_card = relationship("SoilHealthCard", back_populates="yield_predictions")
    crop = relationship("Crop", back_populates="yield_predictions")
    optimization_recommendations = relationship("OptimizationRecommendation", back_populates="yield_prediction", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<YieldPrediction {self.crop_name} - {self.baseline_yield}>"

class OptimizationRecommendation(Base):
    """Optimization recommendations for yield improvement"""
    __tablename__ = "optimization_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    yield_prediction_id = Column(UUID(as_uuid=True), ForeignKey("yield_predictions.id", ondelete="CASCADE"), nullable=False)
    recommendation_type = Column(String(50))
    priority = Column(Integer)
    action_description = Column(String, nullable=False)
    expected_impact = Column(String)
    cost_impact = Column(Float)
    yield_impact = Column(Float)
    timing = Column(String(50))
    resources_needed = Column(String)
    implementation_difficulty = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    yield_prediction = relationship("YieldPrediction", back_populates="optimization_recommendations")
    
    def __repr__(self):
        return f"<OptimizationRecommendation {self.recommendation_type}>"
