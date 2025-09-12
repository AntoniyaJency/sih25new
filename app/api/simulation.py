from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import time
import logging
import copy

from app.models.schemas import SimulationRequest, SimulationResult
from app.core.optimization_engine import OptimizationEngine
from app.core.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
router = APIRouter()

optimization_engine = OptimizationEngine()
websocket_manager = WebSocketManager()

@router.post("/run", response_model=SimulationResult)
async def run_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """Run what-if simulation scenario"""
    try:
        start_time = time.time()
        
        # Store original state
        original_trains = copy.deepcopy(optimization_engine.trains)
        original_sections = copy.deepcopy(optimization_engine.sections)
        
        # Apply modifications
        modified_trains = apply_modifications(original_trains, request.modifications)
        
        # Create temporary optimization engine for simulation
        sim_engine = OptimizationEngine()
        sim_engine.trains = modified_trains
        sim_engine.sections = original_sections
        
        # Run optimization on modified scenario
        sim_result = sim_engine.optimize_schedule()
        sim_metrics = sim_engine.get_throughput_metrics()
        
        # Run optimization on base scenario
        base_result = optimization_engine.optimize_schedule()
        base_metrics = optimization_engine.get_throughput_metrics()
        
        # Calculate improvement
        base_delay = base_result.get("total_delay", 0)
        sim_delay = sim_result.get("total_delay", 0)
        
        if base_delay > 0:
            improvement_percentage = ((base_delay - sim_delay) / base_delay) * 100
        else:
            improvement_percentage = 0
        
        execution_time = time.time() - start_time
        
        result = SimulationResult(
            scenario_name=request.scenario_name,
            base_metrics=base_metrics,
            modified_metrics=sim_metrics,
            improvement_percentage=improvement_percentage,
            execution_time=execution_time
        )
        
        # Broadcast simulation results
        background_tasks.add_task(broadcast_simulation_results, result)
        
        logger.info(f"Simulation '{request.scenario_name}' completed in {execution_time:.2f} seconds")
        return result
        
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenarios")
async def get_simulation_scenarios():
    """Get available simulation scenarios"""
    try:
        scenarios = [
            {
                "id": "delay_scenario",
                "name": "Train Delay Impact",
                "description": "Simulate impact of 30-minute delay on express train",
                "modifications": [
                    {
                        "type": "delay_train",
                        "train_filter": {"train_type": "express"},
                        "delay_minutes": 30
                    }
                ]
            },
            {
                "id": "cancellation_scenario",
                "name": "Train Cancellation",
                "description": "Simulate cancellation of local train",
                "modifications": [
                    {
                        "type": "cancel_train",
                        "train_filter": {"train_type": "local"},
                        "limit": 1
                    }
                ]
            },
            {
                "id": "maintenance_scenario",
                "name": "Track Maintenance",
                "description": "Simulate track maintenance reducing capacity",
                "modifications": [
                    {
                        "type": "reduce_capacity",
                        "section_filter": {"name": "Main Line"},
                        "capacity_reduction": 0.5
                    }
                ]
            },
            {
                "id": "priority_scenario",
                "name": "Priority Adjustment",
                "description": "Simulate increasing freight train priority",
                "modifications": [
                    {
                        "type": "change_priority",
                        "train_filter": {"train_type": "freight"},
                        "new_priority": 8
                    }
                ]
            }
        ]
        
        return {"scenarios": scenarios}
        
    except Exception as e:
        logger.error(f"Error getting simulation scenarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_scenarios(scenario1: Dict[str, Any], scenario2: Dict[str, Any]):
    """Compare two simulation scenarios"""
    try:
        start_time = time.time()
        
        # Run both scenarios
        sim1_result = await run_simulation_internal(scenario1)
        sim2_result = await run_simulation_internal(scenario2)
        
        execution_time = time.time() - start_time
        
        comparison = {
            "scenario1": {
                "name": scenario1.get("name", "Scenario 1"),
                "metrics": sim1_result["metrics"],
                "improvement": sim1_result["improvement"]
            },
            "scenario2": {
                "name": scenario2.get("name", "Scenario 2"),
                "metrics": sim2_result["metrics"],
                "improvement": sim2_result["improvement"]
            },
            "comparison": {
                "better_scenario": "scenario1" if sim1_result["improvement"] > sim2_result["improvement"] else "scenario2",
                "improvement_difference": abs(sim1_result["improvement"] - sim2_result["improvement"]),
                "execution_time": execution_time
            }
        }
        
        logger.info(f"Scenario comparison completed in {execution_time:.2f} seconds")
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_simulation_history():
    """Get simulation history"""
    try:
        # In a real implementation, this would come from a database
        history = [
            {
                "id": "sim_001",
                "scenario_name": "Express Delay Impact",
                "timestamp": "2024-01-15T10:30:00Z",
                "improvement_percentage": 15.5,
                "execution_time": 2.3,
                "status": "completed"
            },
            {
                "id": "sim_002",
                "scenario_name": "Track Maintenance",
                "timestamp": "2024-01-15T11:15:00Z",
                "improvement_percentage": -8.2,
                "execution_time": 1.8,
                "status": "completed"
            },
            {
                "id": "sim_003",
                "scenario_name": "Priority Adjustment",
                "timestamp": "2024-01-15T12:00:00Z",
                "improvement_percentage": 22.1,
                "execution_time": 2.7,
                "status": "completed"
            }
        ]
        
        return {"history": history}
        
    except Exception as e:
        logger.error(f"Error getting simulation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def apply_modifications(trains: Dict[str, Any], modifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Apply modifications to train data for simulation"""
    modified_trains = copy.deepcopy(trains)
    
    for modification in modifications:
        mod_type = modification.get("type")
        
        if mod_type == "delay_train":
            train_filter = modification.get("train_filter", {})
            delay_minutes = modification.get("delay_minutes", 0)
            
            for train_id, train in modified_trains.items():
                if matches_filter(train, train_filter):
                    from datetime import timedelta
                    train.scheduled_departure += timedelta(minutes=delay_minutes)
                    train.scheduled_arrival += timedelta(minutes=delay_minutes)
                    train.status = "delayed"
                    
        elif mod_type == "cancel_train":
            train_filter = modification.get("train_filter", {})
            limit = modification.get("limit", 1)
            
            cancelled_count = 0
            trains_to_remove = []
            
            for train_id, train in modified_trains.items():
                if cancelled_count < limit and matches_filter(train, train_filter):
                    trains_to_remove.append(train_id)
                    cancelled_count += 1
            
            for train_id in trains_to_remove:
                del modified_trains[train_id]
                
        elif mod_type == "change_priority":
            train_filter = modification.get("train_filter", {})
            new_priority = modification.get("new_priority", 5)
            
            for train_id, train in modified_trains.items():
                if matches_filter(train, train_filter):
                    train.priority = new_priority
    
    return modified_trains

def matches_filter(train: Any, filter_dict: Dict[str, Any]) -> bool:
    """Check if train matches the given filter"""
    for key, value in filter_dict.items():
        if hasattr(train, key) and getattr(train, key) != value:
            return False
    return True

async def run_simulation_internal(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """Internal function to run a single simulation"""
    try:
        # Store original state
        original_trains = copy.deepcopy(optimization_engine.trains)
        
        # Apply modifications
        modified_trains = apply_modifications(original_trains, scenario.get("modifications", []))
        
        # Create temporary optimization engine
        sim_engine = OptimizationEngine()
        sim_engine.trains = modified_trains
        sim_engine.sections = copy.deepcopy(optimization_engine.sections)
        
        # Run optimization
        sim_result = sim_engine.optimize_schedule()
        sim_metrics = sim_engine.get_throughput_metrics()
        
        # Calculate improvement
        base_result = optimization_engine.optimize_schedule()
        base_delay = base_result.get("total_delay", 0)
        sim_delay = sim_result.get("total_delay", 0)
        
        if base_delay > 0:
            improvement_percentage = ((base_delay - sim_delay) / base_delay) * 100
        else:
            improvement_percentage = 0
        
        return {
            "metrics": sim_metrics,
            "improvement": improvement_percentage
        }
        
    except Exception as e:
        logger.error(f"Error in internal simulation: {e}")
        return {"metrics": {}, "improvement": 0}

async def broadcast_simulation_results(result: SimulationResult):
    """Broadcast simulation results via WebSocket"""
    try:
        await websocket_manager.broadcast({
            "type": "simulation_complete",
            "result": result.dict(),
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Error broadcasting simulation results: {e}")
