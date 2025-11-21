from dash import dcc, html
from src.data.loader import load_security_data, get_filter_options
from src.components.kpi_cards import create_kpi_card, create_kpi_row
from src.layouts.chart_builder import create_chart_builder_panel
from config.settings import AUTO_REFRESH_INTERVAL
from config.theme import CYBER_THEME

def create_layout():
    """Create the complete dashboard layout with top filters and right sidebar"""
    
    # Load initial data
    df = load_security_data()
    filter_options = get_filter_options(df)
    builder_columns = [c for c in df.columns if c not in ["tool_url", "View_Link"]]
    
    return html.Div([
        # Hidden store for chart builder state
        dcc.Store(id="custom-charts-store", data=[]),
        
        # Header
        html.Div([
            html.H1("🛡️ Security Insights Center", 
                   style={"textAlign": "center", "marginBottom": "8px", "fontSize": "2.5rem"}),
            html.P("Unified Security Dashboard - GHAS, AWS Security Hub & Multi-Tool Integration",
                  style={"textAlign": "center", "color": "#9ca3af", "marginBottom": "24px", "fontSize": "1.1rem"})
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id="refresh-interval",
            interval=AUTO_REFRESH_INTERVAL,
            n_intervals=0
        ),
        
        # TOP BAR: Collapsible Filters
        html.Div([
            html.Div([
                html.Button(
                    "🔽 Hide Filters",
                    id="toggle-filters",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "backgroundColor": CYBER_THEME["accent"],
                        "color": "white",
                        "border": "none",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "fontSize": "15px",
                        "fontWeight": "600",
                        "marginBottom": "16px"
                    }
                ),
                html.Button(
                    "🔄 Reset All Filters",
                    id="reset-filters-btn",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "backgroundColor": CYBER_THEME["warning"],
                        "color": "white",
                        "border": "none",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "fontSize": "15px",
                        "fontWeight": "600",
                        "marginBottom": "16px",
                        "marginLeft": "12px"
                    }
                )
            ]),
            
            # Filters Container (Collapsible)
            html.Div([
                html.Div([
                    # Source Filter
                    html.Div([
                        html.Label("Source", style={"fontWeight": "600", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="source-filter",
                            options=[{"label": opt, "value": opt} for opt in filter_options["sources"]],
                            multi=True,
                            placeholder="All Sources",
                            style={"minWidth": "200px"}
                        )
                    ], style={"flex": "1", "minWidth": "200px", "marginRight": "16px"}),
                    
                    # Severity Filter
                    html.Div([
                        html.Label("Severity", style={"fontWeight": "600", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="severity-filter",
                            options=[{"label": opt, "value": opt} for opt in filter_options["severities"]],
                            multi=True,
                            placeholder="All Severities",
                            style={"minWidth": "200px"}
                        )
                    ], style={"flex": "1", "minWidth": "200px", "marginRight": "16px"}),
                    
                    # Status Filter
                    html.Div([
                        html.Label("Status", style={"fontWeight": "600", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="status-filter",
                            options=[{"label": opt, "value": opt} for opt in filter_options["statuses"]],
                            multi=True,
                            placeholder="All Statuses",
                            style={"minWidth": "200px"}
                        )
                    ], style={"flex": "1", "minWidth": "200px", "marginRight": "16px"}),
                    
                    # Team Filter
                    html.Div([
                        html.Label("Team", style={"fontWeight": "600", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="team-filter",
                            options=[{"label": opt, "value": opt} for opt in filter_options["teams"]],
                            multi=True,
                            placeholder="All Teams",
                            style={"minWidth": "200px"}
                        )
                    ], style={"flex": "1", "minWidth": "200px", "marginRight": "16px"}),
                    
                    # Repository Filter
                    html.Div([
                        html.Label("Repository", style={"fontWeight": "600", "marginBottom": "6px", "display": "block"}),
                        dcc.Dropdown(
                            id="repo-filter",
                            options=[{"label": opt, "value": opt} for opt in filter_options["repos"]],
                            multi=True,
                            placeholder="All Repositories",
                            style={"minWidth": "200px"}
                        )
                    ], style={"flex": "1", "minWidth": "200px"}),
                    
                ], style={
                    "display": "flex",
                    "gap": "16px",
                    "flexWrap": "wrap",
                    "alignItems": "flex-end"
                })
            ], id="filters-container", style={
                "display": "block",
                "padding": "20px",
                "backgroundColor": CYBER_THEME["bg_card"],
                "borderRadius": "8px",
                "border": f"1px solid {CYBER_THEME['border_glow']}",
                "marginBottom": "24px"
            })
        ]),
        
        # KPI Cards Row
        create_kpi_row([
            create_kpi_card("Total Findings", "0", card_id="total-findings"),
            create_kpi_card("Open Findings", "0", card_id="open-findings"),
            create_kpi_card("Critical Open", "0", card_id="critical-open"),
            create_kpi_card("Avg MTTR", "0h", card_id="avg-mttr")
        ]),
        
        # Main Content Area - Charts (Left) + Chart Builder (Right Sidebar)
        html.Div([
            # LEFT: Main Charts Area
            html.Div([
                # ROW 1: Severity Pie + Trend Line (2 graphs side by side)
                html.Div([
                    html.Div([
                        dcc.Graph(id="severity-chart")
                    ], style={"flex": "1", "minWidth": "350px"}),
                    html.Div([
                        dcc.Graph(id="trend-chart")
                    ], style={"flex": "1", "minWidth": "350px"}),
                ], style={
                    "display": "flex",
                    "gap": "16px",
                    "marginBottom": "24px",
                    "flexWrap": "wrap"
                }),
                
                # ROW 2: Severity by Week (Full width)
                html.Div([
                    dcc.Graph(id="severity-week-chart")
                ], style={"marginBottom": "24px"}),
                
                # ROW 3: All remaining graphs (3 graphs in a row)
                html.Div([
                    html.Div([
                        dcc.Graph(id="source-chart")
                    ], style={"flex": "1", "minWidth": "280px"}),
                    html.Div([
                        dcc.Graph(id="category-chart")
                    ], style={"flex": "1", "minWidth": "280px"}),
                    html.Div([
                        dcc.Graph(id="repos-chart")
                    ], style={"flex": "1", "minWidth": "280px"}),
                ], style={
                    "display": "flex",
                    "gap": "16px",
                    "marginBottom": "24px",
                    "flexWrap": "wrap"
                }),
                # ROW 4: Custom Charts Section
                html.Div([
                    html.Div([
                        html.H3("🎨 Custom Charts", 
                               style={"marginBottom": "12px", "color": CYBER_THEME["accent"]}),
                        html.P("Charts created with the Chart Builder appear here",
                              style={"color": CYBER_THEME["text_muted"], "fontSize": "13px", "marginBottom": "16px"})
                    ]),
                    html.Div(id="custom-charts-container-inline")
                ], style={
                    "marginBottom": "32px",
                    "padding": "20px",
                    "backgroundColor": CYBER_THEME["bg_card"],
                    "borderRadius": "8px",
                    "border": f"1px solid {CYBER_THEME['border_glow']}"
                }),
                
                # Click instruction
                html.Div([
                    html.P("💡 Click on any chart to view detailed findings below", 
                          style={
                              "textAlign": "center",
                              "color": CYBER_THEME["accent"],
                              "fontSize": "14px",
                              "fontStyle": "italic",
                              "marginBottom": "16px"
                          })
                ]),
                # KPI Cards Row + Risk Gauge
                html.Div([
                    html.Div(
                        create_kpi_row([
                            create_kpi_card("Total Findings", "0", card_id="total-findings"),
                            create_kpi_card("Open Findings", "0", card_id="open-findings"),
                            create_kpi_card("Critical Open", "0", card_id="critical-open"),
                            create_kpi_card("Avg MTTR", "0h", card_id="avg-mttr"),
                        ]),
                        style={"flex": "1"}
                    ),
                    html.Div(
                        dcc.Graph(id="risk-gauge"),
                        style={"flex": "0 0 320px", "marginLeft": "16px"}
                    ),
                ], style={"display": "flex", "flexWrap": "wrap", "gap": "16px", "marginBottom": "16px"}),

                # Findings Table
                html.Div([
                    html.Div([
                        html.H3("📋 Findings Details", 
                               style={"display": "inline-block", "marginRight": "16px"}),
                        html.Span(id="selection-info", 
                                 style={"color": CYBER_THEME["accent"], "fontSize": "14px"})
                    ], style={"marginBottom": "16px"}),
                    html.Div(id="findings-table-container")
                ])
                
            ], style={"flex": "1", "marginRight": "24px"}),
            # ROW 3.5: Attack Timeline Heatmap (full width)
            html.Div([
                dcc.Graph(id="attack-heatmap")
            ], style={"marginBottom": "24px"}),

            # Trend summary text (WoW / MoM)
            html.Div(
                id="trend-summary",
                style={"color": CYBER_THEME["text_muted"], "fontSize": "12px", "marginBottom": "12px"}
            ),

            
            # RIGHT SIDEBAR: Chart Builder
            html.Div([
                html.Div([
                    html.Button(
                        "📊 Chart Builder",
                        id="toggle-builder",
                        n_clicks=0,
                        style={
                            "width": "100%",
                            "padding": "12px",
                            "backgroundColor": CYBER_THEME["accent_soft"],
                            "color": "white",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": "15px",
                            "fontWeight": "600",
                            "marginBottom": "16px"
                        }
                    ),
                    html.Div(
                        create_chart_builder_panel(builder_columns),
                        id="builder-container",
                        style={"display": "block"}  # Always visible on right side
                    )
                ])
            ], style={
                "flex": "0 0 320px",
                "maxHeight": "calc(100vh - 200px)",
                "overflowY": "auto",
                "position": "sticky",
                "top": "20px"
            })
            
        ], style={"display": "flex"}),
        
    ], className="dashboard-root", style={
        "padding": "20px",
        "maxWidth": "2000px",
        "margin": "0 auto",
        "minHeight": "100vh"
    })