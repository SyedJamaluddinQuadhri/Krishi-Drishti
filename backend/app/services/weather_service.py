"""
Weather Service - Fetch weather data from OpenWeatherMap or IMD API
"""

import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

from app.config import settings
from app.models.weather import WeatherCache

logger = logging.getLogger(__name__)

async def get_weather_data(latitude: float, longitude: float, db: Session) -> dict:
    """
    Get weather data with caching
    """
    try:
        # Check cache first
        cache = db.query(WeatherCache).filter(
            WeatherCache.latitude == latitude,
            WeatherCache.longitude == longitude,
            WeatherCache.expires_at > datetime.utcnow()
        ).first()
        
        if cache:
            logger.info(f"Weather data retrieved from cache for {latitude},{longitude}")
            return cache.weather_data
        
        # Fetch fresh data
        weather_data = await fetch_weather_from_api(latitude, longitude)
        
        # Save to cache
        new_cache = WeatherCache(
            latitude=latitude,
            longitude=longitude,
            weather_data=weather_data,
            expires_at=datetime.utcnow() + timedelta(hours=settings.WEATHER_CACHE_HOURS)
        )
        
        db.add(new_cache)
        db.commit()
        
        return weather_data
        
    except Exception as e:
        logger.error(f"Error getting weather data: {e}")
        # Return default values as fallback
        return get_default_weather()

async def fetch_weather_from_api(latitude: float, longitude: float) -> dict:
    """
    Fetch weather data from OpenWeatherMap API
    """
    try:
        if not settings.WEATHER_API_KEY:
            logger.warning("Weather API key not configured")
            return get_default_weather()
        
        url = f"{settings.WEATHER_API_URL}/weather"
        
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Also get forecast
                forecast_url = f"{settings.WEATHER_API_URL}/forecast"
                forecast_response = await client.get(forecast_url, params=params)
                forecast_data = forecast_response.json() if forecast_response.status_code == 200 else {}
                
                # Calculate average rainfall from forecast
                rainfall = 0
                if forecast_data.get('list'):
                    rain_values = [item.get('rain', {}).get('3h', 0) for item in forecast_data['list'][:8]]
                    rainfall = sum(rain_values)
                
                weather_data = {
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'temp_min': data['main']['temp_min'],
                    'temp_max': data['main']['temp_max'],
                    'pressure': data['main']['pressure'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'clouds': data['clouds']['all'],
                    'rainfall': rainfall,
                    'weather_main': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description'],
                    'location': data['name'],
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                logger.info(f"Weather data fetched from API for {latitude},{longitude}")
                return weather_data
            else:
                logger.error(f"Weather API error: {response.status_code}")
                return get_default_weather()
                
    except Exception as e:
        logger.error(f"Error fetching weather from API: {e}")
        return get_default_weather()

def get_default_weather() -> dict:
    """
    Return default weather values as fallback
    """
    return {
        'temperature': 25.0,
        'humidity': 60.0,
        'rainfall': 100.0,
        'wind_speed': 5.0,
        'clouds': 50,
        'weather_main': 'Clear',
        'weather_description': 'Default weather data',
        'timestamp': datetime.utcnow().isoformat()
    }
