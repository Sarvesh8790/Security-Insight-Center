from dash import Input, Output, State
from src.data.loader import load_security_data, get_filtered_data
from src.components.charts import (
    create_severity_pie_chart,
    create_trend_line_chart,
    create_severity_by_week_chart,
    create_source_bar_chart,
    create_category_treemap,
    create_top_repos_chart,
    create_custom_chart,
    create_risk_gauge,
    create_attack_timeline_heatmap
)
from src.components.tables import create_findings_table
from src.utils.logger import logger

def register_chart_callbacks(app):
    """Register chart update and click-to-drill callbacks"""
    
    # Main dashboard charts update
    @app.callback(
        [Output("risk-gauge", "figure"),
         Output("severity-chart", "figure"),
         Output("trend-chart", "figure"),
         Output("severity-week-chart", "figure"),
         Output("source-chart", "figure"),
         Output("category-chart", "figure"),
         Output("repos-chart", "figure"),
         Output("attack-heatmap", "figure")],
        [Input("source-filter", "value"),
         Input("severity-filter", "value"),
         Input("status-filter", "value"),
         Input("team-filter", "value"),
         Input("repo-filter", "value"),
         Input("refresh-interval", "n_intervals")]
    )
    def update_all_charts(source_val, severity_val, status_val, team_val, repo_val, n):
        """Update all main dashboard charts including new visualizations"""
        try:
            df = load_security_data()
            filtered = get_filtered_data(df, source_val, severity_val, 
                                        status_val, team_val, repo_val)
            
            # Debug prints (optional - can be removed in production)
            logger.info(f"Filtered data: {len(filtered)} rows")
            
            risk_fig = create_risk_gauge(filtered)
            severity_fig = create_severity_pie_chart(filtered)
            trend_fig = create_trend_line_chart(filtered)
            severity_week_fig = create_severity_by_week_chart(filtered)
            source_fig = create_source_bar_chart(filtered)
            category_fig = create_category_treemap(filtered)
            repos_fig = create_top_repos_chart(filtered)
            heatmap_fig = create_attack_timeline_heatmap(filtered, time_granularity="W", by="Repo/Account")
            
            return (risk_fig, severity_fig, trend_fig, severity_week_fig,
                    source_fig, category_fig, repos_fig, heatmap_fig)
            
        except Exception as e:
            logger.error(f"Error updating charts: {e}")
            from plotly import graph_objects as go
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Error loading data")
            return (empty_fig, empty_fig, empty_fig, empty_fig,
                    empty_fig, empty_fig, empty_fig, empty_fig)
    
    # Click-to-drill: Update table based on any chart click
    @app.callback(
        [Output("findings-table-container", "children"),
         Output("selection-info", "children")],
        [Input("severity-chart", "clickData"),
         Input("trend-chart", "clickData"),
         Input("severity-week-chart", "clickData"),
         Input("source-chart", "clickData"),
         Input("category-chart", "clickData"),
         Input("repos-chart", "clickData"),
         Input("source-filter", "value"),
         Input("severity-filter", "value"),
         Input("status-filter", "value"),
         Input("team-filter", "value"),
         Input("repo-filter", "value")]
    )
    def update_table_on_click(sev_click, trend_click, sev_week_click, 
                             source_click, cat_click, repo_click,
                             source_val, severity_val, status_val, team_val, repo_val):
        """Update findings table based on chart clicks"""
        try:
            df = load_security_data()
            filtered = get_filtered_data(df, source_val, severity_val, 
                                        status_val, team_val, repo_val)
            
            # Determine which chart was clicked
            from dash import callback_context
            if not callback_context.triggered:
                table = create_findings_table(filtered)
                return table, f"Showing all {len(filtered)} findings"
            
            trigger_id = callback_context.triggered[0]["prop_id"].split(".")[0]
            
            # Filter based on clicked element
            drill_filtered = filtered.copy()
            info_text = f"Showing all {len(filtered)} findings"
            
            if "severity-chart" in trigger_id and sev_click:
                severity = sev_click["points"][0]["label"]
                drill_filtered = filtered[filtered["Severity"] == severity]
                info_text = f"Filtered: {severity} severity ({len(drill_filtered)} findings)"
            
            elif "trend-chart" in trigger_id and trend_click:
                date = trend_click["points"][0]["x"]
                drill_filtered = filtered[filtered["Opened_At"].dt.date.astype(str) == date]
                info_text = f"Filtered: Date {date} ({len(drill_filtered)} findings)"
            
            elif "severity-week-chart" in trigger_id and sev_week_click:
                week = sev_week_click["points"][0]["x"]
                severity = sev_week_click["points"][0]["legendgroup"]
                drill_filtered = filtered[(filtered["Week_Number"] == week) & 
                                         (filtered["Severity"] == severity)]
                info_text = f"Filtered: Week {week}, {severity} ({len(drill_filtered)} findings)"
            
            elif "source-chart" in trigger_id and source_click:
                source = source_click["points"][0]["x"]
                drill_filtered = filtered[filtered["Source"] == source]
                info_text = f"Filtered: Source {source} ({len(drill_filtered)} findings)"
            
            elif "category-chart" in trigger_id and cat_click:
                category = cat_click["points"][0]["label"]
                drill_filtered = filtered[filtered["Category"] == category]
                info_text = f"Filtered: Category {category} ({len(drill_filtered)} findings)"
            
            elif "repos-chart" in trigger_id and repo_click:
                repo = repo_click["points"][0]["y"]
                drill_filtered = filtered[filtered["Repo/Account"] == repo]
                info_text = f"Filtered: Repository {repo} ({len(drill_filtered)} findings)"
            
            table = create_findings_table(drill_filtered)
            return table, info_text
            
        except Exception as e:
            logger.error(f"Error in click-to-drill: {e}")
            return "Error loading table", "Error"