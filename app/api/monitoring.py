from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import time
import logging
from datetime import datetime, timedelta

from app.models.schemas import PerformanceMetrics, SystemStatus, Alert
from app.core.optimization_engine import OptimizationEngine
from app.core.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)
router = APIRouter()

optimization_engine = OptimizationEngine()
websocket_manager = WebSocketManager()

# In-memory storage for alerts and historical data
alerts_db = []
performance_history = []

@router.get("/metrics", response_model=PerformanceMetrics)
async def get_current_metrics():
    """Get current performance metrics"""
    try:
        metrics = optimization_engine.get_throughput_metrics()
        performance_metrics = PerformanceMetrics(**metrics)
        
        # Store in history
        performance_history.append(performance_metrics)
        
        # Keep only last 1000 records
        if len(performance_history) > 1000:
            performance_history.pop(0)
        
        return performance_metrics
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/history")
async def get_metrics_history(hours: int = 24):
    """Get historical performance metrics"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_history = [
            metrics for metrics in performance_history
            if metrics.timestamp >= cutoff_time
        ]
        
        return {
            "metrics": [metrics.dict() for metrics in filtered_history],
            "time_range_hours": hours,
            "total_records": len(filtered_history)
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get overall system status"""
    try:
        metrics = optimization_engine.get_throughput_metrics()
        
        # Calculate system load (simplified)
        total_trains = metrics.get("total_trains", 0)
        max_capacity = sum(section.capacity for section in optimization_engine.sections.values())
        system_load = total_trains / max(1, max_capacity)
        
        status = SystemStatus(
            status="operational",
            optimization_engine_active=True,
            websocket_connections=len(websocket_manager.active_connections),
            last_optimization=optimization_engine.solution,
            active_conflicts=metrics.get("conflicts_detected", 0),
            system_load=min(1.0, system_load)
        )
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def get_alerts(acknowledged: bool = None):
    """Get system alerts"""
    try:
        filtered_alerts = alerts_db
        
        if acknowledged is not None:
            filtered_alerts = [alert for alert in alerts_db if alert.acknowledged == acknowledged]
        
        return {
            "alerts": [alert.dict() for alert in filtered_alerts],
            "total_alerts": len(filtered_alerts),
            "unacknowledged_alerts": len([a for a in alerts_db if not a.acknowledged])
        }
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Acknowledge an alert"""
    try:
        alert = next((a for a in alerts_db if a.id == alert_id), None)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        alert.acknowledged = True
        
        logger.info(f"Alert {alert_id} acknowledged")
        return {"message": f"Alert {alert_id} acknowledged"}
        
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        # Get current metrics
        current_metrics = optimization_engine.get_throughput_metrics()
        
        # Get recent alerts
        recent_alerts = [
            alert for alert in alerts_db
            if alert.timestamp >= datetime.now() - timedelta(hours=1)
        ]
        
        # Get system status
        system_status = await get_system_status()
        
        # Calculate trends
        if len(performance_history) >= 2:
            latest = performance_history[-1]
            previous = performance_history[-2]
            
            trends = {
                "punctuality_trend": latest.punctuality_percentage - previous.punctuality_percentage,
                "delay_trend": latest.average_delay_minutes - previous.average_delay_minutes,
                "throughput_trend": latest.throughput_efficiency - previous.throughput_efficiency
            }
        else:
            trends = {
                "punctuality_trend": 0,
                "delay_trend": 0,
                "throughput_trend": 0
            }
        
        dashboard_data = {
            "current_metrics": current_metrics,
            "system_status": system_status.dict(),
            "recent_alerts": [alert.dict() for alert in recent_alerts],
            "trends": trends,
            "last_updated": datetime.now().isoformat()
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kpis")
async def get_kpis():
    """Get Key Performance Indicators"""
    try:
        metrics = optimization_engine.get_throughput_metrics()
        
        # Calculate KPIs
        kpis = {
            "punctuality": {
                "value": metrics.get("punctuality_percentage", 0),
                "target": 95.0,
                "status": "good" if metrics.get("punctuality_percentage", 0) >= 95 else "needs_improvement"
            },
            "average_delay": {
                "value": metrics.get("average_delay_minutes", 0),
                "target": 5.0,
                "status": "good" if metrics.get("average_delay_minutes", 0) <= 5 else "needs_improvement"
            },
            "throughput_efficiency": {
                "value": metrics.get("throughput_efficiency", 0),
                "target": 90.0,
                "status": "good" if metrics.get("throughput_efficiency", 0) >= 90 else "needs_improvement"
            },
            "conflict_resolution": {
                "value": len(optimization_engine.conflicts),
                "target": 0,
                "status": "good" if len(optimization_engine.conflicts) == 0 else "needs_attention"
            }
        }
        
        return {"kpis": kpis}
        
    except Exception as e:
        logger.error(f"Error getting KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/generate")
async def generate_test_alert(background_tasks: BackgroundTasks):
    """Generate a test alert for demonstration"""
    try:
        alert_id = f"alert_{len(alerts_db) + 1}"
        alert = Alert(
            id=alert_id,
            type="system_test",
            severity="info",
            message="This is a test alert generated for demonstration purposes",
            timestamp=datetime.now(),
            acknowledged=False
        )
        
        alerts_db.append(alert)
        
        # Broadcast alert
        background_tasks.add_task(broadcast_alert, alert)
        
        logger.info(f"Generated test alert {alert_id}")
        return {"message": f"Test alert {alert_id} generated"}
        
    except Exception as e:
        logger.error(f"Error generating test alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/summary")
async def get_summary_report():
    """Get summary report for the current period"""
    try:
        # Get metrics for the last 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_metrics = [
            metrics for metrics in performance_history
            if metrics.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return {"message": "No data available for the specified period"}
        
        # Calculate summary statistics
        punctuality_values = [m.punctuality_percentage for m in recent_metrics]
        delay_values = [m.average_delay_minutes for m in recent_metrics]
        throughput_values = [m.throughput_efficiency for m in recent_metrics]
        
        summary = {
            "period": "Last 24 hours",
            "data_points": len(recent_metrics),
            "punctuality": {
                "average": sum(punctuality_values) / len(punctuality_values),
                "min": min(punctuality_values),
                "max": max(punctuality_values)
            },
            "average_delay": {
                "average": sum(delay_values) / len(delay_values),
                "min": min(delay_values),
                "max": max(delay_values)
            },
            "throughput_efficiency": {
                "average": sum(throughput_values) / len(throughput_values),
                "min": min(throughput_values),
                "max": max(throughput_values)
            },
            "total_conflicts": sum(m.conflicts_detected for m in recent_metrics),
            "generated_at": datetime.now().isoformat()
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def broadcast_alert(alert: Alert):
    """Broadcast alert via WebSocket"""
    try:
        await websocket_manager.broadcast({
            "type": "alert",
            "alert": alert.dict(),
            "timestamp": time.time()
        })
    except Exception as e:
        logger.error(f"Error broadcasting alert: {e}")

# Background task to generate alerts based on metrics
async def monitor_and_alert():
    """Background task to monitor metrics and generate alerts"""
    while True:
        try:
            metrics = optimization_engine.get_throughput_metrics()
            
            # Check for alert conditions
            if metrics.get("punctuality_percentage", 0) < 80:
                alert = Alert(
                    id=f"alert_punctuality_{int(time.time())}",
                    type="performance",
                    severity="warning",
                    message=f"Punctuality dropped to {metrics.get('punctuality_percentage', 0):.1f}%",
                    timestamp=datetime.now(),
                    acknowledged=False
                )
                alerts_db.append(alert)
                await broadcast_alert(alert)
            
            if metrics.get("average_delay_minutes", 0) > 15:
                alert = Alert(
                    id=f"alert_delay_{int(time.time())}",
                    type="performance",
                    severity="critical",
                    message=f"Average delay increased to {metrics.get('average_delay_minutes', 0):.1f} minutes",
                    timestamp=datetime.now(),
                    acknowledged=False
                )
                alerts_db.append(alert)
                await broadcast_alert(alert)
            
            if metrics.get("conflicts_detected", 0) > 5:
                alert = Alert(
                    id=f"alert_conflicts_{int(time.time())}",
                    type="conflict",
                    severity="warning",
                    message=f"{metrics.get('conflicts_detected', 0)} conflicts detected",
                    timestamp=datetime.now(),
                    acknowledged=False
                )
                alerts_db.append(alert)
                await broadcast_alert(alert)
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Error in monitor_and_alert: {e}")
            await asyncio.sleep(60)
