# KrushiMitra Backend

FastAPI backend with YOLOv8 integration for plant disease detection.

## Features

- YOLOv8 disease detection
- Cloudinary image storage
- Google Translate API integration
- SQLite database for predictions
- Automatic model retraining
- RESTful API endpoints

## Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Run server**
```bash
python main.py
```

Server runs at `http://localhost:8000`

## API Endpoints

### Prediction
```bash
POST /api/predict/
Content-Type: application/json

{
  "image_url": "https://res.cloudinary.com/your-cloud/image.jpg"
}
```

### Translation
```bash
POST /api/translate/
Content-Type: application/json

{
  "text": "Disease detected",
  "target_language": "hi",
  "source_language": "en"
}
```

### Retraining
```bash
POST /api/retrain/
```

### Model Info
```bash
GET /api/model-info/
```

## Model Training

Place your YOLOv8 model at `models/best.pt` or use the default pretrained model.

To train custom model:
```bash
cd models
python retrain_yolo.py
```

## Database

SQLite database stores:
- Prediction history
- Retraining logs
- Model versions

Location: `database/predictions.db`

## Pesticide Recommendations

Edit `utils/pesticide_data.json` to add/modify treatment recommendations.

## Testing

Run API tests:
```bash
pytest tests/
```

## Production

Use Gunicorn or Uvicorn workers:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
