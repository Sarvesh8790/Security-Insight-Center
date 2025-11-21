"""
Table components
"""
from dash import dash_table
from config.theme import CYBER_THEME

def create_findings_table(df):
    """Create interactive findings data table"""
    
    display_columns = [
        "Source", "Category", "Severity", "Status", 
        "Assigned_Team", "Repo/Account", "Opened_At", "MTTR_Hours"
    ]
    
    return dash_table.DataTable(
        id="findings-table",
        columns=[{"name": col, "id": col} for col in display_columns],
        data=df[display_columns].to_dict("records"),
        page_size=20,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "backgroundColor": CYBER_THEME["bg_card"],
            "color": CYBER_THEME["text_primary"],
            "border": f"1px solid {CYBER_THEME['border_glow']}",
            "textAlign": "left",
            "padding": "10px"
        },
        style_header={
            "backgroundColor": CYBER_THEME["bg_main"],
            "fontWeight": "bold",
            "border": f"1px solid {CYBER_THEME['border_glow']}"
        },
        style_data_conditional=[
            {
                "if": {"filter_query": "{Severity} = Critical"},
                "backgroundColor": "rgba(239, 68, 68, 0.1)",
            },
            {
                "if": {"filter_query": "{Severity} = High"},
                "backgroundColor": "rgba(245, 158, 11, 0.1)",
            }
        ]
    )
 