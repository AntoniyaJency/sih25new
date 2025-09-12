#!/usr/bin/env python3
"""
Railway Traffic Control System Demo Script

This script demonstrates the key features of the AI-powered train traffic control system
by creating sample data and running optimization scenarios.
"""

import asyncio
import json
from datetime import datetime, timedelta
from app.core.optimization_engine import OptimizationEngine, Train, TrackSection

async def create_sample_data():
    """Create sample trains and track sections for demonstration"""
    
    # Initialize optimization engine
    engine = OptimizationEngine()
    
    # Create sample track sections
    sections = [
        TrackSection(
            id="section_1",
            name="Mumbai-Delhi Main Line",
            start_station="Mumbai Central",
            end_station="Delhi",
            length=1384,
            max_speed=160,
            capacity=8,
            gradient=2.5,
            signal_spacing=2.0,
            maintenance_windows=[]
        ),
        TrackSection(
            id="section_2",
            name="Mumbai-Thane Suburban",
            start_station="Mumbai Central",
            end_station="Thane",
            length=35,
            max_speed=80,
            capacity=12,
            gradient=1.0,
            signal_spacing=1.5,
            maintenance_windows=[]
        ),
        TrackSection(
            id="section_3",
            name="Chennai-Bangalore Line",
            start_station="Chennai",
            end_station="Bangalore",
            length=362,
            max_speed=120,
            capacity=6,
            gradient=3.2,
            signal_spacing=2.5,
            maintenance_windows=[]
        )
    ]
    
    for section in sections:
        engine.add_section(section)
    
    # Create sample trains
    base_time = datetime.now()
    trains = [
        Train(
            id="train_1",
            train_number="12345",
            train_type="express",
            priority=8,
            origin="Mumbai Central",
            destination="Delhi",
            scheduled_departure=base_time + timedelta(minutes=0),
            scheduled_arrival=base_time + timedelta(minutes=390),
            current_location="Mumbai Central",
            speed=120,
            length=450,
            weight=1200,
            status="running"
        ),
        Train(
            id="train_2",
            train_number="67890",
            train_type="local",
            priority=5,
            origin="Mumbai Central",
            destination="Thane",
            scheduled_departure=base_time + timedelta(minutes=5),
            scheduled_arrival=base_time + timedelta(minutes=50),
            current_location="Mumbai Central",
            speed=60,
            length=200,
            weight=400,
            status="scheduled"
        ),
        Train(
            id="train_3",
            train_number="11111",
            train_type="freight",
            priority=6,
            origin="Chennai",
            destination="Bangalore",
            scheduled_departure=base_time + timedelta(minutes=10),
            scheduled_arrival=base_time + timedelta(minutes=380),
            current_location="Chennai",
            speed=80,
            length=600,
            weight=2000,
            status="scheduled"
        ),
        Train(
            id="train_4",
            train_number="22222",
            train_type="express",
            priority=9,
            origin="Delhi",
            destination="Mumbai Central",
            scheduled_departure=base_time + timedelta(minutes=15),
            scheduled_arrival=base_time + timedelta(minutes=405),
            current_location="Delhi",
            speed=130,
            length=450,
            weight=1200,
            status="running"
        ),
        Train(
            id="train_5",
            train_number="33333",
            train_type="special",
            priority=10,
            origin="Mumbai Central",
            destination="Thane",
            scheduled_departure=base_time + timedelta(minutes=8),
            scheduled_arrival=base_time + timedelta(minutes=53),
            current_location="Mumbai Central",
            speed=70,
            length=300,
            weight=600,
            status="scheduled"
        )
    ]
    
    for train in trains:
        engine.add_train(train)
    
    return engine

async def demonstrate_conflict_detection(engine):
    """Demonstrate conflict detection capabilities"""
    print("\n🔍 CONFLICT DETECTION DEMONSTRATION")
    print("=" * 50)
    
    conflicts = engine.detect_conflicts()
    
    if conflicts:
        print(f"✅ Detected {len(conflicts)} conflicts:")
        for i, conflict in enumerate(conflicts, 1):
            print(f"\n{i}. Conflict Type: {conflict.conflict_type.upper()}")
            print(f"   Trains: {conflict.train1_id} ↔ {conflict.train2_id}")
            print(f"   Section: {conflict.section_id}")
            print(f"   Severity: {conflict.severity:.2f}")
            print(f"   Resolution Options: {len(conflict.resolution_options)}")
            
            for j, option in enumerate(conflict.resolution_options, 1):
                print(f"     {j}. {option['action']} - Train {option['train_id']}")
                if 'delay_minutes' in option:
                    print(f"        Delay: {option['delay_minutes']} minutes")
    else:
        print("✅ No conflicts detected")

async def demonstrate_optimization(engine):
    """Demonstrate optimization capabilities"""
    print("\n⚡ OPTIMIZATION DEMONSTRATION")
    print("=" * 50)
    
    print("Running optimization algorithm...")
    result = engine.optimize_schedule()
    
    print(f"✅ Optimization Status: {result['status']}")
    
    if result['status'] in ['optimal', 'feasible']:
        print(f"📊 Total Delay: {result.get('total_delay', 0)} minutes")
        print(f"🔧 Conflicts Resolved: {result.get('conflicts_resolved', 0)}")
        
        if 'solution' in result:
            print("\n📋 Optimized Schedule:")
            for train_id, schedule in result['solution'].items():
                print(f"   {train_id}: Delay {schedule.get('delay_minutes', 0)} minutes")
    else:
        print(f"❌ Optimization failed: {result.get('message', 'Unknown error')}")

async def demonstrate_metrics(engine):
    """Demonstrate performance metrics"""
    print("\n📈 PERFORMANCE METRICS DEMONSTRATION")
    print("=" * 50)
    
    metrics = engine.get_throughput_metrics()
    
    print(f"🚂 Total Trains: {metrics['total_trains']}")
    print(f"🏃 Running Trains: {metrics['running_trains']}")
    print(f"⏰ Delayed Trains: {metrics['delayed_trains']}")
    print(f"❌ Cancelled Trains: {metrics['cancelled_trains']}")
    print(f"📊 Average Delay: {metrics['average_delay_minutes']:.1f} minutes")
    print(f"✅ Punctuality: {metrics['punctuality_percentage']:.1f}%")
    print(f"🔧 Conflicts Detected: {metrics['conflicts_detected']}")
    print(f"⚡ Throughput Efficiency: {metrics['throughput_efficiency']:.1f}%")

async def demonstrate_disruption_handling(engine):
    """Demonstrate disruption handling capabilities"""
    print("\n🚨 DISRUPTION HANDLING DEMONSTRATION")
    print("=" * 50)
    
    print("Simulating train delay disruption...")
    result = engine.reoptimize_on_disruption("delay", ["train_2"])
    
    print(f"✅ Re-optimization Status: {result['status']}")
    print(f"📊 New Total Delay: {result.get('total_delay', 0)} minutes")
    print(f"🔧 Conflicts After Re-optimization: {result.get('conflicts_resolved', 0)}")

async def demonstrate_simulation_scenarios():
    """Demonstrate simulation capabilities"""
    print("\n🎯 SIMULATION SCENARIOS DEMONSTRATION")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "Express Train Delay",
            "description": "30-minute delay on express train",
            "impact": "Cascading delays, reduced punctuality"
        },
        {
            "name": "Track Maintenance",
            "description": "50% capacity reduction on main line",
            "impact": "Rerouting required, increased travel time"
        },
        {
            "name": "Priority Adjustment",
            "description": "Increase freight train priority",
            "impact": "Improved freight movement, potential passenger delays"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Expected Impact: {scenario['impact']}")

async def main():
    """Main demonstration function"""
    print("🚂 RAILWAY TRAFFIC CONTROL SYSTEM DEMO")
    print("=" * 60)
    print("AI-Powered Train Traffic Control for Maximizing Section Throughput")
    print("Smart India Hackathon 2025 - Ministry of Railways")
    print("=" * 60)
    
    # Create sample data
    engine = await create_sample_data()
    print(f"✅ Created {len(engine.trains)} trains and {len(engine.sections)} track sections")
    
    # Run demonstrations
    await demonstrate_conflict_detection(engine)
    await demonstrate_optimization(engine)
    await demonstrate_metrics(engine)
    await demonstrate_disruption_handling(engine)
    await demonstrate_simulation_scenarios()
    
    print("\n🎉 DEMONSTRATION COMPLETED")
    print("=" * 60)
    print("Key Features Demonstrated:")
    print("✅ Real-time conflict detection")
    print("✅ AI-powered optimization algorithms")
    print("✅ Performance metrics and KPIs")
    print("✅ Disruption handling and re-optimization")
    print("✅ What-if simulation scenarios")
    print("✅ Comprehensive monitoring dashboard")
    print("\n🚀 To run the full system:")
    print("   1. Backend: python -m uvicorn app.main:app --reload")
    print("   2. Frontend: cd frontend && npm run dev")
    print("   3. Access: http://localhost:3000")

if __name__ == "__main__":
    asyncio.run(main())
