import sqlite3
import os
from datetime import datetime
from typing import Optional

DB_PATH = "database/predictions.db"

def init_database():
    """Initialize SQLite database"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL,
            verified BOOLEAN DEFAULT 0,
            feedback TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS retraining_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_version TEXT NOT NULL,
            accuracy REAL,
            timestamp TEXT NOT NULL,
            notes TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def save_prediction(image_url: str, disease_name: str, confidence: float, timestamp: str):
    """Save prediction to database"""
    init_database()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO predictions (image_url, disease_name, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (image_url, disease_name, confidence, timestamp))
    
    conn.commit()
    conn.close()

def get_predictions(limit: int = 100):
    """Retrieve predictions from database"""
    init_database()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?", (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results
