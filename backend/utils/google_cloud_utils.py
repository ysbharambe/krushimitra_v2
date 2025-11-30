"""
Google Cloud Translation and Text-to-Speech utilities
High-quality translation and voice synthesis for Indian languages
"""

import os
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import base64

# Initialize clients
translate_client = None
tts_client = None

def init_google_cloud():
    """Initialize Google Cloud clients"""
    global translate_client, tts_client
    
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if credentials_path and os.path.exists(credentials_path):
        try:
            translate_client = translate.Client()
            tts_client = texttospeech.TextToSpeechClient()
            print("✅ Google Cloud services initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️ Google Cloud initialization failed: {e}")
            return False
    else:
        print("⚠️ Google Cloud credentials not found. Translation and TTS features will be limited.")
        return False

# Initialize on module load
init_google_cloud()

def translate_text(text: str, target_language: str, source_language: str = 'en') -> dict:
    """
    Translate text using Google Cloud Translation API
    
    Args:
        text: Text to translate
        target_language: Target language code (hi, mr, gu, ta, etc.)
        source_language: Source language code (default: en)
    
    Returns:
        dict: {
            'translated_text': str,
            'source_language': str,
            'target_language': str
        }
    """
    
    if not translate_client:
        return {
            'translated_text': text,
            'source_language': source_language,
            'target_language': target_language,
            'error': 'Translation service not available'
        }
    
    try:
        # Translate
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        
        return {
            'translated_text': result['translatedText'],
            'source_language': source_language,
            'target_language': target_language
        }
    
    except Exception as e:
        print(f"Translation error: {e}")
        return {
            'translated_text': text,
            'source_language': source_language,
            'target_language': target_language,
            'error': str(e)
        }

def text_to_speech(text: str, language_code: str = 'en-IN', voice_gender: str = 'NEUTRAL') -> dict:
    """
    Convert text to speech using Google Cloud Text-to-Speech API
    
    Args:
        text: Text to convert to speech
        language_code: Language code (hi-IN, mr-IN, en-IN, etc.)
        voice_gender: Voice gender (MALE, FEMALE, NEUTRAL)
    
    Returns:
        dict: {
            'audio_content': base64 encoded audio,
            'language_code': str
        }
    """
    
    if not tts_client:
        return {
            'error': 'Text-to-Speech service not available'
        }
    
    try:
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Map language codes to proper Google Cloud TTS codes
        language_map = {
            'en': 'en-IN',
            'hi': 'hi-IN',
            'mr': 'mr-IN',
            'gu': 'gu-IN',
            'ta': 'ta-IN',
            'te': 'te-IN',
            'kn': 'kn-IN',
            'bn': 'bn-IN',
            'pa': 'pa-IN',
            'ml': 'ml-IN'
        }
        
        # Get proper language code
        lang_code = language_map.get(language_code.split('-')[0], 'en-IN')
        
        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, voice_gender)
        )
        
        # Select the audio config
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,  # Slightly slower for better understanding
            pitch=0.0
        )
        
        # Perform the text-to-speech request
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Encode audio content to base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        
        return {
            'audio_content': audio_base64,
            'language_code': lang_code,
            'format': 'mp3'
        }
    
    except Exception as e:
        print(f"TTS error: {e}")
        return {
            'error': str(e)
        }

def is_google_cloud_available() -> bool:
    """Check if Google Cloud services are available"""
    return translate_client is not None and tts_client is not None
