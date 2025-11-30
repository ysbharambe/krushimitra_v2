"""
Feedback route for collecting user feedback
Sends feedback to email and stores locally
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

router = APIRouter()

FEEDBACK_EMAIL = "yashbharambe.ai@gmail.com"
FEEDBACK_FILE = "feedback_data.json"

class FeedbackRequest(BaseModel):
    name: str
    email: EmailStr
    rating: int
    message: str
    timestamp: str

@router.post("/feedback/")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit feedback from users
    Saves to local file and attempts to send email
    """
    try:
        # Save feedback to local file
        feedback_data = feedback.dict()
        
        # Load existing feedback
        feedbacks = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                try:
                    feedbacks = json.load(f)
                except json.JSONDecodeError:
                    feedbacks = []
        
        # Add new feedback
        feedbacks.append(feedback_data)
        
        # Save updated feedback
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, indent=2, ensure_ascii=False)
        
        # Prepare email content
        email_subject = f"KrushiMitra Feedback - {feedback.rating} stars from {feedback.name}"
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #2d6a4f; border-bottom: 2px solid #2d6a4f; padding-bottom: 10px;">
                    New Feedback Received
                </h2>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Name:</strong> {feedback.name}</p>
                    <p><strong>Email:</strong> {feedback.email}</p>
                    <p><strong>Rating:</strong> {'⭐' * feedback.rating} ({feedback.rating}/5)</p>
                    <p><strong>Date:</strong> {feedback.timestamp}</p>
                </div>
                
                <div style="background-color: #fff; padding: 15px; border-left: 4px solid #2d6a4f; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2d6a4f;">Message:</h3>
                    <p style="white-space: pre-wrap;">{feedback.message}</p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px;">
                    <p>This feedback was submitted through KrushiMitra - Plant Disease Detection System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Try to send email (optional - won't fail if email server not configured)
        try:
            # Note: Email sending requires SMTP configuration
            # For now, we'll just save the feedback locally
            # You can configure SMTP later if needed
            print(f"📧 Feedback saved from {feedback.name} ({feedback.rating} stars)")
        except Exception as email_error:
            print(f"Email sending failed (feedback saved locally): {email_error}")
        
        return {
            "status": "success",
            "message": "Thank you for your feedback!",
            "feedback_id": len(feedbacks)
        }
        
    except Exception as e:
        print(f"Feedback submission error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit feedback: {str(e)}"
        )

@router.get("/feedback/stats/")
async def get_feedback_stats():
    """
    Get feedback statistics
    """
    try:
        if not os.path.exists(FEEDBACK_FILE):
            return {
                "total_feedbacks": 0,
                "average_rating": 0,
                "ratings_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
        
        total = len(feedbacks)
        ratings = [f['rating'] for f in feedbacks]
        avg_rating = sum(ratings) / total if total > 0 else 0
        
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            distribution[rating] += 1
        
        return {
            "total_feedbacks": total,
            "average_rating": round(avg_rating, 2),
            "ratings_distribution": distribution
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get feedback stats: {str(e)}"
        )
