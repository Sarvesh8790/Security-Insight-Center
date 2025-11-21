"""
Utility helper functions
"""
import pandas as pd
from datetime import datetime, timezone

def format_timestamp(ts):
    """Format timestamp for display"""
    if pd.isna(ts):
        return "N/A"
    return ts.strftime("%Y-%m-%d %H:%M")

def calculate_age_hours(opened_at):
    """Calculate how many hours since finding was opened"""
    if pd.isna(opened_at):
        return 0
    now = datetime.now(timezone.utc)
    if opened_at.tzinfo is None:
        opened_at = opened_at.replace(tzinfo=timezone.utc)
    delta = now - opened_at
    return delta.total_seconds() / 3600

def get_severity_order():
    """Return severity levels in priority order"""
    return ["Critical", "High", "Medium", "Low"]

def get_status_order():
    """Return status values in logical order"""
    return ["Open", "In Progress", "Closed"]

def safe_divide(numerator, denominator, default=0):
    """Safe division with default value"""
    if denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator
