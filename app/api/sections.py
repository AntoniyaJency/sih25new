from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
import logging

from app.models.schemas import TrackSection, TrackSectionCreate, TrackSectionUpdate
from app.core.optimization_engine import OptimizationEngine, TrackSection as OptTrackSection
from app.core.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for demo purposes
sections_db = {}
optimization_engine = OptimizationEngine()
websocket_manager = WebSocketManager()

@router.post("/", response_model=TrackSection)
async def create_section(section: TrackSectionCreate, background_tasks: BackgroundTasks):
    """Create a new track section"""
    try:
        section_id = f"section_{len(sections_db) + 1}"
        section_data = TrackSection(
            id=section_id,
            **section.dict()
        )
        sections_db[section_id] = section_data
        
        # Add to optimization engine
        opt_section = OptTrackSection(
            id=section_id,
            name=section.name,
            start_station=section.start_station,
            end_station=section.end_station,
            length=section.length,
            max_speed=section.max_speed,
            capacity=section.capacity,
            gradient=section.gradient,
            signal_spacing=section.signal_spacing,
            maintenance_windows=[]
        )
        optimization_engine.add_section(opt_section)
        
        logger.info(f"Created section {section.name} with ID {section_id}")
        return section_data
        
    except Exception as e:
        logger.error(f"Error creating section: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TrackSection])
async def get_sections():
    """Get all track sections"""
    try:
        return list(sections_db.values())
    except Exception as e:
        logger.error(f"Error getting sections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{section_id}", response_model=TrackSection)
async def get_section(section_id: str):
    """Get a specific section by ID"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    return sections_db[section_id]

@router.put("/{section_id}", response_model=TrackSection)
async def update_section(section_id: str, section_update: TrackSectionUpdate):
    """Update a section"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        # Update section data
        existing_section = sections_db[section_id]
        update_data = section_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_section, field, value)
        
        # Update optimization engine
        opt_section = OptTrackSection(
            id=section_id,
            name=existing_section.name,
            start_station=existing_section.start_station,
            end_station=existing_section.end_station,
            length=existing_section.length,
            max_speed=existing_section.max_speed,
            capacity=existing_section.capacity,
            gradient=existing_section.gradient,
            signal_spacing=existing_section.signal_spacing,
            maintenance_windows=[]
        )
        optimization_engine.add_section(opt_section)
        
        logger.info(f"Updated section {section_id}")
        return existing_section
        
    except Exception as e:
        logger.error(f"Error updating section: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{section_id}")
async def delete_section(section_id: str):
    """Delete a section"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        del sections_db[section_id]
        
        # Remove from optimization engine
        if section_id in optimization_engine.sections:
            del optimization_engine.sections[section_id]
        
        logger.info(f"Deleted section {section_id}")
        return {"message": "Section deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting section: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{section_id}/capacity")
async def get_section_capacity(section_id: str):
    """Get current capacity utilization for a section"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        section = sections_db[section_id]
        
        # Count trains currently in this section
        trains_in_section = 0
        for train in optimization_engine.trains.values():
            if train.current_location == section.start_station or train.current_location == section.end_station:
                trains_in_section += 1
        
        utilization_percentage = (trains_in_section / section.capacity) * 100
        
        return {
            "section_id": section_id,
            "section_name": section.name,
            "max_capacity": section.capacity,
            "current_trains": trains_in_section,
            "utilization_percentage": utilization_percentage,
            "available_capacity": section.capacity - trains_in_section
        }
        
    except Exception as e:
        logger.error(f"Error getting section capacity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{section_id}/conflicts")
async def get_section_conflicts(section_id: str):
    """Get conflicts in a specific section"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        conflicts = optimization_engine.detect_conflicts()
        section_conflicts = [
            conflict for conflict in conflicts 
            if conflict.section_id == section_id
        ]
        
        return {
            "section_id": section_id,
            "conflicts": [
                {
                    "train1_id": conflict.train1_id,
                    "train2_id": conflict.train2_id,
                    "conflict_type": conflict.conflict_type,
                    "severity": conflict.severity,
                    "resolution_options": conflict.resolution_options
                }
                for conflict in section_conflicts
            ],
            "total_conflicts": len(section_conflicts)
        }
        
    except Exception as e:
        logger.error(f"Error getting section conflicts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{section_id}/maintenance")
async def schedule_maintenance(section_id: str, start_time: str, end_time: str):
    """Schedule maintenance window for a section"""
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        from datetime import datetime
        
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        
        # Add maintenance window to optimization engine
        if section_id in optimization_engine.sections:
            optimization_engine.sections[section_id].maintenance_windows.append((start_dt, end_dt))
        
        logger.info(f"Scheduled maintenance for section {section_id} from {start_time} to {end_time}")
        return {
            "message": f"Maintenance scheduled for section {section_id}",
            "start_time": start_time,
            "end_time": end_time
        }
        
    except Exception as e:
        logger.error(f"Error scheduling maintenance: {e}")
        raise HTTPException(status_code=500, detail=str(e))
