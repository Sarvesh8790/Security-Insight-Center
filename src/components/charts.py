"""
Chart components with click-to-drill functionality
"""
import plotly.express as px
import plotly.graph_objects as go
from config.theme import CYBER_THEME, SEVERITY_COLORS
import plotly.express as px
from config.theme import CYBER_THEME, SEVERITY_COLORS
from src.utils.metrics import calculate_risk_score

def create_severity_pie_chart(df):
    """Severity distribution pie chart"""
    severity_counts = df["Severity"].value_counts()
    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title="🎯 Findings by Severity",
        color=severity_counts.index,
        color_discrete_map=SEVERITY_COLORS,
        hole=0.4
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        showlegend=True,
        legend=dict(
            orientation="v",  # Vertical orientation
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        margin=dict(t=50, b=20, l=20, r=20),
        height=350
    )
    return fig
def create_attack_timeline_heatmap(df, time_granularity="W", by="Repo/Account"):
    """
    Attack timeline heatmap: vulnerability density over time

    Args:
        df: filtered DataFrame
        time_granularity: "D" (day), "W" (week), "M" (month)
        by: dimension on y-axis, e.g. "Repo/Account" or "Source"
    """
    if df.empty:
        fig = px.imshow([[0]], labels=dict(x="Time", y=by, color="Findings"))
        fig.update_layout(
            title="Attack Timeline Heatmap (no data)",
            paper_bgcolor=CYBER_THEME["bg_card"],
            plot_bgcolor=CYBER_THEME["bg_card"],
            font_color=CYBER_THEME["text_primary"],
        )
        return fig

    # Bucket time
    if time_granularity == "D":
        df["_bucket"] = df["Opened_At"].dt.date
    elif time_granularity == "M":
        df["_bucket"] = df["Opened_At"].dt.to_period("M").astype(str)
    else:  # week
        df["_bucket"] = df["Opened_At"].dt.to_period("W").apply(lambda p: p.start_time.date())

    pivot = (
        df.groupby([by, "_bucket"])
          .size()
          .reset_index(name="Count")
          .pivot(index=by, columns="_bucket", values="Count")
          .fillna(0)
    )

    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale="Viridis",
        aspect="auto",
        labels=dict(x="Time", y=by, color="Findings"),
        title="🔥 Attack Timeline Heatmap",
    )

    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=60, l=80, r=20),
        height=400,
    )
    return fig

def create_trend_line_chart(df):
    """Timeline trend chart"""
    timeline_data = df.groupby(df["Opened_At"].dt.date).size().reset_index(name="Count")
    timeline_data.columns = ["Date", "Count"]

    fig = px.line(
        timeline_data,
        x="Date",
        y="Count",
        title="📈 Findings Trend Over Time",
        markers=True
    )
    fig.update_traces(
        line_color=CYBER_THEME["accent"],
        marker=dict(size=8, color=CYBER_THEME["accent"])
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        xaxis_title="Date",
        yaxis_title="Number of Findings",
        hovermode='x unified',
        margin=dict(t=50, b=50, l=50, r=20),
        height=350
    )
    return fig

def create_severity_by_week_chart(df):
    """Stacked bar chart - Severity by Week"""
    weekly = df.groupby(["Week_Number", "Severity"]).size().reset_index(name="Count")
    
    fig = px.bar(
        weekly,
        x="Week_Number",
        y="Count",
        color="Severity",
        title="📊 Severity Distribution by Week",
        color_discrete_map=SEVERITY_COLORS,
        barmode='stack'
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        xaxis_title="Week Number",
        yaxis_title="Count",
        legend_title="Severity",
        margin=dict(t=50, b=50, l=50, r=20),
        height=400  # ← Increase from 350 to 400 for full-width chart
    )
    return fig

def create_source_bar_chart(df):
    """Source distribution bar chart"""
    source_counts = df["Source"].value_counts()

    fig = px.bar(
        x=source_counts.index,
        y=source_counts.values,
        title="🔍 Findings by Source",
        labels={"x": "Source", "y": "Count"}
    )
    fig.update_traces(
        marker_color=CYBER_THEME["accent"],
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=50, l=50, r=20),
        height=350
    )
    return fig

def create_category_treemap(df):
    """Category treemap visualization"""
    cat_counts = df.groupby(["Category", "Severity"]).size().reset_index(name="Count")

    fig = px.treemap(
        cat_counts,
        path=["Category", "Severity"],
        values="Count",
        title="🗂️ Findings by Category",
        color="Severity",
        color_discrete_map=SEVERITY_COLORS
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=20, l=20, r=20),
        height=350
    )
    return fig

def create_top_repos_chart(df, top_n=10):
    """Top repositories horizontal bar chart"""
    top_repos = df["Repo/Account"].value_counts().head(top_n)

    fig = px.bar(
        x=top_repos.values,
        y=top_repos.index,
        orientation='h',
        title=f"🏆 Top {top_n} Repositories",
        labels={"x": "Count", "y": "Repository"}
    )
    fig.update_traces(
        marker_color=CYBER_THEME["accent_soft"],
        hovertemplate='<b>%{y}</b><br>Findings: %{x}<extra></extra>'
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=50, l=150, r=20),
        height=400,
        yaxis={'categoryorder':'total ascending'}
    )
    return fig

def create_custom_chart(df, x_col, y_col, chart_type, color_col=None):
    """Create custom chart based on user selection"""
    if chart_type == "bar":
        if y_col == "count":
            data = df[x_col].value_counts().reset_index()
            data.columns = [x_col, "Count"]
            fig = px.bar(data, x=x_col, y="Count", color=color_col if color_col and color_col != "None" else None)
        else:
            fig = px.bar(df, x=x_col, y=y_col, color=color_col if color_col and color_col != "None" else None)

    elif chart_type == "line":
        if y_col == "count":
            data = df.groupby(x_col).size().reset_index(name="Count")
            fig = px.line(data, x=x_col, y="Count", markers=True)
        else:
            fig = px.line(df, x=x_col, y=y_col, markers=True)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col if color_col and color_col != "None" else None)

    elif chart_type == "box":
        fig = px.box(df, x=x_col, y=y_col, color=color_col if color_col and color_col != "None" else None)

    else:  # pie
        data = df[x_col].value_counts()
        fig = px.pie(values=data.values, names=data.index)

    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=50, l=50, r=20),
        height=400
    )
    return fig
def create_risk_gauge(df):
    """Overall security posture gauge (0–100)."""
    score = calculate_risk_score(df)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": CYBER_THEME["accent"]},
                "steps": [
                    {"range": [0, 40], "color": "#065f46"},   # green
                    {"range": [40, 70], "color": "#92400e"},  # amber
                    {"range": [70, 100], "color": "#7f1d1d"}, # red
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        height=260,
        margin=dict(t=40, b=20, l=20, r=20),
    )
    return fig
def create_attack_timeline_heatmap(df, time_granularity="W", by="Repo/Account"):
    """
    Attack timeline heatmap: vulnerability density over time.

    time_granularity: "D" (day), "W" (week), "M" (month)
    by: y-axis dimension, e.g. "Repo/Account" or "Source"
    """
    if df.empty:
        fig = px.imshow([[0]], labels=dict(x="Time", y=by, color="Findings"))
        fig.update_layout(
            title="Attack Timeline Heatmap (no data)",
            paper_bgcolor=CYBER_THEME["bg_card"],
            plot_bgcolor=CYBER_THEME["bg_card"],
            font_color=CYBER_THEME["text_primary"],
        )
        return fig

    # Bucket time
    if time_granularity == "D":
        df["_bucket"] = df["Opened_At"].dt.date
    elif time_granularity == "M":
        df["_bucket"] = df["Opened_At"].dt.to_period("M").astype(str)
    else:  # week
        df["_bucket"] = df["Opened_At"].dt.to_period("W").apply(
            lambda p: p.start_time.date()
        )

    pivot = (
        df.groupby([by, "_bucket"])
          .size()
          .reset_index(name="Count")
          .pivot(index=by, columns="_bucket", values="Count")
          .fillna(0)
    )

    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale="Viridis",
        aspect="auto",
        labels=dict(x="Time", y=by, color="Findings"),
        title="🔥 Attack Timeline Heatmap",
    )

    fig.update_layout(
        paper_bgcolor=CYBER_THEME["bg_card"],
        plot_bgcolor=CYBER_THEME["bg_card"],
        font_color=CYBER_THEME["text_primary"],
        margin=dict(t=50, b=60, l=80, r=20),
        height=400,
    )
    return fig
