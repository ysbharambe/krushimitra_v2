"""
Gemini Vision API Integration for Plant Disease Detection
High-quality AI-powered disease identification
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Optional
import requests
from PIL import Image
from io import BytesIO

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
MODEL_NAME = "gemini-2.0-flash"  # Latest stable multimodal model

def analyze_plant_disease(image_url: str) -> Dict:
    """
    Analyze plant image for disease detection using Gemini Vision
    
    Args:
        image_url: URL of the plant image
    
    Returns:
        dict: {
            'disease_name': str,
            'confidence': float,
            'crop_type': str,
            'severity': str,
            'description': str
        }
    """
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured in environment variables")
    
    try:
        # Download image
        print(f"📥 Downloading image from: {image_url}")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        print(f"✅ Image loaded successfully")
        
        # Create model instance
        print(f"🤖 Initializing Gemini model: {MODEL_NAME}")
        model = genai.GenerativeModel(MODEL_NAME)
        print(f"✅ Model initialized")
        
        # Craft detailed prompt for plant disease detection
        prompt = """You are an agricultural advisor helping Indian farmers. Analyze this plant image and provide a simple disease diagnosis.

IMPORTANT: Use SIMPLE language that a farmer with basic education can understand. Avoid technical/scientific terms.

Respond ONLY in valid JSON format (no markdown, no extra text):

{
  "disease_name": "Tomato Early blight",
  "confidence": 85.5,
  "crop_type": "Tomato",
  "severity": "Medium",
  "description": "Your plant leaves have brown spots and are turning yellow. This disease spreads when leaves stay wet. It can reduce your crop yield if not treated soon."
}

Guidelines:
- disease_name: Use simple names with spaces, NOT underscores (e.g., "Tomato Early blight", NOT "Tomato_Early_blight")
- crop_type: Simple crop name (Tomato, Potato, Corn, etc.)
- severity: Low (just starting), Medium (spreading), High (very bad)
- description: Explain in SIMPLE Hindi-English words what the farmer can SEE and what will HAPPEN. Use short sentences. Avoid scientific terms like "pathogen", "fungal infection" - instead say "disease", "fungus", "germs".

Example descriptions:
- BAD: "Fungal pathogen causing necrotic lesions on foliar tissues"
- GOOD: "Your plant has a fungus disease. Brown dead spots appear on leaves. Leaves will fall if not treated."

Provide ONLY the JSON response."""
        
        # Generate response
        response = model.generate_content([prompt, img])
        
        # Parse response
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
        
        # Parse JSON
        result = json.loads(result_text)
        
        # Validate and format response
        disease_name = result.get('disease_name', 'Unknown')
        confidence = float(result.get('confidence', 0))
        
        return {
            'disease_name': disease_name,
            'confidence': round(confidence, 2),
            'crop_type': result.get('crop_type', 'Unknown'),
            'severity': result.get('severity', 'Unknown'),
            'description': result.get('description', 'No description available'),
            'source': 'gemini_vision'
        }
        
    except json.JSONDecodeError as e:
        # Fallback parsing if JSON fails
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {result_text}")
        
        # Try to extract information from text
        return {
            'disease_name': 'Analysis_Failed',
            'confidence': 0.0,
            'crop_type': 'Unknown',
            'severity': 'Unknown',
            'description': 'Unable to parse Gemini response',
            'source': 'gemini_vision',
            'raw_response': result_text
        }
        
    except Exception as e:
        print(f"Gemini Vision error: {e}")
        raise Exception(f"Failed to analyze image with Gemini: {str(e)}")

def get_detailed_recommendations(disease_name: str, crop_type: str) -> Dict:
    """
    Get detailed treatment recommendations using Gemini
    
    Args:
        disease_name: Name of the detected disease
        crop_type: Type of crop
    
    Returns:
        dict: Treatment recommendations
    """
    
    if not GEMINI_API_KEY:
        return None
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        prompt = f"""You are helping an Indian farmer treat their crop disease. Use SIMPLE language that a farmer with basic education can understand.

Disease: {disease_name}
Crop: {crop_type}

Give REAL medicine names available in India. Use SIMPLE HINDI-ENGLISH words. NO scientific terms.

Respond ONLY in JSON format (no markdown):
{{
  "chemical_treatment": {{
    "name": "Medicine name (e.g., 'Mancozeb' or 'Copper spray')",
    "active_ingredient": "Main ingredient",
    "description": "What it does (use simple words: kills fungus, stops disease spread, protects plant)",
    "application_steps": "Simple steps: 1) Mix 2 spoon in 1 liter water. 2) Spray on leaves in morning. 3) Repeat after 7 days.",
    "where_to_buy": "Local fertilizer shop, Krishi Kendra, BigHaat app, AgroStar app",
    "precautions": "Wear gloves. Don't spray in afternoon sun. Wash hands after use."
  }},
  "organic_treatment": {{
    "name": "Natural treatment (e.g., 'Neem oil', 'Cow urine mix', 'Turmeric powder')",
    "ingredients": "What you need",
    "description": "How it helps your plant",
    "application_steps": "Simple steps: 1) Take ingredients. 2) Mix with water. 3) Spray on plant.",
    "effectiveness": "When you will see results (e.g., 'Disease reduces in 1 week', 'Plant becomes healthy in 10 days')"
  }},
  "preventive_measures": [
    "Remove bad leaves from plant",
    "Don't water leaves, water the soil only",
    "Keep space between plants for air",
    "Check plants every 2-3 days"
  ]
}}

IMPORTANT: 
- Use SIMPLE words: "medicine" not "fungicide", "spray" not "apply", "bad leaves" not "infected foliage"
- Give REAL product names available in Indian agriculture shops
- Write like you're talking to a farmer friend
- Use Hindi-English mix if helpful (e.g., "pani" for water, "dawai" for medicine)"""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        recommendations = json.loads(result_text)
        return recommendations
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return None

def is_gemini_configured() -> bool:
    """Check if Gemini API is properly configured"""
    return bool(GEMINI_API_KEY)
