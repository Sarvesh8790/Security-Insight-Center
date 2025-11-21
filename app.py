"""
Security Insights Center - Enhanced Modular Application
Includes: Custom Chart Builder, Click-to-Drill, All Original Features
"""
import dash
from dash import dcc, html
from src.layouts.main_layout import create_layout
from src.callbacks import register_all_callbacks
from config.settings import DEBUG, PORT, HOST
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger()

# Initialize Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "Security Insights Center"
server = app.server

# Set layout
app.layout = create_layout()

# Register all callbacks
register_all_callbacks(app)

if __name__ == "__main__":
    logger.info(f"Starting Security Insights Center on {HOST}:{PORT}")
    app.run_server(debug=DEBUG, host=HOST, port=PORT)
