import numpy as np
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from typing import List, Dict, Any, Tuple, Optional
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class Train:
    id: str
    train_number: str
    train_type: str  # express, local, freight, special
    priority: int  # 1-10, higher is more important
    origin: str
    destination: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    current_location: str
    speed: float  # km/h
    length: float  # meters
    weight: float  # tons
    status: str  # running, delayed, cancelled, maintenance

@dataclass
class TrackSection:
    id: str
    name: str
    start_station: str
    end_station: str
    length: float  # km
    max_speed: float  # km/h
    capacity: int  # number of trains
    gradient: float  # percentage
    signal_spacing: float  # km
    maintenance_windows: List[Tuple[datetime, datetime]]

@dataclass
class Conflict:
    train1_id: str
    train2_id: str
    section_id: str
    conflict_type: str  # headway, platform, crossing
    severity: float  # 0-1
    resolution_options: List[Dict[str, Any]]

class OptimizationEngine:
    def __init__(self):
        self.trains: Dict[str, Train] = {}
        self.sections: Dict[str, TrackSection] = {}
        self.conflicts: List[Conflict] = []
        self.solver = None
        self.solution = None
        
    def add_train(self, train: Train):
        """Add or update train information"""
        self.trains[train.id] = train
        logger.info(f"Added train {train.train_number} to optimization engine")
        
    def add_section(self, section: TrackSection):
        """Add or update track section information"""
        self.sections[section.id] = section
        logger.info(f"Added section {section.name} to optimization engine")
        
    def detect_conflicts(self) -> List[Conflict]:
        """Detect conflicts between trains"""
        conflicts = []
        
        for train1_id, train1 in self.trains.items():
            for train2_id, train2 in self.trains.items():
                if train1_id >= train2_id:  # Avoid duplicate checks
                    continue
                    
                # Check for headway conflicts
                headway_conflict = self._check_headway_conflict(train1, train2)
                if headway_conflict:
                    conflicts.append(headway_conflict)
                    
                # Check for platform conflicts
                platform_conflict = self._check_platform_conflict(train1, train2)
                if platform_conflict:
                    conflicts.append(platform_conflict)
                    
        self.conflicts = conflicts
        return conflicts
        
    def _check_headway_conflict(self, train1: Train, train2: Train) -> Optional[Conflict]:
        """Check for headway conflicts between two trains"""
        # Simplified headway conflict detection
        # In reality, this would consider track sections, timing, and safety margins
        
        if train1.current_location == train2.current_location:
            # Calculate minimum headway based on train speeds and safety requirements
            min_headway = max(
                train1.length / train1.speed * 3.6,  # Convert to seconds
                train2.length / train2.speed * 3.6,
                120  # Minimum 2 minutes
            )
            
            time_diff = abs((train1.scheduled_departure - train2.scheduled_departure).total_seconds())
            
            if time_diff < min_headway:
                return Conflict(
                    train1_id=train1.id,
                    train2_id=train2.id,
                    section_id=train1.current_location,
                    conflict_type="headway",
                    severity=1.0 - (time_diff / min_headway),
                    resolution_options=[
                        {"action": "delay_train", "train_id": train1.id, "delay_minutes": min_headway/60},
                        {"action": "delay_train", "train_id": train2.id, "delay_minutes": min_headway/60},
                        {"action": "reroute_train", "train_id": train1.id},
                        {"action": "reroute_train", "train_id": train2.id}
                    ]
                )
        return None
        
    def _check_platform_conflict(self, train1: Train, train2: Train) -> Optional[Conflict]:
        """Check for platform conflicts between two trains"""
        # Simplified platform conflict detection
        if (train1.destination == train2.destination and 
            abs((train1.scheduled_arrival - train2.scheduled_arrival).total_seconds()) < 300):  # 5 minutes
            return Conflict(
                train1_id=train1.id,
                train2_id=train2.id,
                section_id=train1.destination,
                conflict_type="platform",
                severity=0.8,
                resolution_options=[
                    {"action": "delay_train", "train_id": train1.id, "delay_minutes": 10},
                    {"action": "delay_train", "train_id": train2.id, "delay_minutes": 10},
                    {"action": "change_platform", "train_id": train1.id},
                    {"action": "change_platform", "train_id": train2.id}
                ]
            )
        return None
        
    def optimize_schedule(self) -> Dict[str, Any]:
        """Main optimization function using constraint programming"""
        try:
            # Create CP model
            model = cp_model.CpModel()
            
            # Decision variables
            train_departures = {}
            train_arrivals = {}
            train_delays = {}
            
            for train_id, train in self.trains.items():
                # Convert datetime to minutes since epoch for optimization
                base_departure = int(train.scheduled_departure.timestamp() / 60)
                base_arrival = int(train.scheduled_arrival.timestamp() / 60)
                
                # Allow delays up to 60 minutes
                train_departures[train_id] = model.NewIntVar(
                    base_departure, base_departure + 60, f"departure_{train_id}"
                )
                train_arrivals[train_id] = model.NewIntVar(
                    base_arrival, base_arrival + 60, f"arrival_{train_id}"
                )
                train_delays[train_id] = model.NewIntVar(
                    0, 60, f"delay_{train_id}"
                )
                
                # Constraint: delay = departure - base_departure
                model.Add(train_delays[train_id] == train_departures[train_id] - base_departure)
                
            # Add conflict resolution constraints
            for conflict in self.conflicts:
                if conflict.conflict_type == "headway":
                    # Ensure minimum headway between trains
                    min_headway = 5  # minutes
                    model.Add(
                        train_departures[conflict.train1_id] + min_headway <= train_departures[conflict.train2_id]
                    ).OnlyEnforceIf(
                        model.NewBoolVar(f"train1_first_{conflict.train1_id}_{conflict.train2_id}")
                    )
                    model.Add(
                        train_departures[conflict.train2_id] + min_headway <= train_departures[conflict.train1_id]
                    ).OnlyEnforceIf(
                        model.NewBoolVar(f"train2_first_{conflict.train1_id}_{conflict.train2_id}")
                    )
                    
            # Objective: minimize total delay weighted by priority
            total_delay = []
            for train_id, train in self.trains.items():
                # Higher priority trains have lower delay weights
                weight = 1.0 / train.priority
                total_delay.append(train_delays[train_id] * weight)
                
            model.Minimize(sum(total_delay))
            
            # Solve the model
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = 30  # 30 second timeout
            
            status = solver.Solve(model)
            
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                # Extract solution
                solution = {}
                for train_id in self.trains.keys():
                    solution[train_id] = {
                        "departure_time": datetime.fromtimestamp(solver.Value(train_departures[train_id]) * 60),
                        "arrival_time": datetime.fromtimestamp(solver.Value(train_arrivals[train_id]) * 60),
                        "delay_minutes": solver.Value(train_delays[train_id])
                    }
                    
                return {
                    "status": "optimal" if status == cp_model.OPTIMAL else "feasible",
                    "solution": solution,
                    "total_delay": sum(solver.Value(delay) for delay in train_delays.values()),
                    "conflicts_resolved": len(self.conflicts)
                }
            else:
                return {
                    "status": "infeasible",
                    "message": "No feasible solution found",
                    "conflicts": len(self.conflicts)
                }
                
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
            
    def reoptimize_on_disruption(self, disruption_type: str, affected_trains: List[str]) -> Dict[str, Any]:
        """Re-optimize schedule when disruptions occur"""
        logger.info(f"Re-optimizing due to {disruption_type} affecting trains: {affected_trains}")
        
        # Update affected trains with new constraints
        for train_id in affected_trains:
            if train_id in self.trains:
                if disruption_type == "delay":
                    # Add delay to affected trains
                    self.trains[train_id].status = "delayed"
                elif disruption_type == "cancellation":
                    # Remove cancelled trains
                    del self.trains[train_id]
                elif disruption_type == "maintenance":
                    # Add maintenance constraints
                    self.trains[train_id].status = "maintenance"
                    
        # Re-detect conflicts and optimize
        self.detect_conflicts()
        return self.optimize_schedule()
        
    def get_throughput_metrics(self) -> Dict[str, Any]:
        """Calculate section throughput metrics"""
        total_trains = len(self.trains)
        running_trains = sum(1 for train in self.trains.values() if train.status == "running")
        delayed_trains = sum(1 for train in self.trains.values() if train.status == "delayed")
        
        # Calculate average delay
        total_delay = 0
        for train in self.trains.values():
            if train.status == "delayed":
                delay_minutes = (datetime.now() - train.scheduled_departure).total_seconds() / 60
                total_delay += max(0, delay_minutes)
                
        avg_delay = total_delay / max(1, delayed_trains) if delayed_trains > 0 else 0
        
        return {
            "total_trains": total_trains,
            "running_trains": running_trains,
            "delayed_trains": delayed_trains,
            "cancelled_trains": sum(1 for train in self.trains.values() if train.status == "cancelled"),
            "average_delay_minutes": avg_delay,
            "punctuality_percentage": (running_trains / max(1, total_trains)) * 100,
            "conflicts_detected": len(self.conflicts),
            "throughput_efficiency": (running_trains / max(1, total_trains)) * 100
        }
