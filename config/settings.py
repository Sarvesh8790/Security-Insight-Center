"""
Application configuration and environment settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application settings
DEBUG = os.getenv("DEBUG", "True") == "True"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8050))

# Data settings
DATA_PATH = os.getenv("DATA_PATH", "data/security_findings_unified.csv")
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))  # 5 minutes

# Security settings
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

# Refresh settings
AUTO_REFRESH_INTERVAL = int(os.getenv("AUTO_REFRESH_INTERVAL", 300000))  # 5 min in ms

# SLA Configuration
SLA_HOURS_CRITICAL = int(os.getenv("SLA_HOURS_CRITICAL", 24))
SLA_HOURS_HIGH = int(os.getenv("SLA_HOURS_HIGH", 72))
SLA_HOURS_MEDIUM = int(os.getenv("SLA_HOURS_MEDIUM", 168))
