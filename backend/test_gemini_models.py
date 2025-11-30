"""Test which Gemini models are available"""
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("Available Gemini Models:")
print("=" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Description: {model.description}")
        print(f"  Supports: {model.supported_generation_methods}")
        print()
