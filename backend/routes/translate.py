from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from deep_translator import GoogleTranslator
from utils.google_cloud_utils import translate_text as gc_translate, text_to_speech, is_google_cloud_available

router = APIRouter()

# Supported languages for Indian farmers
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "bn": "Bengali",
    "pa": "Punjabi",
    "ml": "Malayalam"
}

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "en"

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

class BulkTranslateRequest(BaseModel):
    texts: Dict[str, str]  # key: value pairs to translate
    target_language: str
    source_language: str = "en"

@router.get("/languages/")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "supported_languages": SUPPORTED_LANGUAGES,
        "total_count": len(SUPPORTED_LANGUAGES)
    }

@router.post("/translate/", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text from source language to target language
    """
    try:
        # Validate target language
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Target language '{request.target_language}' not supported. Supported languages: {list(SUPPORTED_LANGUAGES.keys())}"
            )
        
        # Skip translation if source and target are same
        if request.source_language == request.target_language:
            return TranslateResponse(
                original_text=request.text,
                translated_text=request.text,
                source_language=request.source_language,
                target_language=request.target_language
            )
        
        # Try Google Cloud Translation first (better quality for Indian languages)
        if is_google_cloud_available():
            result = gc_translate(
                text=request.text,
                target_language=request.target_language,
                source_language=request.source_language
            )
            translated = result.get('translated_text', request.text)
        else:
            # Fallback to deep-translator
            translated = GoogleTranslator(
                source=request.source_language,
                target=request.target_language
            ).translate(request.text)
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated,
            source_language=request.source_language,
            target_language=request.target_language
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )

@router.post("/translate/bulk/")
async def translate_bulk(request: BulkTranslateRequest):
    """
    Translate multiple text fields at once
    Useful for translating entire disease prediction response
    """
    try:
        # Validate target language
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Target language '{request.target_language}' not supported"
            )
        
        translated_texts = {}
        
        # Skip translation if source and target are same
        if request.source_language == request.target_language:
            return {
                "original_texts": request.texts,
                "translated_texts": request.texts,
                "source_language": request.source_language,
                "target_language": request.target_language
            }
        
        # Translate each text using deep-translator
        translator = GoogleTranslator(
            source=request.source_language,
            target=request.target_language
        )
        for key, text in request.texts.items():
            translated_texts[key] = translator.translate(text)
        
        return {
            "original_texts": request.texts,
            "translated_texts": translated_texts,
            "source_language": request.source_language,
            "target_language": request.target_language
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bulk translation failed: {str(e)}"
        )

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice_gender: str = "NEUTRAL"

@router.post("/text-to-speech/")
async def generate_speech(request: TTSRequest):
    """
    Convert text to speech using Google Cloud Text-to-Speech
    Returns base64 encoded MP3 audio
    """
    try:
        # Validate language
        if request.language.split('-')[0] not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{request.language}' not supported"
            )
        
        # Generate speech using Google Cloud TTS
        result = text_to_speech(
            text=request.text,
            language_code=request.language,
            voice_gender=request.voice_gender
        )
        
        if 'error' in result:
            raise HTTPException(
                status_code=500,
                detail=f"TTS generation failed: {result['error']}"
            )
        
        return {
            "audio_content": result['audio_content'],
            "language_code": result['language_code'],
            "format": result['format']
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TTS failed: {str(e)}"
        )
