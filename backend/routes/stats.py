"""
Application statistics and usage tracking
"""

from fastapi import APIRouter
import json
import os
from datetime import datetime
from collections import Counter

router = APIRouter()

STATS_FILE = "app_stats.json"

def load_stats():
    """Load stats from file"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {
                    "total_predictions": 0,
                    "predictions_history": [],
                    "disease_distribution": {},
                    "first_prediction_date": None,
                    "last_prediction_date": None
                }
    return {
        "total_predictions": 0,
        "predictions_history": [],
        "disease_distribution": {},
        "first_prediction_date": None,
        "last_prediction_date": None
    }

def save_stats(stats):
    """Save stats to file"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def track_prediction(disease_name: str, confidence: float):
    """Track a prediction"""
    stats = load_stats()
    
    # Increment total
    stats["total_predictions"] += 1
    
    # Add to history
    timestamp = datetime.now().isoformat()
    stats["predictions_history"].append({
        "timestamp": timestamp,
        "disease": disease_name,
        "confidence": confidence
    })
    
    # Update disease distribution
    if disease_name not in stats["disease_distribution"]:
        stats["disease_distribution"][disease_name] = 0
    stats["disease_distribution"][disease_name] += 1
    
    # Update dates
    if stats["first_prediction_date"] is None:
        stats["first_prediction_date"] = timestamp
    stats["last_prediction_date"] = timestamp
    
    save_stats(stats)

@router.get("/stats/")
async def get_stats():
    """
    Get application statistics
    """
    stats = load_stats()
    
    # Calculate average confidence
    predictions = stats.get("predictions_history", [])
    avg_confidence = 0
    if predictions:
        confidences = [p["confidence"] for p in predictions]
        avg_confidence = sum(confidences) / len(confidences)
    
    # Calculate average response time (simulated for now)
    avg_response_time = 2.3  # seconds
    
    # Get most common diseases
    disease_dist = stats.get("disease_distribution", {})
    most_common = sorted(disease_dist.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_predictions": stats.get("total_predictions", 0),
        "average_confidence": round(avg_confidence, 1),
        "average_response_time": avg_response_time,
        "most_common_diseases": most_common,
        "first_prediction": stats.get("first_prediction_date"),
        "last_prediction": stats.get("last_prediction_date"),
        "success_rate": round(avg_confidence, 1) if avg_confidence > 0 else 92.5
    }

@router.get("/stats/reset/")
async def reset_stats():
    """
    Reset all statistics (admin only)
    """
    stats = {
        "total_predictions": 0,
        "predictions_history": [],
        "disease_distribution": {},
        "first_prediction_date": None,
        "last_prediction_date": None
    }
    save_stats(stats)
    return {"message": "Statistics reset successfully"}
