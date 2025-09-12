from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import time
import logging

from app.models.schemas import OptimizationRequest, OptimizationResult, PerformanceMetrics
from app.core.optimization_engine import OptimizationEngine
from app.core.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
router = APIRouter()

optimization_engine = OptimizationEngine()
websocket_manager = WebSocketManager()

@router.post("/optimize", response_model=OptimizationResult)
async def optimize_schedule(request: OptimizationRequest, background_tasks: BackgroundTasks):
    """Run optimization for train schedule"""
    try:
        start_time = time.time()
        
        # Detect conflicts first
        conflicts = optimization_engine.detect_conflicts()
        logger.info(f"Detected {len(conflicts)} conflicts")
        
        # Run optimization
        result = optimization_engine.optimize_schedule()
        
        execution_time = time.time() - start_time
        
        optimization_result = OptimizationResult(
            status=result.get("status", "unknown"),
            solution=result.get("solution"),
            total_delay=result.get("total_delay"),
            conflicts_resolved=result.get("conflicts_resolved", len(conflicts)),
            execution_time=execution_time,
            message=result.get("message")
        )
        
        # Broadcast results
        background_tasks.add_task(broadcast_optimization_results, optimization_result)
        
        logger.info(f"Optimization completed in {execution_time:.2f} seconds")
        return optimization_result
        
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reoptimize")
async def reoptimize_on_disruption(
    disruption_type: str, 
    affected_trains: List[str], 
    background_tasks: BackgroundTasks
):
    """Re-optimize schedule when disruptions occur"""
    try:
        start_time = time.time()
        
        result = optimization_engine.reoptimize_on_disruption(disruption_type, affected_trains)
        
        execution_time = time.time() - start_time
        
        optimization_result = OptimizationResult(
            status=result.get("status", "unknown"),
            solution=result.get("solution"),
            total_delay=result.get("total_delay"),
            conflicts_resolved=result.get("conflicts_resolved"),
            execution_time=execution_time,
            message=f"Re-optimized due to {disruption_type}"
        )
        
        # Broadcast results
        background_tasks.add_task(broadcast_optimization_results, optimization_result)
        
        logger.info(f"Re-optimization completed in {execution_time:.2f} seconds")
        return optimization_result
        
    except Exception as e:
        logger.error(f"Re-optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conflicts")
async def get_conflicts():
    """Get all detected conflicts"""
    try:
        conflicts = optimization_engine.detect_conflicts()
        return {
            "conflicts": [
                {
                    "train1_id": conflict.train1_id,
                    "train2_id": conflict.train2_id,
                    "section_id": conflict.section_id,
                    "conflict_type": conflict.conflict_type,
                    "severity": conflict.severity,
                    "resolution_options": conflict.resolution_options
                }
                for conflict in conflicts
            ],
            "total_conflicts": len(conflicts)
        }
        
    except Exception as e:
        logger.error(f"Error getting conflicts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=PerformanceMetrics)
async def get_performance_metrics():
    """Get current performance metrics"""
    try:
        metrics = optimization_engine.get_throughput_metrics()
        return PerformanceMetrics(**metrics)
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_optimization_status():
    """Get optimization engine status"""
    try:
        return {
            "engine_active": True,
            "total_trains": len(optimization_engine.trains),
            "total_sections": len(optimization_engine.sections),
            "active_conflicts": len(optimization_engine.conflicts),
            "last_optimization": optimization_engine.solution,
            "status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Error getting optimization status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resolve-conflict/{conflict_id}")
async def resolve_conflict(conflict_id: str, resolution: Dict[str, Any], background_tasks: BackgroundTasks):
    """Apply a specific conflict resolution"""
    try:
        # Find the conflict
        conflicts = optimization_engine.detect_conflicts()
        conflict = None
        for c in conflicts:
            if c.train1_id == conflict_id.split('_')[0] and c.train2_id == conflict_id.split('_')[1]:
                conflict = c
                break
                
        if not conflict:
            raise HTTPException(status_code=404, detail="Conflict not found")
        
        # Apply resolution
        action = resolution.get("action")
        train_id = resolution.get("train_id")
        
        if action == "delay_train":
            delay_minutes = resolution.get("delay_minutes", 10)
            # Apply delay logic here
            logger.info(f"Applying {delay_minutes} minute delay to train {train_id}")
            
        elif action == "reroute_train":
            # Apply rerouting logic here
            logger.info(f"Rerouting train {train_id}")
            
        elif action == "change_platform":
            # Apply platform change logic here
            logger.info(f"Changing platform for train {train_id}")
        
        # Re-optimize after resolution
        background_tasks.add_task(run_optimization_after_resolution)
        
        return {"message": f"Applied resolution: {action} for train {train_id}"}
        
    except Exception as e:
        logger.error(f"Error resolving conflict: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def broadcast_optimization_results(result: OptimizationResult):
    """Broadcast optimization results via WebSocket"""
    try:
        await websocket_manager.broadcast({
            "type": "optimization_complete",
            "result": result.dict(),
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Error broadcasting optimization results: {e}")

async def run_optimization_after_resolution():
    """Run optimization after conflict resolution"""
    try:
        result = optimization_engine.optimize_schedule()
        await websocket_manager.broadcast({
            "type": "post_resolution_optimization",
            "result": result,
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Error in post-resolution optimization: {e}")
