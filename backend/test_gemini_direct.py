"""Direct test of Gemini Vision API"""
from dotenv import load_dotenv
load_dotenv()

from utils.gemini_vision import analyze_plant_disease

# Test with a public plant disease image URL
test_image_url = "https://res.cloudinary.com/demo/image/upload/v1234567890/sample.jpg"

print("Testing Gemini Vision API...")
print("=" * 50)

try:
    # Use your actual Cloudinary image URL from the upload
    # Replace this with the URL you see in the browser
    image_url = input("Paste your Cloudinary image URL here: ")
    
    result = analyze_plant_disease(image_url)
    
    print("\n✅ SUCCESS!")
    print("=" * 50)
    print(f"Disease Name: {result['disease_name']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Crop Type: {result['crop_type']}")
    print(f"Severity: {result['severity']}")
    print(f"Description: {result['description']}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
