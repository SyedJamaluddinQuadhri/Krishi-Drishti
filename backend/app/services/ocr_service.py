"""
OCR Service - Extract soil health data from images using Pytesseract
"""

try:
    import pytesseract
    import cv2
    import numpy as np
    from PIL import Image
    _OCR_AVAILABLE = True
except ImportError:
    _OCR_AVAILABLE = False
    pytesseract = None
    cv2 = None
    np = None
    Image = None
import re
import logging
from typing import Tuple, Dict

from app.config import settings

logger = logging.getLogger(__name__)

# Configure Tesseract path only if available
if _OCR_AVAILABLE and pytesseract is not None:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

async def extract_shc_data(image_path: str) -> Tuple[Dict, float]:
    """
    Extract soil health card data from image using OCR
    Returns: (extracted_data dict, confidence score)
    """
    if not _OCR_AVAILABLE:
        logger.error("OCR packages (pytesseract, opencv-python, Pillow) not installed. Cannot extract SHC data.")
        return {}, 0.0

    try:
        # Preprocess image
        processed_image = preprocess_image(image_path)
        
        # Extract text using OCR
        custom_config = r'--oem 3 --psm 6 -l ' + settings.OCR_LANGUAGES
        ocr_data = pytesseract.image_to_data(
            processed_image,
            config=custom_config,
            output_type=pytesseract.Output.DICT
        )
        
        # Get raw text
        raw_text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        logger.info(f"OCR extracted text length: {len(raw_text)}")
        
        # Parse extracted text
        extracted_data = parse_shc_text(raw_text)
        
        # Calculate average confidence
        confidences = [int(conf) for conf in ocr_data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        logger.info(f"OCR extraction completed with confidence: {avg_confidence:.2f}%")
        
        return extracted_data, round(avg_confidence, 2)
        
    except Exception as e:
        logger.error(f"OCR extraction error: {e}")
        return {}, 0.0

def preprocess_image(image_path: str) -> 'np.ndarray':
    """
    Preprocess image for better OCR accuracy
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        
        # Dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.dilate(thresh, kernel, iterations=1)
        processed = cv2.erode(processed, kernel, iterations=1)
        
        # Increase contrast
        processed = cv2.convertScaleAbs(processed, alpha=1.5, beta=0)
        
        return processed
        
    except Exception as e:
        logger.error(f"Image preprocessing error: {e}")
        # Return original image if preprocessing fails
        return cv2.imread(image_path)

def parse_shc_text(text: str) -> Dict:
    """
    Parse OCR text to extract soil health parameters
    Uses regex patterns to find common SHC field names and values
    """
    data = {}
    
    # Convert to lowercase for easier matching
    text_lower = text.lower()
    
    # Patterns for each nutrient/parameter
    patterns = {
        'nitrogen': [
            r'nitrogen\s*[:\-]?\s*(\d+\.?\d*)',
            r'n\s*[:\-]?\s*(\d+\.?\d*)\s*kg',
            r'available\s*n\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'phosphorus': [
            r'phosphorus\s*[:\-]?\s*(\d+\.?\d*)',
            r'p\s*[:\-]?\s*(\d+\.?\d*)\s*kg',
            r'available\s*p\s*[:\-]?\s*(\d+\.?\d*)',
            r'p2o5\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'potassium': [
            r'potassium\s*[:\-]?\s*(\d+\.?\d*)',
            r'k\s*[:\-]?\s*(\d+\.?\d*)\s*kg',
            r'available\s*k\s*[:\-]?\s*(\d+\.?\d*)',
            r'k2o\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'ph_value': [
            r'ph\s*[:\-]?\s*(\d+\.?\d*)',
            r'ph\s*value\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'electrical_conductivity': [
            r'ec\s*[:\-]?\s*(\d+\.?\d*)',
            r'electrical\s*conductivity\s*[:\-]?\s*(\d+\.?\d*)',
            r'e\.c\.\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'organic_carbon': [
            r'organic\s*carbon\s*[:\-]?\s*(\d+\.?\d*)',
            r'oc\s*[:\-]?\s*(\d+\.?\d*)',
            r'o\.c\.\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'sulphur': [
            r'sulphur\s*[:\-]?\s*(\d+\.?\d*)',
            r'sulfur\s*[:\-]?\s*(\d+\.?\d*)',
            r's\s*[:\-]?\s*(\d+\.?\d*)\s*(?:kg|ppm)'
        ],
        'zinc': [
            r'zinc\s*[:\-]?\s*(\d+\.?\d*)',
            r'zn\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'iron': [
            r'iron\s*[:\-]?\s*(\d+\.?\d*)',
            r'fe\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'copper': [
            r'copper\s*[:\-]?\s*(\d+\.?\d*)',
            r'cu\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'manganese': [
            r'manganese\s*[:\-]?\s*(\d+\.?\d*)',
            r'mn\s*[:\-]?\s*(\d+\.?\d*)'
        ],
        'boron': [
            r'boron\s*[:\-]?\s*(\d+\.?\d*)',
            r'b\s*[:\-]?\s*(\d+\.?\d*)'
        ]
    }
    
    # Try to extract each parameter
    for param, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = float(match.group(1))
                    data[param] = value
                    break
                except (ValueError, IndexError):
                    continue
    
    logger.info(f"Parsed {len(data)} parameters from OCR text")
    
    return data
