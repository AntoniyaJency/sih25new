# Railway Traffic Control System - Deployment Guide

## Overview

This AI-powered railway traffic control system is designed to maximize section throughput using intelligent optimization algorithms. The system assists section controllers in making real-time decisions for train precedence and crossings.

## System Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.8+
- **Optimization Engine**: Google OR-Tools with Constraint Programming
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for performance optimization
- **Real-time**: WebSocket connections for live updates

### Frontend (Next.js)
- **Framework**: Next.js 14 with React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts for data visualization
- **State Management**: React hooks and context

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher

### Development Tools
- Git
- pip (Python package manager)
- npm (Node.js package manager)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sih25new
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Database Setup
```bash
# Install PostgreSQL and create database
createdb railway_control

# Set environment variables
cp env.example .env
# Edit .env with your database credentials
```

#### Run Database Migrations
```bash
# Initialize database tables
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Redis Setup
```bash
# Install and start Redis
redis-server
```

## Running the System

### Option 1: Quick Start Script
```bash
./start.sh
```

### Option 2: Manual Start

#### Start Backend
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start Frontend (in another terminal)
```bash
cd frontend
npm start
```

### Option 3: Demo Mode
```bash
python demo.py
```

## Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## Configuration

### Environment Variables
Copy `env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/railway_control

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here

# External APIs
SIGNALLING_SYSTEM_URL=http://signalling-system:8080
TMS_URL=http://tms-system:8080
ROLLING_STOCK_URL=http://rolling-stock:8080
```

## Key Features

### 1. Real-time Optimization
- Constraint programming algorithms
- Multi-objective optimization
- Dynamic re-optimization on disruptions

### 2. Conflict Detection & Resolution
- Automatic conflict detection
- Multiple resolution strategies
- Real-time conflict monitoring

### 3. What-if Simulation
- Scenario analysis
- Performance impact assessment
- Alternative routing strategies

### 4. Performance Monitoring
- Real-time KPIs
- Historical trend analysis
- Alert management system

### 5. Integration Ready
- RESTful APIs
- WebSocket connections
- External system integration

## API Endpoints

### Trains
- `GET /api/trains` - List all trains
- `POST /api/trains` - Create new train
- `PUT /api/trains/{id}` - Update train
- `DELETE /api/trains/{id}` - Delete train

### Sections
- `GET /api/sections` - List track sections
- `POST /api/sections` - Create new section
- `PUT /api/sections/{id}` - Update section

### Optimization
- `POST /api/optimization/optimize` - Run optimization
- `GET /api/optimization/conflicts` - Get conflicts
- `GET /api/optimization/metrics` - Get metrics

### Simulation
- `POST /api/simulation/run` - Run simulation
- `GET /api/simulation/scenarios` - Get scenarios

### Monitoring
- `GET /api/monitoring/metrics` - Get performance metrics
- `GET /api/monitoring/alerts` - Get alerts
- `GET /api/monitoring/dashboard` - Get dashboard data

## Performance Optimization

### Backend Optimization
- Connection pooling for database
- Redis caching for frequent queries
- Asynchronous processing for heavy operations
- Background tasks for optimization

### Frontend Optimization
- Code splitting and lazy loading
- Memoization for expensive calculations
- Virtual scrolling for large datasets
- Optimistic updates for better UX

## Security Considerations

### API Security
- JWT token authentication
- Rate limiting
- Input validation and sanitization
- CORS configuration

### Data Security
- Encrypted database connections
- Secure environment variable handling
- Audit trails for all operations
- Role-based access control

## Monitoring & Logging

### Application Monitoring
- Performance metrics collection
- Error tracking and alerting
- System health monitoring
- Resource usage tracking

### Logging
- Structured logging with timestamps
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Log rotation and retention policies
- Centralized logging for distributed deployment

## Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Check if all dependencies are installed
pip list

# Check database connection
python -c "from app.core.database import engine; print(engine.execute('SELECT 1').fetchone())"

# Check Redis connection
python -c "import redis; r = redis.Redis(); print(r.ping())"
```

#### Frontend Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check build
npm run build
```

#### Performance Issues
- Check database query performance
- Monitor Redis memory usage
- Analyze frontend bundle size
- Review optimization algorithm parameters

## Production Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### Load Balancing
- Use nginx or similar for load balancing
- Configure SSL/TLS certificates
- Set up health checks
- Implement circuit breakers

## Scaling Considerations

### Horizontal Scaling
- Multiple backend instances
- Database read replicas
- Redis cluster setup
- CDN for frontend assets

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching strategies
- Use connection pooling

## Maintenance

### Regular Tasks
- Database backup and cleanup
- Log rotation and archival
- Security updates
- Performance monitoring

### Updates
- Backend: Update requirements.txt and restart
- Frontend: Update package.json and rebuild
- Database: Run migration scripts
- Configuration: Update environment variables

## Support

For technical support or questions:
- Check the API documentation at `/docs`
- Review the demo script: `python demo.py`
- Check system logs for error details
- Monitor performance metrics in the dashboard

## License

This project is developed for the Smart India Hackathon 2025 under the Ministry of Railways.
