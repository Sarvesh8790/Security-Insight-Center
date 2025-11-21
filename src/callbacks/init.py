"""
Callback registration
"""
from src.callbacks.filter_callbacks import register_filter_callbacks
from src.callbacks.chart_callbacks import register_chart_callbacks

def register_all_callbacks(app):
    """Register all application callbacks"""
    register_filter_callbacks(app)
    register_chart_callbacks(app)
