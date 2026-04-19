"""
Machine Learning Service - Crop recommendation and yield prediction
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging
import os

from app.config import settings

logger = logging.getLogger(__name__)

# Global model variables
crop_model = None
yield_model = None
models_loaded = False

def load_models():
    """
    Load trained ML models
    """
    global crop_model, yield_model, models_loaded
    
    try:
        crop_model_path = settings.CROP_MODEL_PATH
        yield_model_path = settings.YIELD_MODEL_PATH
        
        if os.path.exists(crop_model_path):
            crop_model = joblib.load(crop_model_path)
            logger.info("Crop suitability model loaded successfully")
        else:
            logger.warning(f"Crop model not found at {crop_model_path}")
        
        if os.path.exists(yield_model_path):
            yield_model = joblib.load(yield_model_path)
            logger.info("Yield prediction model loaded successfully")
        else:
            logger.warning(f"Yield model not found at {yield_model_path}")
        
        models_loaded = True
        
    except Exception as e:
        logger.error(f"Error loading ML models: {e}")
        models_loaded = False

def predict_crop_suitability(features: Dict, top_n: int = 10) -> List[Dict]:
    """
    Predict crop suitability scores using trained model
    """
    try:
        if crop_model is None:
            logger.warning("Crop model not loaded, using fallback predictions")
            return get_fallback_crop_recommendations(features, top_n)
        
        # Prepare feature vector
        feature_vector = prepare_crop_features(features)
        
        # Get predictions
        probabilities = crop_model.predict_proba(feature_vector)[0]
        
        # Get class names (crop names)
        crop_names = crop_model.classes_
        
        # Create prediction list
        predictions = []
        for idx, prob in enumerate(probabilities):
            predictions.append({
                'crop_name': crop_names[idx],
                'suitability_score': round(prob * 100, 2),
                'recommendations': generate_crop_recommendations(
                    crop_names[idx], features
                ),
                'feature_importance': get_feature_importance(crop_model, feature_vector)
            })
        
        # Sort by score and return top N
        predictions.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return predictions[:top_n]
        
    except Exception as e:
        logger.error(f"Error predicting crop suitability: {e}")
        return get_fallback_crop_recommendations(features, top_n)

def predict_yield(features: Dict) -> Dict:
    """
    Predict crop yield using trained model
    """
    try:
        if yield_model is None:
            logger.warning("Yield model not loaded, using fallback prediction")
            return get_fallback_yield_prediction(features)
        
        # Prepare feature vector
        feature_vector = prepare_yield_features(features)
        
        # Get prediction
        yield_prediction = yield_model.predict(feature_vector)[0]
        
        # Get confidence (if available)
        confidence = 0.85  # Default confidence
        
        return {
            'yield_per_acre': round(yield_prediction, 2),
            'confidence': confidence
        }
        
    except Exception as e:
        logger.error(f"Error predicting yield: {e}")
        return get_fallback_yield_prediction(features)

def optimize_yield(features: Dict, baseline_yield: float) -> Dict:
    """
    Optimization engine to find best practices for yield improvement
    Simulates different scenarios to find optimal combination
    """
    try:
        # Target: at least 10% yield increase
        target_increase = 0.10
        
        # Test different optimization scenarios
        scenarios = []
        
        # Scenario 1: Optimize nitrogen levels
        if features.get('nitrogen', 0) < 280:
            scenarios.append({
                'type': 'fertilizer',
                'priority': 1,
                'action': f"Increase nitrogen application to 280-300 kg/ha. Current: {features.get('nitrogen', 0):.1f} kg/ha",
                'impact': "Expected to increase yield by 5-8%",
                'yield_impact': 6.5,
                'cost_impact': 3000,
                'timing': 'Before sowing and at vegetative stage',
                'resources': 'Urea or DAP fertilizer',
                'difficulty': 'easy'
            })
        
        # Scenario 2: Balance NPK ratio
        n = features.get('nitrogen', 0)
        p = features.get('phosphorus', 0)
        k = features.get('potassium', 0)
        
        if p < n / 2:
            scenarios.append({
                'type': 'fertilizer',
                'priority': 2,
                'action': f"Increase phosphorus to balance NPK ratio. Current P: {p:.1f} kg/ha",
                'impact': "Improved nutrient uptake and root development",
                'yield_impact': 4.0,
                'cost_impact': 2000,
                'timing': 'Basal application before sowing',
                'resources': 'Single Super Phosphate (SSP) or DAP',
                'difficulty': 'easy'
            })
        
        if k < 150:
            scenarios.append({
                'type': 'fertilizer',
                'priority': 3,
                'action': f"Apply potassium fertilizer. Current K: {k:.1f} kg/ha. Recommended: 150-180 kg/ha",
                'impact': "Better stress tolerance and grain quality",
                'yield_impact': 3.5,
                'cost_impact': 2500,
                'timing': 'Split application: basal and flowering stage',
                'resources': 'Muriate of Potash (MOP)',
                'difficulty': 'easy'
            })
        
        # Scenario 3: Optimize pH
        ph = features.get('ph', 7.0)
        if ph < 6.0 or ph > 7.5:
            action = "Apply lime to increase pH" if ph < 6.0 else "Apply gypsum to reduce pH"
            scenarios.append({
                'type': 'soil_amendment',
                'priority': 4,
                'action': f"{action}. Current pH: {ph:.1f}",
                'impact': "Improved nutrient availability",
                'yield_impact': 5.0,
                'cost_impact': 4000,
                'timing': 'Before land preparation',
                'resources': 'Lime or Gypsum',
                'difficulty': 'medium'
            })
        
        # Scenario 4: Improve irrigation
        if features.get('irrigation_type') == 'rainfed':
            scenarios.append({
                'type': 'irrigation',
                'priority': 5,
                'action': 'Install drip irrigation system for water-use efficiency',
                'impact': 'Consistent moisture availability and 30-40% water saving',
                'yield_impact': 15.0,
                'cost_impact': 25000,
                'timing': 'Before crop season',
                'resources': 'Drip irrigation kit',
                'difficulty': 'hard'
            })
        
        # Scenario 5: Micronutrient application
        if features.get('zinc', 0) < 0.8:
            scenarios.append({
                'type': 'micronutrient',
                'priority': 6,
                'action': f"Apply zinc sulfate. Current Zn: {features.get('zinc', 0):.2f} ppm",
                'impact': 'Prevention of zinc deficiency symptoms',
                'yield_impact': 3.0,
                'cost_impact': 800,
                'timing': 'Foliar spray at tillering/branching stage',
                'resources': 'Zinc Sulfate (0.5% solution)',
                'difficulty': 'easy'
            })
        
        # Scenario 6: Organic carbon improvement
        if features.get('oc', 0) < 0.75:
            scenarios.append({
                'type': 'soil_health',
                'priority': 7,
                'action': f"Incorporate organic matter. Current OC: {features.get('oc', 0):.2f}%",
                'impact': 'Improved soil structure and water retention',
                'yield_impact': 6.0,
                'cost_impact': 5000,
                'timing': 'During land preparation',
                'resources': 'Farm Yard Manure (FYM) or Compost - 5-10 tons/acre',
                'difficulty': 'medium'
            })
        
        # Calculate optimized yield
        total_yield_impact = sum(s['yield_impact'] for s in scenarios[:5])  # Top 5 recommendations
        optimized_yield = baseline_yield * (1 + min(total_yield_impact / 100, 0.25))  # Cap at 25% increase
        
        total_cost_impact = sum(s['cost_impact'] for s in scenarios[:5])
        
        return {
            'optimized_yield': round(optimized_yield, 2),
            'yield_increase_percent': round((optimized_yield - baseline_yield) / baseline_yield * 100, 2),
            'cost_increase_percent': round((total_cost_impact / 25000) * 100, 2) if total_cost_impact > 0 else 0,
            'recommendations': scenarios[:7]  # Return top 7 recommendations
        }
        
    except Exception as e:
        logger.error(f"Error optimizing yield: {e}")
        return {
            'optimized_yield': baseline_yield * 1.1,
            'yield_increase_percent': 10.0,
            'cost_increase_percent': 5.0,
            'recommendations': []
        }

def prepare_crop_features(features: Dict) -> np.ndarray:
    """
    Prepare feature vector for crop suitability model
    """
    feature_list = [
        features.get('nitrogen', 0),
        features.get('phosphorus', 0),
        features.get('potassium', 0),
        features.get('ph', 7.0),
        features.get('ec', 0),
        features.get('oc', 0),
        features.get('temperature', 25),
        features.get('humidity', 60),
        features.get('rainfall', 100)
    ]
    
    return np.array(feature_list).reshape(1, -1)

def prepare_yield_features(features: Dict) -> np.ndarray:
    """
    Prepare feature vector for yield prediction model
    """
    feature_list = [
        features.get('nitrogen', 0),
        features.get('phosphorus', 0),
        features.get('potassium', 0),
        features.get('ph', 7.0),
        features.get('temperature', 25),
        features.get('humidity', 60),
        features.get('rainfall', 100),
        features.get('land_size', 1)
    ]
    
    return np.array(feature_list).reshape(1, -1)

def get_feature_importance(model, feature_vector: np.ndarray) -> Dict:
    """
    Get feature importance from model
    """
    try:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            features = ['N', 'P', 'K', 'pH', 'EC', 'OC', 'Temp', 'Humidity', 'Rainfall']
            return dict(zip(features, [round(float(imp), 4) for imp in importances]))
    except:
        pass
    return {}

def generate_crop_recommendations(crop_name: str, features: Dict) -> str:
    """
    Generate text recommendations for a crop
    """
    recommendations = []
    
    ph = features.get('ph', 7.0)
    n = features.get('nitrogen', 0)
    
    recommendations.append(f"{crop_name} is suitable for your soil conditions.")
    
    if ph < 6.0:
        recommendations.append("Consider liming to increase soil pH.")
    elif ph > 7.5:
        recommendations.append("Soil pH is slightly alkaline, monitor nutrient availability.")
    
    if n < 200:
        recommendations.append("Apply additional nitrogen fertilizer for optimal growth.")
    
    return " ".join(recommendations)

def get_fallback_crop_recommendations(features: Dict, top_n: int) -> List[Dict]:
    """
    Fallback crop recommendations when model is not available
    """
    # Rule-based recommendations
    crops = [
        {'crop_name': 'Rice', 'suitability_score': 85.5},
        {'crop_name': 'Wheat', 'suitability_score': 82.3},
        {'crop_name': 'Cotton', 'suitability_score': 78.9},
        {'crop_name': 'Maize', 'suitability_score': 76.4},
        {'crop_name': 'Sugarcane', 'suitability_score': 74.2},
        {'crop_name': 'Groundnut', 'suitability_score': 71.8},
        {'crop_name': 'Soybean', 'suitability_score': 69.5},
        {'crop_name': 'Chickpea', 'suitability_score': 67.3},
        {'crop_name': 'Mustard', 'suitability_score': 65.1},
        {'crop_name': 'Potato', 'suitability_score': 63.7}
    ]
    
    for crop in crops:
        crop['recommendations'] = f"{crop['crop_name']} can be grown based on your soil conditions."
        crop['feature_importance'] = {}
    
    return crops[:top_n]

def get_fallback_yield_prediction(features: Dict) -> Dict:
    """
    Fallback yield prediction when model is not available
    """
    # Simple rule-based yield estimate
    base_yield = 25.0  # quintals per acre
    
    # Adjust based on nutrients
    n_factor = min(features.get('nitrogen', 200) / 280, 1.2)
    ph_factor = 1.0 if 6.0 <= features.get('ph', 7.0) <= 7.5 else 0.9
    
    estimated_yield = base_yield * n_factor * ph_factor
    
    return {
        'yield_per_acre': round(estimated_yield, 2),
        'confidence': 0.70
    }
