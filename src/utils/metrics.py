"""
KPI and metrics calculation functions
"""
import pandas as pd
import numpy as np
import math
from src.utils.helpers import safe_divide

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate key performance indicators

    Args:
        df: Filtered security findings DataFrame

    Returns:
        dict: Dictionary of KPI values
    """
    total_findings = len(df)
    open_findings = len(df[df["Status"] == "Open"])
    critical_open = len(df[(df["Severity"] == "Critical") & (df["Status"] == "Open")])

    closed_df = df[df["Status"] == "Closed"]
    avg_mttr = closed_df["MTTR_Hours"].mean() if len(closed_df) > 0 else 0

    return {
        "total": total_findings,
        "open": open_findings,
        "critical_open": critical_open,
        "avg_mttr": avg_mttr if not np.isnan(avg_mttr) else 0
    }

def calculate_sla_compliance(df: pd.DataFrame, sla_hours: int = 72) -> float:
    """
    Calculate SLA compliance percentage

    Args:
        df: Security findings DataFrame
        sla_hours: SLA threshold in hours

    Returns:
        float: Compliance percentage
    """
    closed = df[df["Status"] == "Closed"]
    if len(closed) == 0:
        return 0.0

    compliant = (closed["MTTR_Hours"] <= sla_hours).sum()
    return safe_divide(compliant, len(closed), 0) * 100

def calculate_trend(df: pd.DataFrame, metric_column: str = "Status") -> dict:
    """
    Calculate week-over-week trend

    Args:
        df: Security findings DataFrame
        metric_column: Column to analyze for trends

    Returns:
        dict: Trend information
    """
    if "Week_Number" not in df.columns or len(df) == 0:
        return {"change": 0, "direction": "→", "text": "No data"}

    current_week = df["Week_Number"].max()
    previous_week = current_week - 1

    current_count = len(df[df["Week_Number"] == current_week])
    previous_count = len(df[df["Week_Number"] == previous_week])

    if previous_count == 0:
        return {"change": 0, "direction": "→", "text": "New"}

    change_pct = ((current_count - previous_count) / previous_count) * 100
    direction = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "→"

    return {
        "change": abs(change_pct),
        "direction": direction,
        "text": f"{direction} {abs(change_pct):.1f}%"
    }

def get_top_repositories(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Get top N repositories by finding count

    Args:
        df: Security findings DataFrame
        n: Number of top repositories to return

    Returns:
        pd.DataFrame: Top repositories with counts
    """
    return df["Repo/Account"].value_counts().head(n).reset_index()

def get_team_workload(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate workload distribution by team

    Args:
        df: Security findings DataFrame

    Returns:
        pd.DataFrame: Team workload statistics
    """
    return df.groupby(["Assigned_Team", "Status"]).size().reset_index(name="Count")
def calculate_trend_comparison(df: pd.DataFrame, window: str = "W") -> dict:
    """
    Compare current vs previous period (week or month) by total findings.

    Args:
        df: Security findings DataFrame
        window: "W" for week-over-week, "M" for month-over-month

    Returns:
        dict with keys: current, previous, delta, delta_pct
    """
    if df is None or df.empty:
        return {"current": 0, "previous": 0, "delta": 0, "delta_pct": 0}

    if window == "M":
        bucket = df["Opened_At"].dt.to_period("M")
    else:
        bucket = df["Opened_At"].dt.to_period("W")

    counts = df.groupby(bucket).size().sort_index()

    if len(counts) == 0:
        return {"current": 0, "previous": 0, "delta": 0, "delta_pct": 0}
    if len(counts) == 1:
        cur = int(counts.iloc[-1])
        return {"current": cur, "previous": 0, "delta": cur, "delta_pct": 100}

    cur = int(counts.iloc[-1])
    prev = int(counts.iloc[-2])
    delta = cur - prev
    delta_pct = 0 if prev == 0 else (delta / prev) * 100

    return {
        "current": cur,
        "previous": prev,
        "delta": delta,
        "delta_pct": round(delta_pct, 1),
    }
def calculate_risk_score(df):
    """
    Overall risk score (0–100) based on open findings by severity.
    Weights: Critical=5, High=3, Medium=2, Low=1.
    """
    if df is None or df.empty:
        return 0

    weights = {"Critical": 5, "High": 3, "Medium": 2, "Low": 1}
    open_df = df[df["Status"].isin(["Open", "In Progress"])]
    if open_df.empty:
        return 0

    score_raw = sum(
        open_df[open_df["Severity"] == sev].shape[0] * w
        for sev, w in weights.items()
    )
    score = 100 * (1 - math.exp(-score_raw / 50))
    return round(score, 1)
