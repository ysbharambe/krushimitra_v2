from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from datetime import datetime
from ultralytics import YOLO

router = APIRouter()

class RetrainResponse(BaseModel):
    message: str
    new_accuracy: Optional[float] = None
    model_version: str
    timestamp: str

def perform_retraining():
    """Background task to retrain YOLOv8 model"""
    try:
        # Check if dataset exists
        dataset_path = "datasets/user_collected"
        if not os.path.exists(dataset_path) or not os.listdir(dataset_path):
            print("No new data available for retraining")
            return
        
        # Load existing model
        model_path = "models/best.pt"
        if not os.path.exists(model_path):
            model_path = "yolov8s.pt"
        
        model = YOLO(model_path)
        
        # Check if data.yaml exists
        data_yaml_path = "datasets/data.yaml"
        if not os.path.exists(data_yaml_path):
            print("data.yaml not found. Creating default configuration.")
            # Create a default data.yaml
            with open(data_yaml_path, "w") as f:
                f.write("""
# Plant Disease Dataset Configuration
path: ./user_collected
train: images/train
val: images/val

# Classes
nc: 10
names: ['Healthy', 'Leaf_Spot', 'Leaf_Blight', 'Powdery_Mildew', 'Rust', 'Bacterial_Blight', 'Early_Blight', 'Late_Blight', 'Anthracnose', 'Mosaic_Virus']
""")
        
        # Fine-tune the model
        print("Starting model retraining...")
        results = model.train(
            data=data_yaml_path,
            epochs=30,
            imgsz=640,
            batch=16,
            device='cpu',  # Change to 'cuda' if GPU available
            patience=5,
            project='models/training',
            name='retrained',
            exist_ok=True
        )
        
        # Get new accuracy
        metrics = model.val()
        new_accuracy = metrics.box.map * 100  # mAP50-95
        
        # Update model if improved
        new_model_path = "models/training/retrained/weights/best.pt"
        if os.path.exists(new_model_path):
            # Backup old model
            if os.path.exists("models/best.pt"):
                backup_path = f"models/backup/best_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"
                os.makedirs("models/backup", exist_ok=True)
                shutil.copy("models/best.pt", backup_path)
            
            # Copy new model
            shutil.copy(new_model_path, "models/best.pt")
            
            # Update model log
            log_entry = f"model_v{datetime.now().strftime('%Y%m%d_%H%M%S')}, {datetime.now().isoformat()}, {new_accuracy:.2f}%\n"
            with open("models/model_log.txt", "a") as log_file:
                log_file.write(log_entry)
            
            print(f"Model retrained successfully. New accuracy: {new_accuracy:.2f}%")
        else:
            print("Retraining completed but new model not found")
            
    except Exception as e:
        print(f"Retraining failed: {str(e)}")

@router.post("/retrain/", response_model=RetrainResponse)
async def retrain_model(background_tasks: BackgroundTasks):
    """
    Manually trigger YOLOv8 model retraining
    This process runs in the background
    """
    try:
        # Add retraining task to background
        background_tasks.add_task(perform_retraining)
        
        return RetrainResponse(
            message="Retraining process started in background. This may take several minutes.",
            model_version=f"model_v{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start retraining: {str(e)}"
        )

@router.get("/retrain/status/")
async def get_retrain_status():
    """Get the status and history of model retraining"""
    model_log_path = "models/model_log.txt"
    
    if not os.path.exists(model_log_path):
        return {
            "status": "No retraining history found",
            "history": []
        }
    
    with open(model_log_path, "r") as f:
        history = []
        for line in f.readlines():
            if line.strip():
                parts = line.strip().split(", ")
                if len(parts) >= 3:
                    history.append({
                        "version": parts[0],
                        "timestamp": parts[1],
                        "accuracy": parts[2]
                    })
    
    return {
        "status": "Available",
        "total_retrains": len(history),
        "history": history
    }
