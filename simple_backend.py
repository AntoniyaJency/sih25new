#!/usr/bin/env python3
"""
Simple Railway Traffic Control Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Railway Traffic Control System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Railway Traffic Control System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "System is running"
    }

@app.get("/api/trains")
async def get_trains():
    """Get sample trains"""
    return [
        {
            "id": "train_1",
            "train_number": "12345",
            "train_type": "express",
            "priority": 8,
            "origin": "Mumbai Central",
            "destination": "Delhi",
            "status": "running",
            "current_location": "Mumbai Central"
        },
        {
            "id": "train_2", 
            "train_number": "67890",
            "train_type": "local",
            "priority": 5,
            "origin": "Mumbai Central",
            "destination": "Thane",
            "status": "delayed",
            "current_location": "Kurla"
        }
    ]

@app.get("/api/metrics")
async def get_metrics():
    """Get performance metrics"""
    return {
        "total_trains": 45,
        "running_trains": 38,
        "delayed_trains": 5,
        "cancelled_trains": 2,
        "average_delay_minutes": 8.5,
        "punctuality_percentage": 84.4,
        "conflicts_detected": 3,
        "throughput_efficiency": 87.2
    }

if __name__ == "__main__":
    print("🚂 Starting Railway Traffic Control System Backend...")
    print("📡 Backend will be available at: http://localhost:8000")
    print("📊 API documentation will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
