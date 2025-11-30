from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import predict, retrain, translate, feedback, auth, stats
import uvicorn

app = FastAPI(
    title="KrushiMitra API",
    description="AI-Powered Plant Disease Detection for Farmers",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(retrain.router, prefix="/api", tags=["Retraining"])
app.include_router(translate.router, prefix="/api", tags=["Translation"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(stats.router, prefix="/api", tags=["Statistics"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to KrushiMitra API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/predict/",
            "retrain": "/api/retrain/",
            "translate": "/api/translate/",
            "languages": "/api/languages/"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "KrushiMitra API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
