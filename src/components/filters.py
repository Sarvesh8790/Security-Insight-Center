"""
Filter UI components
"""
from dash import dcc, html

def create_dropdown_filter(filter_id: str, label: str, options: list, 
                          multi: bool = True, placeholder: str = None) -> html.Div:
    """
    Create a dropdown filter component

    Args:
        filter_id: HTML id for the dropdown
        label: Label text
        options: List of option values
        multi: Whether to allow multiple selections
        placeholder: Placeholder text

    Returns:
        html.Div: Filter component
    """
    return html.Div([
        html.Label(label, style={"display": "block", "marginBottom": "4px"}),
        dcc.Dropdown(
            id=filter_id,
            options=[{"label": opt, "value": opt} for opt in options],
            multi=multi,
            placeholder=placeholder or f"Select {label}...",
            className="filter-dropdown"
        )
    ], className="filter-container", style={"marginBottom": "16px"})

def create_filter_section(filter_options: dict) -> html.Div:
    """
    Create the complete filter section with all dropdowns

    Args:
        filter_options: Dictionary of filter options from get_filter_options

    Returns:
        html.Div: Complete filter section
    """
    return html.Div([
        html.H3("🔍 Filters", style={"marginBottom": "16px"}),

        create_dropdown_filter(
            "source-filter",
            "Source",
            filter_options["sources"],
            placeholder="All Sources"
        ),

        create_dropdown_filter(
            "severity-filter",
            "Severity",
            filter_options["severities"],
            placeholder="All Severities"
        ),

        create_dropdown_filter(
            "status-filter",
            "Status",
            filter_options["statuses"],
            placeholder="All Statuses"
        ),

        create_dropdown_filter(
            "team-filter",
            "Team",
            filter_options["teams"],
            placeholder="All Teams"
        ),

        create_dropdown_filter(
            "repo-filter",
            "Repository",
            filter_options["repos"],
            placeholder="All Repositories"
        ),

        html.Button(
            "Reset Filters",
            id="reset-filters-btn",
            n_clicks=0,
            style={
                "marginTop": "16px",
                "padding": "8px 16px",
                "backgroundColor": "#5E5CE6",
                "color": "white",
                "border": "none",
                "borderRadius": "4px",
                "cursor": "pointer"
            }
        )
    ], className="filter-section")
