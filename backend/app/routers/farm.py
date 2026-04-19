"""
Farm management router
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.utils.logger import setup_logger

# Optional import for geo types; handle missing package gracefully
try:
    from geoalchemy2.elements import WKTElement
    _GEOALCHEMY_AVAILABLE = True
except ImportError:
    WKTElement = None
    _GEOALCHEMY_AVAILABLE = False
from typing import Optional
import uuid
import os
import shutil

from app.database import get_db
from app.schemas.farm import FarmCreate, FarmResponse, SoilHealthCardCreate, SoilHealthCardResponse, SHCUploadResponse
from app.models.farm import Farm, SoilHealthCard
from app.models.user import User
from app.services.ocr_service import extract_shc_data
from app.utils.jwt import get_current_user
from app.config import settings
logger = setup_logger(__name__)
router = APIRouter()

@router.post("/create", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
async def create_farm(
    farm_data: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new farm with location data
    """
    try:
        # Create PostGIS point from lat/lon
        if not _GEOALCHEMY_AVAILABLE or WKTElement is None:
            logger.error("geoalchemy2 not installed - can't create PostGIS geometry. Install with: pip install geoalchemy2")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Server missing geoalchemy2 dependency; please install geoalchemy2.")

        location_wkt = f'POINT({farm_data.longitude} {farm_data.latitude})'

        farm = Farm(
            user_id=current_user.id,
            farm_name=farm_data.farm_name,
            location=WKTElement(location_wkt, srid=4326),
            latitude=farm_data.latitude,
            longitude=farm_data.longitude,
            size=farm_data.size,
            size_unit=farm_data.size_unit,
            soil_type=farm_data.soil_type,
            irrigation_type=farm_data.irrigation_type,
            region=farm_data.region,
            district=farm_data.district,
            state=farm_data.state
        )
        
        db.add(farm)
        db.commit()
        db.refresh(farm)
        
        logger.info(f"Farm created: {farm.id} for user {current_user.id}")
        
        return FarmResponse.model_validate(farm)
        
    except Exception as e:
        logger.error(f"Error creating farm: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/upload_shc", response_model=SHCUploadResponse)
async def upload_soil_health_card(
    farm_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload Soil Health Card image and extract data using OCR
    """
    try:
        # Validate farm ownership
        farm = db.query(Farm).filter(
            Farm.id == uuid.UUID(farm_id),
            Farm.user_id == current_user.id
        ).first()
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        # Validate file type
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract data using OCR
        extracted_data, confidence = await extract_shc_data(file_path)
        
        # Create SHC record
        shc = SoilHealthCard(
            farm_id=farm.id,
            image_path=file_path,
            image_url=f"/uploads/{file_name}",
            nitrogen=extracted_data.get('nitrogen'),
            phosphorus=extracted_data.get('phosphorus'),
            potassium=extracted_data.get('potassium'),
            ph_value=extracted_data.get('ph_value'),
            electrical_conductivity=extracted_data.get('electrical_conductivity'),
            organic_carbon=extracted_data.get('organic_carbon'),
            sulphur=extracted_data.get('sulphur'),
            zinc=extracted_data.get('zinc'),
            iron=extracted_data.get('iron'),
            copper=extracted_data.get('copper'),
            manganese=extracted_data.get('manganese'),
            boron=extracted_data.get('boron'),
            ocr_confidence=confidence,
            is_verified=False
        )
        
        db.add(shc)
        db.commit()
        db.refresh(shc)
        
        logger.info(f"SHC uploaded: {shc.id} for farm {farm.id}")
        
        return SHCUploadResponse(
            success=True,
            message="Soil Health Card uploaded successfully. Please verify the extracted data.",
            shc_id=str(shc.id),
            extracted_data=SoilHealthCardCreate(**extracted_data),
            ocr_confidence=confidence,
            image_url=shc.image_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading SHC: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/verify_shc/{shc_id}", response_model=SoilHealthCardResponse)
async def verify_soil_health_card(
    shc_id: str,
    shc_data: SoilHealthCardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Verify and update extracted SHC data
    """
    try:
        # Find SHC
        shc = db.query(SoilHealthCard).join(Farm).filter(
            SoilHealthCard.id == uuid.UUID(shc_id),
            Farm.user_id == current_user.id
        ).first()
        
        if not shc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Soil Health Card not found"
            )
        
        # Update SHC data
        for field, value in shc_data.dict(exclude_unset=True).items():
            setattr(shc, field, value)
        
        shc.is_verified = True
        
        db.commit()
        db.refresh(shc)
        
        logger.info(f"SHC verified: {shc.id}")
        
        return SoilHealthCardResponse.model_validate(shc)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying SHC: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/farms", response_model=list[FarmResponse])
async def get_user_farms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all farms for current user
    """
    farms = db.query(Farm).filter(Farm.user_id == current_user.id).all()
    return [FarmResponse.model_validate(farm) for farm in farms]

@router.get("/shc/{farm_id}", response_model=SoilHealthCardResponse)
async def get_latest_shc(
    farm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get latest Soil Health Card for a farm
    """
    shc = db.query(SoilHealthCard).join(Farm).filter(
        SoilHealthCard.farm_id == uuid.UUID(farm_id),
        Farm.user_id == current_user.id
    ).order_by(SoilHealthCard.created_at.desc()).first()
    
    if not shc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Soil Health Card found for this farm"
        )
    
    return SoilHealthCardResponse.model_validate(shc)
