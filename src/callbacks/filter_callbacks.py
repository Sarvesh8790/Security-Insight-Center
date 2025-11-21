"""
Filter-related callbacks
"""
from dash import Input, Output, State, callback_context
from src.data.loader import load_security_data, get_filtered_data
from src.utils.metrics import calculate_kpis, calculate_trend_comparison
from src.utils.logger import logger


def register_filter_callbacks(app):
    """Register filter callbacks"""

    @app.callback(
        [Output("total-findings", "children"),
         Output("open-findings", "children"),
         Output("critical-open", "children"),
         Output("avg-mttr", "children")],
        [Input("source-filter", "value"),
         Input("severity-filter", "value"),
         Input("status-filter", "value"),
         Input("team-filter", "value"),
         Input("repo-filter", "value"),
         Input("refresh-interval", "n_intervals")]
    )
    def update_kpis(source_val, severity_val, status_val, team_val, repo_val, n):
        """Update KPI cards based on current filters"""
        try:
            df = load_security_data()
            filtered = get_filtered_data(df, source_val, severity_val,
                                         status_val, team_val, repo_val)
            kpis = calculate_kpis(filtered)

            return (
                str(kpis["total"]),
                str(kpis["open"]),
                str(kpis["critical_open"]),
                f"{kpis['avg_mttr']:.1f}h"
            )
        except Exception as e:
            logger.error(f"Error updating KPIs: {e}")
            return "Error", "Error", "Error", "Error"

    @app.callback(
        [Output("source-filter", "value"),
         Output("severity-filter", "value"),
         Output("status-filter", "value"),
         Output("team-filter", "value"),
         Output("repo-filter", "value")],
        [Input("reset-filters-btn", "n_clicks")]
    )
    def reset_filters(n_clicks):
        """Reset all filters to None"""
        if n_clicks and n_clicks > 0:
            return None, None, None, None, None
        return None, None, None, None, None


# NEW CALLBACK – top level (not inside register_filter_callbacks)
    @app.callback(
        Output("trend-summary", "children"),
        [Input("source-filter", "value"),
         Input("severity-filter", "value"),
         Input("status-filter", "value"),
         Input("team-filter", "value"),
         Input("repo-filter", "value"),
         Input("refresh-interval", "n_intervals")]
    )
    def update_trend_summary(source_val, severity_val, status_val, team_val, repo_val, n):
        """Show week-over-week trend in total findings."""
        try:
            df = load_security_data()
            filtered = get_filtered_data(df, source_val, severity_val,
                                         status_val, team_val, repo_val)

            week = calculate_trend_comparison(filtered, "W")
            arrow = "↑" if week["delta"] > 0 else "↓" if week["delta"] < 0 else "→"
            return (
                f"Week-over-week: {arrow} {abs(week['delta_pct']):.1f}% "
                f"({week['current']} vs {week['previous']})"
            )
        except Exception as e:
            logger.error(f"Error updating trend summary: {e}")
            return "Week-over-week: n/a"
