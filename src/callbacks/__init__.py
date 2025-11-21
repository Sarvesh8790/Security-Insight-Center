"""
Callback registration module
Imports and registers all dashboard callbacks
"""
from src.callbacks.filter_callbacks import register_filter_callbacks
from src.callbacks.chart_callbacks import register_chart_callbacks
from src.callbacks.builder_callbacks import register_builder_callbacks

def register_all_callbacks(app):
    """
    Register all application callbacks
    
    Args:
        app: Dash application instance
    """
    register_filter_callbacks(app)
    register_chart_callbacks(app)
    register_builder_callbacks(app)
