# Models Directory

## Place Your YOLOv8 Model Here

### Option 1: Use Pretrained Model (Automatic)
The application will automatically download `yolov8s.pt` on first run if no custom model is found.

### Option 2: Custom Trained Model
Place your custom-trained YOLOv8 model as `best.pt` in this directory.

```
models/
├── best.pt              # Your custom trained model
├── retrain_yolo.py      # Retraining script
└── README.md            # This file
```

### Training Your Own Model

1. **Prepare Dataset**
   - Collect images of diseased plants
   - Annotate with bounding boxes using tools like LabelImg or Roboflow
   - Organize in YOLO format (see datasets/README.md)

2. **Train Model**
   ```bash
   python retrain_yolo.py
   ```

3. **Or use YOLOv8 CLI**
   ```bash
   yolo train model=yolov8s.pt data=../datasets/data.yaml epochs=50 imgsz=640
   ```

### Model Performance Tips

- Use at least 100 images per class for better accuracy
- Include images with various lighting conditions
- Include different disease stages
- Use data augmentation
- Train for at least 30-50 epochs
- Use GPU for faster training (if available)

### Supported YOLOv8 Models

- `yolov8n.pt` - Nano (fastest, least accurate)
- `yolov8s.pt` - Small (balanced)
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (slowest, most accurate)

For farming applications, `yolov8s.pt` or `yolov8m.pt` are recommended for good balance of speed and accuracy.

### Model Versioning

The app automatically maintains:
- `best.pt` - Current production model
- `backup/` - Previous model versions
- `model_log.txt` - Version history with accuracy metrics
