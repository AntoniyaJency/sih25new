#!/usr/bin/env python3
"""
Simple backend test
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Railway Traffic Control System API is working!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting Railway Traffic Control System Backend...")
    print("📡 Backend will be available at: http://localhost:8000")
    print("📊 API documentation will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
