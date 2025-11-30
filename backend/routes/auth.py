"""
Simple admin authentication route
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Default for development

class LoginRequest(BaseModel):
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str = None

@router.post("/admin/login/", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    """
    Simple password-based admin authentication
    Returns success status
    """
    if request.password == ADMIN_PASSWORD:
        return LoginResponse(
            success=True,
            message="Login successful",
            token="admin_authenticated"  # Simple token
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

@router.post("/admin/verify/")
async def verify_admin(token: str):
    """
    Verify if admin token is valid
    """
    if token == "admin_authenticated":
        return {"valid": True}
    return {"valid": False}
