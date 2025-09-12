from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.models.schemas import Train, TrainCreate, TrainUpdate, TrainStatus
from app.core.optimization_engine import OptimizationEngine, Train as OptTrain
from app.core.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for demo purposes
trains_db = {}
optimization_engine = OptimizationEngine()
websocket_manager = WebSocketManager()

@router.post("/", response_model=Train)
async def create_train(train: TrainCreate, background_tasks: BackgroundTasks):
    """Create a new train"""
    try:
        train_id = f"train_{len(trains_db) + 1}"
        train_data = Train(
            id=train_id,
            **train.dict()
        )
        trains_db[train_id] = train_data
        
        # Add to optimization engine
        opt_train = OptTrain(
            id=train_id,
            train_number=train.train_number,
            train_type=train.train_type.value,
            priority=train.priority,
            origin=train.origin,
            destination=train.destination,
            scheduled_departure=train.scheduled_departure,
            scheduled_arrival=train.scheduled_arrival,
            current_location=train.current_location,
            speed=train.speed,
            length=train.length,
            weight=train.weight,
            status=train.status.value
        )
        optimization_engine.add_train(opt_train)
        
        # Trigger optimization in background
        background_tasks.add_task(optimize_and_broadcast)
        
        logger.info(f"Created train {train.train_number} with ID {train_id}")
        return train_data
        
    except Exception as e:
        logger.error(f"Error creating train: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Train])
async def get_trains(status: Optional[TrainStatus] = None):
    """Get all trains, optionally filtered by status"""
    try:
        trains = list(trains_db.values())
        if status:
            trains = [train for train in trains if train.status == status]
        return trains
    except Exception as e:
        logger.error(f"Error getting trains: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{train_id}", response_model=Train)
async def get_train(train_id: str):
    """Get a specific train by ID"""
    if train_id not in trains_db:
        raise HTTPException(status_code=404, detail="Train not found")
    return trains_db[train_id]

@router.put("/{train_id}", response_model=Train)
async def update_train(train_id: str, train_update: TrainUpdate, background_tasks: BackgroundTasks):
    """Update a train"""
    if train_id not in trains_db:
        raise HTTPException(status_code=404, detail="Train not found")
    
    try:
        # Update train data
        existing_train = trains_db[train_id]
        update_data = train_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_train, field, value)
        
        # Update optimization engine
        opt_train = OptTrain(
            id=train_id,
            train_number=existing_train.train_number,
            train_type=existing_train.train_type.value,
            priority=existing_train.priority,
            origin=existing_train.origin,
            destination=existing_train.destination,
            scheduled_departure=existing_train.scheduled_departure,
            scheduled_arrival=existing_train.scheduled_arrival,
            current_location=existing_train.current_location,
            speed=existing_train.speed,
            length=existing_train.length,
            weight=existing_train.weight,
            status=existing_train.status.value
        )
        optimization_engine.add_train(opt_train)
        
        # Trigger optimization in background
        background_tasks.add_task(optimize_and_broadcast)
        
        logger.info(f"Updated train {train_id}")
        return existing_train
        
    except Exception as e:
        logger.error(f"Error updating train: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{train_id}")
async def delete_train(train_id: str, background_tasks: BackgroundTasks):
    """Delete a train"""
    if train_id not in trains_db:
        raise HTTPException(status_code=404, detail="Train not found")
    
    try:
        del trains_db[train_id]
        
        # Remove from optimization engine
        if train_id in optimization_engine.trains:
            del optimization_engine.trains[train_id]
        
        # Trigger optimization in background
        background_tasks.add_task(optimize_and_broadcast)
        
        logger.info(f"Deleted train {train_id}")
        return {"message": "Train deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting train: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{train_id}/delay")
async def delay_train(train_id: str, delay_minutes: int, background_tasks: BackgroundTasks):
    """Apply delay to a train"""
    if train_id not in trains_db:
        raise HTTPException(status_code=404, detail="Train not found")
    
    try:
        train = trains_db[train_id]
        train.status = TrainStatus.DELAYED
        
        # Update scheduled times
        from datetime import timedelta
        train.scheduled_departure += timedelta(minutes=delay_minutes)
        train.scheduled_arrival += timedelta(minutes=delay_minutes)
        
        # Update optimization engine
        opt_train = OptTrain(
            id=train_id,
            train_number=train.train_number,
            train_type=train.train_type.value,
            priority=train.priority,
            origin=train.origin,
            destination=train.destination,
            scheduled_departure=train.scheduled_departure,
            scheduled_arrival=train.scheduled_arrival,
            current_location=train.current_location,
            speed=train.speed,
            length=train.length,
            weight=train.weight,
            status=train.status.value
        )
        optimization_engine.add_train(opt_train)
        
        # Trigger optimization in background
        background_tasks.add_task(optimize_and_broadcast)
        
        logger.info(f"Applied {delay_minutes} minute delay to train {train_id}")
        return {"message": f"Applied {delay_minutes} minute delay to train {train_id}"}
        
    except Exception as e:
        logger.error(f"Error delaying train: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{train_id}/conflicts")
async def get_train_conflicts(train_id: str):
    """Get conflicts involving a specific train"""
    if train_id not in trains_db:
        raise HTTPException(status_code=404, detail="Train not found")
    
    try:
        conflicts = optimization_engine.detect_conflicts()
        train_conflicts = [
            conflict for conflict in conflicts 
            if conflict.train1_id == train_id or conflict.train2_id == train_id
        ]
        return train_conflicts
        
    except Exception as e:
        logger.error(f"Error getting train conflicts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def optimize_and_broadcast():
    """Background task to optimize and broadcast results"""
    try:
        result = optimization_engine.optimize_schedule()
        metrics = optimization_engine.get_throughput_metrics()
        
        # Broadcast optimization results
        await websocket_manager.broadcast({
            "type": "optimization_update",
            "result": result,
            "metrics": metrics,
            "timestamp": optimization_engine.solution
        })
        
    except Exception as e:
        logger.error(f"Error in optimize_and_broadcast: {e}")
