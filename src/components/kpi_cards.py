"""
KPI Card UI components
"""
from dash import html

def create_kpi_card(title: str, value: str, trend: str = None, card_id: str = None) -> html.Div:
    """
    Create a KPI card component

    Args:
        title: Card title
        value: Main KPI value to display
        trend: Optional trend indicator
        card_id: Optional HTML id for the card

    Returns:
        html.Div: KPI card component
    """
    children = [
        html.Div(title, className="kpi-title"),
        html.Div(value, className="kpi-value", id=card_id)
    ]

    if trend:
        children.append(html.Div(trend, className="kpi-trend"))

    return html.Div(children, className="kpi-card")

def create_kpi_row(kpis: list) -> html.Div:
    """
    Create a row of KPI cards

    Args:
        kpis: List of KPI card components

    Returns:
        html.Div: Row container with KPI cards
    """
    return html.Div(
        kpis,
        className="kpi-row",
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"}
    )
