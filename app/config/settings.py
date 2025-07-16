"""
Application settings and configuration.
Author: Victor Velazquez - Invntio SRL
"""

import os
from typing import List

class Settings:
    """Application settings."""
    
    # API Settings
    API_NAME: str = "Sales Report API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # Directory Settings
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    REPORTS_DIR: str = os.path.join(BASE_DIR, "reports")
    
    # File Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS: List[str] = [".csv"]

settings = Settings()