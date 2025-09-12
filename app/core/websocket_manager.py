import json
import asyncio
from typing import List, Dict, Any, Set
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[WebSocket, Set[str]] = {}
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = set()
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
            
    async def broadcast(self, message: Dict[str, Any]):
        if not self.active_connections:
            return
            
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
                
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
            
    async def broadcast_to_subscribers(self, message: Dict[str, Any], topic: str):
        """Broadcast message only to subscribers of a specific topic"""
        if not self.active_connections:
            return
            
        disconnected = []
        for connection in self.active_connections:
            if connection in self.subscriptions and topic in self.subscriptions[connection]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error broadcasting to subscribers: {e}")
                    disconnected.append(connection)
                    
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
            
    async def subscribe(self, websocket: WebSocket, topics: List[str]):
        """Subscribe websocket to specific topics"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].update(topics)
            
    async def unsubscribe(self, websocket: WebSocket, topics: List[str]):
        """Unsubscribe websocket from specific topics"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].difference_update(topics)
            
    async def broadcast_system_status(self):
        """Background task to broadcast system status"""
        while True:
            try:
                status_message = {
                    "type": "system_status",
                    "timestamp": asyncio.get_event_loop().time(),
                    "active_connections": len(self.active_connections),
                    "status": "operational"
                }
                await self.broadcast(status_message)
                await asyncio.sleep(30)  # Broadcast every 30 seconds
            except Exception as e:
                logger.error(f"Error in broadcast_system_status: {e}")
                await asyncio.sleep(30)
