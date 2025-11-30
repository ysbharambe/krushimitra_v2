import cloudinary
import cloudinary.uploader
from typing import Optional

# Note: Configure these via environment variables
# CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

def configure_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    """Configure Cloudinary with credentials"""
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )

def upload_image(image_path: str, folder: str = "krushimitra") -> Optional[str]:
    """Upload image to Cloudinary and return secure URL"""
    try:
        response = cloudinary.uploader.upload(
            image_path,
            folder=folder,
            resource_type="image"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return None
