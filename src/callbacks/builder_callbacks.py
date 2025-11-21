"""
Custom Chart Builder Callbacks
Handles preview, adding custom charts, and toggle functionality
"""
from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
from dash import dcc, html
import dash
from src.data.loader import load_security_data, get_filtered_data
from src.components.charts import create_custom_chart
from src.utils.logger import logger

def register_builder_callbacks(app):
    """Register all chart builder related callbacks"""
    
    # Toggle filters visibility
    @app.callback(
        [Output("filters-container", "style"),
         Output("toggle-filters", "children")],
        [Input("toggle-filters", "n_clicks")],
        [State("filters-container", "style")]
    )
    def toggle_filters(n_clicks, current_style):
        """Show/hide filters section"""
        if n_clicks and n_clicks % 2 == 1:
            return {"display": "none"}, "🔼 Show Filters"
        else:
            return {"display": "block"}, "🔽 Hide Filters"
    
    # Toggle chart builder visibility
    @app.callback(
    [Output("builder-container", "style"),
     Output("toggle-builder", "children"),
     Output("main-charts-area", "style")],
    [Input("toggle-builder", "n_clicks")]
    )
    def toggle_builder(n_clicks):
        if n_clicks and n_clicks % 2 == 1:
            # Collapsed builder, expand charts
            return (
                {"display": "none"},
                "▶ Show Chart Builder",
                {"flex": "1", "marginRight": "0", "transition": "all 0.3s ease"}
            )
        else:
            # Show builder with fixed width, normal chart area
            return (
                {"display": "block", "flex": "0 0 320px", "maxHeight": "calc(100vh - 200px)",
                 "overflowY": "auto", "position": "sticky", "top": "20px", "transition": "all 0.3s ease"},
                "◀ Hide Chart Builder",
                {"flex": "1", "marginRight": "24px", "transition": "all 0.3s ease"}
            )
   
    # Preview chart in builder
    @app.callback(
        Output("builder-preview-chart", "figure"),
        [Input("preview-chart-btn", "n_clicks"),
         Input("builder-chart-type", "value"),
         Input("builder-x-axis", "value"),
         Input("builder-y-axis", "value"),
         Input("builder-color", "value"),
         Input("source-filter", "value"),
         Input("severity-filter", "value"),
         Input("status-filter", "value"),
         Input("team-filter", "value"),
         Input("repo-filter", "value")]
    )
    def preview_custom_chart(n_clicks, chart_type, x_col, y_col, color_col,
                            source_val, severity_val, status_val, team_val, repo_val):
        """Generate preview of custom chart"""
        try:
            if not x_col or not y_col:
                from plotly import graph_objects as go
                fig = go.Figure()
                fig.update_layout(
                    title="Select X and Y axes to preview",
                    paper_bgcolor="#0E0F14",
                    plot_bgcolor="#0E0F14",
                    font_color="#E5E5F0"
                )
                return fig
            
            # Load and filter data
            df = load_security_data()
            filtered = get_filtered_data(df, source_val, severity_val, 
                                        status_val, team_val, repo_val)
            
            # Create custom chart
            fig = create_custom_chart(filtered, x_col, y_col, chart_type, color_col)
            fig.update_layout(title=f"{chart_type.title()} Chart: {x_col} vs {y_col}")
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating preview chart: {e}")
            from plotly import graph_objects as go
            fig = go.Figure()
            fig.update_layout(
                title=f"Error: {str(e)}",
                paper_bgcolor="#0E0F14",
                plot_bgcolor="#0E0F14",
                font_color="#E5E5F0"
            )
            return fig
    
    # Add custom chart to the custom charts tab
    @app.callback(
        Output("custom-charts-store", "data"),
        [Input("add-custom-chart-btn", "n_clicks")],
        [State("builder-chart-type", "value"),
         State("builder-x-axis", "value"),
         State("builder-y-axis", "value"),
         State("builder-color", "value"),
         State("custom-charts-store", "data")]
    )
    def add_custom_chart(n_clicks, chart_type, x_col, y_col, color_col, current_charts):
        """Add a new custom chart to the store"""
        if not n_clicks or n_clicks == 0:
            raise PreventUpdate
        
        if not x_col or not y_col:
            raise PreventUpdate
        
        # Create chart config
        chart_config = {
            "id": len(current_charts) + 1,
            "type": chart_type,
            "x": x_col,
            "y": y_col,
            "color": color_col if color_col != "None" else None,
            "title": f"{chart_type.title()}: {x_col} vs {y_col}"
        }
        
        current_charts.append(chart_config)
        logger.info(f"Added custom chart: {chart_config['title']}")
        
        return current_charts
    
    # Render custom charts inline in Row 4

    @app.callback(
            Output("custom-charts-container-inline", "children"),
            [Input("custom-charts-store", "data"),
             Input("source-filter", "value"),
             Input("severity-filter", "value"),
             Input("status-filter", "value"),
             Input("team-filter", "value"),
             Input("repo-filter", "value")]
        )
    def render_custom_charts_inline(charts_config, source_val, severity_val,
                                       status_val, team_val, repo_val):
            """Render all custom charts inline in Row 4"""
            if not charts_config or len(charts_config) == 0:
                return html.Div(
                    html.P(
                        "No custom charts yet. Use the Chart Builder to create visualizations.",
                        style={"textAlign": "center", "color": "#6B7280", "padding": "20px"}
                    ),
                    style={"minHeight": "100px"}
                )

            try:
                # Load and filter data
                df = load_security_data()
                filtered = get_filtered_data(df, source_val, severity_val,
                                             status_val, team_val, repo_val)
                # Create chart components in a responsive grid
                chart_components = []
                for chart_cfg in charts_config:
                    try:
                        fig = create_custom_chart(
                            filtered,
                            chart_cfg["x"],
                            chart_cfg["y"],
                            chart_cfg["type"],
                            chart_cfg.get("color")
                        )
                        fig.update_layout(
                            title=chart_cfg["title"],
                            height=350
                        )

                        chart_components.append(
                            html.Div([
                                html.Div([
                                    html.Span(f"Chart {chart_cfg['id']}",
                                              style={"fontWeight": "600", "marginRight": "12px"}),
                                    html.Button(
                                        "✕",
                                        id={"type": "remove-chart", "index": chart_cfg["id"]},
                                        n_clicks=0,
                                        title="Remove this chart",
                                        style={
                                            "padding": "2px 8px",
                                            "backgroundColor": "#EF4444",
                                            "color": "white",
                                            "border": "none",
                                            "borderRadius": "3px",
                                            "cursor": "pointer",
                                            "fontSize": "12px",
                                            "float": "right"
                                        }
                                    )
                                ], style={"marginBottom": "8px"}),
                                dcc.Graph(figure=fig, config={"displayModeBar": False})
                            ], style={
                                "flex": "1 1 calc(50% - 16px)",
                                "minWidth": "400px",
                                "marginBottom": "16px",
                                "padding": "12px",
                                "backgroundColor": "#0E0F14",
                                "borderRadius": "6px",
                                "border": "1px solid #5E5CE6"
                            })
                        )
                    except Exception as e:
                        logger.error(f"Error rendering custom chart {chart_cfg['id']}: {e}")

                return html.Div(
                    chart_components,
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "gap": "16px",
                        "marginTop": "16px"
                    }
                )

            except Exception as e:
                logger.error(f"Error rendering custom charts: {e}")
                return html.Div(
                    f"Error loading custom charts: {str(e)}",
                    style={"color": "#EF4444", "padding": "20px"}
                )

    def remove_custom_chart(n_clicks_list, current_charts):
        """Remove a custom chart from the store"""
        ctx = callback_context
        
        if not ctx.triggered or not any(n_clicks_list):
            raise PreventUpdate
        
        # Find which button was clicked
        triggered_id = ctx.triggered[0]["prop_id"]
        if "remove-chart" in triggered_id:
            import json
            button_id = json.loads(triggered_id.split(".")[0])
            chart_id_to_remove = button_id["index"]
            
            # Remove the chart with matching id
            updated_charts = [c for c in current_charts if c["id"] != chart_id_to_remove]
            logger.info(f"Removed custom chart with id: {chart_id_to_remove}")
            
            return updated_charts
        
        raise PreventUpdate
