# AI-Powered Railway Traffic Control System

An intelligent decision-support system that assists section controllers in making optimized, real-time decisions for train precedence and crossings to maximize section throughput and minimize overall train travel time.

## Features

- **Real-time Optimization**: AI-powered algorithms for train precedence and scheduling
- **Conflict Resolution**: Automatic detection and resolution of train conflicts
- **What-if Simulation**: Scenario analysis for alternative routings and strategies
- **Performance Monitoring**: Comprehensive KPIs and dashboards
- **Integration Ready**: APIs for railway control systems integration
- **User-friendly Interface**: Intuitive dashboard for traffic controllers

## Architecture

- **Backend**: FastAPI with Python optimization engines
- **Frontend**: Next.js with React and TypeScript
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Optimization**: Google OR-Tools and custom algorithms
- **Real-time**: WebSocket connections for live updates
- **Caching**: Redis for performance optimization

## Quick Start

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install Node.js dependencies
npm install

# Run the frontend development server
npm run dev
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## System Components

1. **Optimization Engine**: Core algorithms for train scheduling and conflict resolution
2. **Data Models**: Comprehensive models for trains, tracks, signals, and constraints
3. **API Layer**: RESTful endpoints for all operations
4. **Frontend Dashboard**: Real-time monitoring and control interface
5. **Simulation Engine**: What-if analysis and scenario planning
6. **Integration Layer**: Secure APIs for railway control systems
7. **Monitoring**: Performance dashboards and KPI tracking

## Key Algorithms

- **Constraint Satisfaction**: Multi-objective optimization with safety constraints
- **Dynamic Programming**: Real-time re-optimization under disruptions
- **Machine Learning**: Predictive models for delay patterns
- **Graph Theory**: Network flow optimization for train routing

## License

This project is developed for the Smart India Hackathon 2025.
