#!/usr/bin/env python3
"""
Simple test script to verify the Railway Traffic Control System works
"""

print("🚂 Railway Traffic Control System - Simple Test")
print("=" * 50)

try:
    # Test 1: Import optimization engine
    print("1. Testing optimization engine import...")
    from app.core.optimization_engine import OptimizationEngine, Train, TrackSection
    print("   ✅ Optimization engine imported successfully")
    
    # Test 2: Create optimization engine
    print("2. Testing optimization engine creation...")
    engine = OptimizationEngine()
    print("   ✅ Optimization engine created successfully")
    
    # Test 3: Add sample data
    print("3. Testing data addition...")
    
    # Add a track section
    section = TrackSection(
        id="test_section",
        name="Test Line",
        start_station="Station A",
        end_station="Station B",
        length=100,
        max_speed=120,
        capacity=5,
        gradient=1.0,
        signal_spacing=2.0,
        maintenance_windows=[]
    )
    engine.add_section(section)
    print("   ✅ Track section added")
    
    # Add a train
    from datetime import datetime, timedelta
    train = Train(
        id="test_train",
        train_number="TEST001",
        train_type="express",
        priority=8,
        origin="Station A",
        destination="Station B",
        scheduled_departure=datetime.now(),
        scheduled_arrival=datetime.now() + timedelta(hours=1),
        current_location="Station A",
        speed=100,
        length=300,
        weight=800,
        status="scheduled"
    )
    engine.add_train(train)
    print("   ✅ Train added")
    
    # Test 4: Run optimization
    print("4. Testing optimization...")
    result = engine.optimize_schedule()
    print(f"   ✅ Optimization completed: {result['status']}")
    
    # Test 5: Get metrics
    print("5. Testing metrics...")
    metrics = engine.get_throughput_metrics()
    print(f"   ✅ Metrics retrieved: {metrics['total_trains']} trains")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("The Railway Traffic Control System is working correctly.")
    print("\nTo run the full system:")
    print("1. Backend: python3 -m uvicorn app.main:app --reload")
    print("2. Frontend: cd frontend && npm run dev")
    print("3. Access: http://localhost:3000")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies:")
    print("pip3 install fastapi uvicorn pydantic sqlalchemy numpy scipy ortools pandas")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check the error and try again.")
