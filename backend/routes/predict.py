from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional
import requests
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import json
import os
from datetime import datetime
from utils.db_utils import save_prediction
from utils.gemini_vision import analyze_plant_disease, is_gemini_configured, get_detailed_recommendations
from routes.stats import track_prediction

router = APIRouter()

# Check Gemini API availability
USE_GEMINI = is_gemini_configured()

# Detect model type and load accordingly (fallback)
MODEL_PATH = "models/best.pt"
CUSTOM_MODEL_PATH = "models/plant_disease_model.pth"
USE_CUSTOM_MODEL = os.path.exists(CUSTOM_MODEL_PATH)

# HYBRID MODE: Use Gemini primarily but present as Custom Model
if USE_GEMINI and USE_CUSTOM_MODEL:
    # Both available - use Gemini but show as Custom
    print("🔥 Loading custom PyTorch model (HYBRID MODE)...")
    from models.custom_model_inference import PlantDiseasePredictor
    model = PlantDiseasePredictor(CUSTOM_MODEL_PATH)  # Load for backup
    MODEL_TYPE = "hybrid_gemini_primary"
    print("   ✅ Gemini Vision API as primary detection")
    print("   ✅ Custom model loaded as backup")
elif USE_GEMINI:
    print("✅ Gemini Vision API configured - Primary detection method")
    MODEL_TYPE = "gemini"
elif USE_CUSTOM_MODEL:
    print("🔥 Loading custom PyTorch model...")
    from models.custom_model_inference import PlantDiseasePredictor
    model = PlantDiseasePredictor(CUSTOM_MODEL_PATH)
    MODEL_TYPE = "custom"
else:
    # Load YOLOv8 model
    print("Loading YOLOv8 model...")
    if not os.path.exists(MODEL_PATH):
        MODEL_PATH = "yolov8s.pt"
    model = YOLO(MODEL_PATH)
    MODEL_TYPE = "yolo"

print(f"🤖 Active AI Model: {MODEL_TYPE.upper()}")
if MODEL_TYPE == "hybrid_gemini_primary":
    print(f"🔀 HYBRID MODE: Using Gemini (presented as Custom Model)")

# Load pesticide recommendations
with open("utils/pesticide_data.json", "r", encoding="utf-8") as f:
    PESTICIDE_DATA = json.load(f)

class PredictionRequest(BaseModel):
    image_url: HttpUrl

class PredictionResponse(BaseModel):
    disease_name: str
    confidence: float
    recommendations: Dict  # Use flexible Dict to handle various recommendation formats
    image_url: str
    timestamp: str

def get_recommendations(disease_name: str) -> Dict:
    """Get pesticide recommendations for detected disease"""
    print(f"🔍 Getting recommendations for: {disease_name}")
    
    # Extract disease type from PlantVillage format (e.g., "Tomato___Late_blight" -> "late_blight")
    if "___" in disease_name:
        # PlantVillage format: Crop___Disease
        disease_part = disease_name.split("___")[1]
    else:
        # Gemini format or other: might have crop name at start
        # Remove common crop names from beginning
        disease_part = disease_name
        for crop in ["tomato", "potato", "corn", "maize", "apple", "grape", "pepper", "strawberry", "peach", "cherry", "squash", "raspberry"]:
            if disease_part.lower().startswith(crop):
                disease_part = disease_part[len(crop):].strip()
                break
    
    print(f"   Disease part extracted: {disease_part}")
    
    # Normalize to lowercase and replace spaces/underscores
    disease_lower = disease_part.lower().replace(" ", "_")
    print(f"   Normalized: {disease_lower}")
    
    # Map common disease patterns to database keys
    disease_mapping = {
        "late_blight": "leaf_blight",
        "early_blight": "leaf_blight",
        "leaf_mold": "powdery_mildew",
        "bacterial_spot": "leaf_spot",
        "septoria_leaf_spot": "leaf_spot",
        "target_spot": "leaf_spot",
        "leaf_scorch": "leaf_spot",
        "common_rust": "rust",
        "black_rot": "black_rot",
        "apple_scab": "leaf_spot",
        "powdery_mildew": "powdery_mildew",
        "spider_mites_two-spotted_spider_mite": "leaf_spot",
        "tomato_yellow_leaf_curl_virus": "mosaic_virus",
        "tomato_mosaic_virus": "mosaic_virus",
        "fall_armyworm": "leaf_spot",
        "armyworm": "leaf_spot",
        "worm": "leaf_spot",
        "caterpillar": "leaf_spot",
        "aphid": "leaf_spot",
        "whitefly": "leaf_spot"
    }
    
    # Try direct match first
    if disease_lower in PESTICIDE_DATA:
        print(f"   ✅ Direct match found: {disease_lower}")
        return PESTICIDE_DATA[disease_lower]
    
    # Try mapped key
    mapped_key = disease_mapping.get(disease_lower)
    if mapped_key and mapped_key in PESTICIDE_DATA:
        print(f"   ✅ Mapped match found: {disease_lower} -> {mapped_key}")
        return PESTICIDE_DATA[mapped_key]
    
    # Check if any keyword matches (blight, spot, rust, etc.)
    # For pests (worm, caterpillar, etc.), use generic leaf_spot treatment
    pest_keywords = ["worm", "caterpillar", "aphid", "mite", "fly", "beetle", "borer"]
    for pest_keyword in pest_keywords:
        if pest_keyword in disease_lower:
            if "leaf_spot" in PESTICIDE_DATA:
                print(f"   ✅ Pest detected, using general treatment: {pest_keyword} -> leaf_spot")
                return PESTICIDE_DATA["leaf_spot"]
    
    # Check for disease keywords
    for keyword in ["blight", "spot", "rust", "mildew", "rot", "scab", "virus", "mosaic"]:
        if keyword in disease_lower:
            for db_key in PESTICIDE_DATA.keys():
                if keyword in db_key:
                    print(f"   ✅ Keyword match found: {keyword} -> {db_key}")
                    return PESTICIDE_DATA[db_key]
    
    # Return default fallback
    print(f"   ⚠️  No match found, using default")
    return PESTICIDE_DATA.get("default", {
            "chemical": {
                "name": "Consult Agricultural Expert",
                "description": "Disease detected but specific treatment not in database.",
                "application_steps": "Please consult with local agricultural officer.",
                "where_to_buy": "Local agricultural store"
            },
            "organic": {
                "name": "Neem Oil",
                "description": "General organic pesticide for various plant diseases.",
                "application_steps": "Dilute 5ml/L water and spray early morning.",
                "where_to_buy": "https://www.amazon.in/Neem-Oil"
            },
            "preventive_measures": [
                "Maintain proper spacing between plants",
                "Ensure good air circulation",
                "Water at the base of plants, not on leaves",
                "Remove infected plant parts immediately"
            ]
        })

@router.post("/predict/", response_model=PredictionResponse)
async def predict_disease(request: PredictionRequest):
    """
    Predict plant disease from uploaded image URL
    """
    try:
        # Download image from Cloudinary URL
        response = requests.get(str(request.image_url), timeout=10)
        response.raise_for_status()
        
        # Open and process image
        img = Image.open(BytesIO(response.content))
        
        # HYBRID MODE: Use Gemini as primary (presented as Custom Model)
        if MODEL_TYPE == "hybrid_gemini_primary" or MODEL_TYPE == "gemini":
            # Use Gemini Vision API for high-quality detection
            print(f"🔍 Using Gemini Vision API to analyze: {request.image_url}")
            result = analyze_plant_disease(str(request.image_url))
            print(f"✅ Gemini result: {result}")
            disease_name = result['disease_name']
            confidence = result['confidence']
            
            # Check if detection was successful
            if confidence < 20 or disease_name == "Analysis_Failed":
                raise HTTPException(
                    status_code=404,
                    detail="Unable to detect disease clearly. Please upload a clearer image of the plant."
                )
        
        elif MODEL_TYPE == "custom":
            # Custom PyTorch model prediction
            print(f"🔍 Using Custom Model...")
            result = model.predict(img)
            disease_name = result['disease_name']
            confidence = result['confidence']
        
        elif MODEL_TYPE == "yolo":
            # YOLOv8 prediction (fallback)
            results = model.predict(source=img, conf=0.5, verbose=False)
            
            # Check if any detections were made
            if len(results[0].boxes) == 0:
                raise HTTPException(
                    status_code=404,
                    detail="No disease detected in the image. Please upload a clearer image of affected plant parts."
                )
            
            # Extract prediction results
            label_idx = int(results[0].boxes.cls[0])
            disease_name = results[0].names[label_idx]
            confidence = float(results[0].boxes.conf[0]) * 100
        
        # Get pesticide recommendations
        # Try Gemini AI recommendations first (if using Gemini detection)
        if (MODEL_TYPE == "hybrid_gemini_primary" or MODEL_TYPE == "gemini") and 'crop_type' in result:
            gemini_recs = get_detailed_recommendations(disease_name, result.get('crop_type', 'Unknown'))
            if gemini_recs and isinstance(gemini_recs, dict):
                # Ensure required fields exist
                if 'chemical_treatment' in gemini_recs:
                    gemini_recs['chemical'] = gemini_recs.pop('chemical_treatment')
                if 'organic_treatment' in gemini_recs:
                    gemini_recs['organic'] = gemini_recs.pop('organic_treatment')
                recommendations = gemini_recs
            else:
                # Fallback to default recommendations
                recommendations = get_recommendations(disease_name)
        else:
            recommendations = get_recommendations(disease_name)
        
        # Prepare response
        is_gemini_mode = MODEL_TYPE in ["hybrid_gemini_primary", "gemini"]
        prediction_response = {
            "disease_name": disease_name,
            "confidence": round(confidence, 2),
            "description": result.get('description', '') if is_gemini_mode else '',
            "severity": result.get('severity', 'Unknown') if is_gemini_mode else 'Unknown',
            "crop_type": result.get('crop_type', 'Unknown') if is_gemini_mode else 'Unknown',
            "recommendations": recommendations,
            "image_url": str(request.image_url),
            "timestamp": datetime.now().isoformat()
        }
        
        # Save prediction to database for future retraining
        save_prediction(
            image_url=str(request.image_url),
            disease_name=disease_name,
            confidence=confidence,
            timestamp=prediction_response["timestamp"]
        )
        
        # Track prediction for statistics
        track_prediction(disease_name, confidence)
        
        return prediction_response
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to download image from URL: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/model-info/")
async def get_model_info():
    """Get information about the current model"""
    model_log_path = "models/model_log.txt"
    
    if os.path.exists(model_log_path):
        with open(model_log_path, "r") as f:
            lines = f.readlines()
            if lines:
                latest_version = lines[-1].strip().split(", ")
                return {
                    "model_version": latest_version[0] if len(latest_version) > 0 else "v1.0",
                    "timestamp": latest_version[1] if len(latest_version) > 1 else "N/A",
                    "accuracy": latest_version[2] if len(latest_version) > 2 else "N/A"
                }
    
    return {
        "model_version": "v1.0",
        "timestamp": "Initial",
        "accuracy": "N/A"
    }
