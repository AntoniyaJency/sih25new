from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
from typing import List, Dict, Any
import json
import logging

from app.api import trains, sections, optimization, simulation, monitoring
from app.core.config import settings
from app.core.database import engine, Base
from app.core.websocket_manager import WebSocketManager
from app.models import schemas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket manager instance
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Railway Traffic Control System...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize optimization engine
    from app.core.optimization_engine import OptimizationEngine
    app.state.optimization_engine = OptimizationEngine()
    
    # Start background tasks
    asyncio.create_task(websocket_manager.broadcast_system_status())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Railway Traffic Control System...")

app = FastAPI(
    title="Railway Traffic Control System",
    description="AI-powered train traffic control system for maximizing section throughput",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(trains.router, prefix="/api/trains", tags=["trains"])
app.include_router(sections.router, prefix="/api/sections", tags=["sections"])
app.include_router(optimization.router, prefix="/api/optimization", tags=["optimization"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])

@app.get("/")
async def root():
    return {
        "message": "Railway Traffic Control System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "optimization_engine": "active",
        "websocket_connections": len(websocket_manager.active_connections)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket_manager.send_personal_message({
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                }, websocket)
            elif message.get("type") == "subscribe":
                # Subscribe to specific updates
                await websocket_manager.subscribe(websocket, message.get("topics", []))
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

# Mount static files for frontend (commented out for now)
# app.mount("/static", StaticFiles(directory="frontend/out"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
