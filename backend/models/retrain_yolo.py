from ultralytics import YOLO
import os
import shutil
from datetime import datetime

def retrain_model(data_yaml_path: str, epochs: int = 30):
    """
    Retrain YOLOv8 model with new data
    """
    # Load existing model
    model_path = "best.pt" if os.path.exists("best.pt") else "yolov8s.pt"
    model = YOLO(model_path)
    
    # Train
    results = model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=640,
        batch=16,
        device='cpu',
        project='training',
        name='retrained',
        exist_ok=True
    )
    
    # Validate
    metrics = model.val()
    accuracy = metrics.box.map * 100
    
    # Save new model
    new_model_path = "training/retrained/weights/best.pt"
    if os.path.exists(new_model_path):
        backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs("backup", exist_ok=True)
        
        if os.path.exists("best.pt"):
            shutil.copy("best.pt", f"backup/best_backup_{backup_time}.pt")
        
        shutil.copy(new_model_path, "best.pt")
        
        # Log
        with open("model_log.txt", "a") as f:
            f.write(f"model_v{backup_time}, {datetime.now().isoformat()}, {accuracy:.2f}%\n")
    
    return accuracy

if __name__ == "__main__":
    # Example usage
    accuracy = retrain_model("../datasets/data.yaml")
    print(f"Retraining completed. New accuracy: {accuracy:.2f}%")
