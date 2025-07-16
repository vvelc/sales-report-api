"""
Sales Report API
FastAPI application for generating PDF sales reports from CSV data.
Author: Victor Velazquez
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import reports
from app.config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sales Report API",
    description="API for generating PDF sales reports from CSV data - Invntio SRL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])

@app.get("/", summary="Health check")
async def root():
    """Root endpoint for health check."""
    return {
        "status": "Sales Report API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "author": "Victor Velazquez - Invntio SRL"
    }

@app.get("/health", summary="API health status")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sales-report-api"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )