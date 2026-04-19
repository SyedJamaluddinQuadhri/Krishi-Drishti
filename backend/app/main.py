"""
Krishi Drishti - FastAPI Main Application
AI-Powered Crop Advisory Platform for Indian Farmers
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from app.config import settings
from app.database import engine, Base
from app.routers import auth, farm, recommend, plan
from app.utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events"""
    logger.info("Starting Krishi Drishti API Server...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
    # Load ML models
    try:
        from app.services.ml_service import load_models
        load_models()
        logger.info("ML models loaded successfully")
    except Exception as e:
        logger.warning(f"ML models not loaded: {e}")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Krishi Drishti API Server...")

# Initialize FastAPI app
app = FastAPI(
    title="Krishi Drishti API",
    description="AI-Powered Crop Advisory Platform for Indian Farmers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000", "https://krishidrishti.com", "https://www.krishidrishti.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (security)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.krishidrishti.com", "krishidrishti.com"]
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(farm.router, prefix="/farm", tags=["Farm Management"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendations"])
app.include_router(plan.router, prefix="/plan", tags=["Yield Planning"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "success": True,
        "message": "Welcome to Krishi Drishti API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "operational"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "success": True,
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT
    }

# API Status endpoint
@app.get("/api/status", tags=["Health"])
async def api_status():
    """Detailed API status including database and ML models"""
    from app.database import SessionLocal
    
    status_info = {
        "api": "operational",
        "database": "unknown",
        "ml_models": "unknown"
    }
    
    # Check database connection
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        status_info["database"] = "connected"
    except Exception as e:
        status_info["database"] = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    # Check ML models
    try:
        from app.services.ml_service import models_loaded
        status_info["ml_models"] = "loaded" if models_loaded else "not_loaded"
    except Exception as e:
        status_info["ml_models"] = f"error: {str(e)}"
    
    return {
        "success": True,
        "status": status_info,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
