from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TrainType(str, Enum):
    EXPRESS = "express"
    LOCAL = "local"
    FREIGHT = "freight"
    SPECIAL = "special"
    MAINTENANCE = "maintenance"

class TrainStatus(str, Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    DELAYED = "delayed"
    CANCELLED = "cancelled"
    MAINTENANCE = "maintenance"
    ARRIVED = "arrived"

class ConflictType(str, Enum):
    HEADWAY = "headway"
    PLATFORM = "platform"
    CROSSING = "crossing"
    SIGNAL = "signal"
    MAINTENANCE = "maintenance"

class TrainBase(BaseModel):
    train_number: str = Field(..., description="Train number/identifier")
    train_type: TrainType = Field(..., description="Type of train")
    priority: int = Field(..., ge=1, le=10, description="Priority level (1-10)")
    origin: str = Field(..., description="Origin station")
    destination: str = Field(..., description="Destination station")
    scheduled_departure: datetime = Field(..., description="Scheduled departure time")
    scheduled_arrival: datetime = Field(..., description="Scheduled arrival time")
    current_location: str = Field(..., description="Current location/station")
    speed: float = Field(..., gt=0, description="Current speed in km/h")
    length: float = Field(..., gt=0, description="Train length in meters")
    weight: float = Field(..., gt=0, description="Train weight in tons")
    status: TrainStatus = Field(default=TrainStatus.SCHEDULED, description="Current status")

class TrainCreate(TrainBase):
    pass

class TrainUpdate(BaseModel):
    train_number: Optional[str] = None
    train_type: Optional[TrainType] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    origin: Optional[str] = None
    destination: Optional[str] = None
    scheduled_departure: Optional[datetime] = None
    scheduled_arrival: Optional[datetime] = None
    current_location: Optional[str] = None
    speed: Optional[float] = Field(None, gt=0)
    length: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    status: Optional[TrainStatus] = None

class Train(TrainBase):
    id: str = Field(..., description="Unique train identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class TrackSectionBase(BaseModel):
    name: str = Field(..., description="Section name")
    start_station: str = Field(..., description="Start station")
    end_station: str = Field(..., description="End station")
    length: float = Field(..., gt=0, description="Section length in km")
    max_speed: float = Field(..., gt=0, description="Maximum speed in km/h")
    capacity: int = Field(..., gt=0, description="Maximum number of trains")
    gradient: float = Field(..., description="Gradient percentage")
    signal_spacing: float = Field(..., gt=0, description="Signal spacing in km")

class TrackSectionCreate(TrackSectionBase):
    pass

class TrackSectionUpdate(BaseModel):
    name: Optional[str] = None
    start_station: Optional[str] = None
    end_station: Optional[str] = None
    length: Optional[float] = Field(None, gt=0)
    max_speed: Optional[float] = Field(None, gt=0)
    capacity: Optional[int] = Field(None, gt=0)
    gradient: Optional[float] = None
    signal_spacing: Optional[float] = Field(None, gt=0)

class TrackSection(TrackSectionBase):
    id: str = Field(..., description="Unique section identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class ConflictBase(BaseModel):
    train1_id: str = Field(..., description="First train ID")
    train2_id: str = Field(..., description="Second train ID")
    section_id: str = Field(..., description="Section where conflict occurs")
    conflict_type: ConflictType = Field(..., description="Type of conflict")
    severity: float = Field(..., ge=0, le=1, description="Conflict severity (0-1)")
    resolution_options: List[Dict[str, Any]] = Field(..., description="Available resolution options")

class ConflictCreate(ConflictBase):
    pass

class Conflict(ConflictBase):
    id: str = Field(..., description="Unique conflict identifier")
    detected_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolution_applied: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class OptimizationRequest(BaseModel):
    section_id: Optional[str] = None
    time_horizon_minutes: int = Field(default=60, gt=0, le=480)
    include_conflict_resolution: bool = Field(default=True)
    priority_weights: Optional[Dict[str, float]] = None

class OptimizationResult(BaseModel):
    status: str = Field(..., description="Optimization status")
    solution: Optional[Dict[str, Any]] = None
    total_delay: Optional[float] = None
    conflicts_resolved: Optional[int] = None
    execution_time: float = Field(..., description="Execution time in seconds")
    message: Optional[str] = None

class SimulationRequest(BaseModel):
    scenario_name: str = Field(..., description="Name of the scenario")
    base_schedule: Dict[str, Any] = Field(..., description="Base schedule to modify")
    modifications: List[Dict[str, Any]] = Field(..., description="Modifications to apply")
    simulation_duration_minutes: int = Field(default=120, gt=0, le=1440)

class SimulationResult(BaseModel):
    scenario_name: str
    base_metrics: Dict[str, Any]
    modified_metrics: Dict[str, Any]
    improvement_percentage: float
    execution_time: float

class PerformanceMetrics(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    total_trains: int
    running_trains: int
    delayed_trains: int
    cancelled_trains: int
    average_delay_minutes: float
    punctuality_percentage: float
    conflicts_detected: int
    throughput_efficiency: float

class SystemStatus(BaseModel):
    status: str = Field(..., description="System status")
    optimization_engine_active: bool
    websocket_connections: int
    last_optimization: Optional[datetime] = None
    active_conflicts: int
    system_load: float = Field(..., ge=0, le=1)

class Alert(BaseModel):
    id: str
    type: str = Field(..., description="Alert type")
    severity: str = Field(..., description="Alert severity")
    message: str = Field(..., description="Alert message")
    train_id: Optional[str] = None
    section_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    acknowledged: bool = Field(default=False)
