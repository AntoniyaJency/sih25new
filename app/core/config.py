from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/railway_control"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Optimization
    optimization_timeout: int = 30  # seconds
    max_optimization_iterations: int = 1000
    
    # WebSocket
    websocket_heartbeat_interval: int = 30  # seconds
    
    # External APIs
    signalling_system_url: Optional[str] = None
    tms_url: Optional[str] = None
    rolling_stock_url: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
