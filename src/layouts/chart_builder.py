"""
Custom Chart Builder Panel Component
"""
from dash import dcc, html
from config.theme import CYBER_THEME

def create_chart_builder_panel(columns):
    """
    Create the chart builder UI panel

    Args:
        columns: List of available column names for building charts
    """
    return html.Div([
        html.H4("Build Custom Chart", style={"marginBottom": "16px"}),

        # Chart Type
        html.Label("Chart Type", style={"display": "block", "marginBottom": "4px", "fontSize": "12px"}),
        dcc.Dropdown(
            id="builder-chart-type",
            options=[
                {"label": "Bar Chart", "value": "bar"},
                {"label": "Line Chart", "value": "line"},
                {"label": "Pie Chart", "value": "pie"},
                {"label": "Scatter Plot", "value": "scatter"},
                {"label": "Box Plot", "value": "box"}
            ],
            value="bar",
            clearable=False,
            style={"marginBottom": "12px"}
        ),

        # X-Axis
        html.Label("X-Axis", style={"display": "block", "marginBottom": "4px", "fontSize": "12px"}),
        dcc.Dropdown(
            id="builder-x-axis",
            options=[{"label": c, "value": c} for c in columns],
            value=columns[0] if columns else None,
            clearable=False,
            style={"marginBottom": "12px"}
        ),

        # Y-Axis
        html.Label("Y-Axis", style={"display": "block", "marginBottom": "4px", "fontSize": "12px"}),
        dcc.Dropdown(
            id="builder-y-axis",
            options=[{"label": "Count", "value": "count"}] + [{"label": c, "value": c} for c in columns if c in ["MTTR_Hours", "Week_Number"]],
            value="count",
            clearable=False,
            style={"marginBottom": "12px"}
        ),

        # Color By (optional)
        html.Label("Color By (Optional)", style={"display": "block", "marginBottom": "4px", "fontSize": "12px"}),
        dcc.Dropdown(
            id="builder-color",
            options=[{"label": "None", "value": "None"}] + [{"label": c, "value": c} for c in ["Severity", "Status", "Source", "Category"]],
            value="None",
            clearable=False,
            style={"marginBottom": "16px"}
        ),

        # Buttons
        html.Div([
            html.Button(
                "Preview Chart",
                id="preview-chart-btn",
                n_clicks=0,
                style={
                    "padding": "8px 16px",
                    "backgroundColor": CYBER_THEME["accent"],
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "marginRight": "8px",
                    "fontSize": "13px"
                }
            ),
            html.Button(
                "Add to Custom Charts",
                id="add-custom-chart-btn",
                n_clicks=0,
                style={
                    "padding": "8px 16px",
                    "backgroundColor": CYBER_THEME["accent_soft"],
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontSize": "13px"
                }
            )
        ]),

        # Preview Area
        html.Div([
            html.H5("Preview", style={"marginTop": "20px", "marginBottom": "12px"}),
            dcc.Graph(id="builder-preview-chart", style={"height": "300px"})
        ])

    ], style={
        "padding": "16px",
        "backgroundColor": CYBER_THEME["bg_card"],
        "borderRadius": "8px",
        "border": f"1px solid {CYBER_THEME['border_glow']}"
    })
