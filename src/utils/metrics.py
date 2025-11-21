"""
KPI and metrics calculation functions
"""
import pandas as pd
import numpy as np
import math
from datetime import datetime

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate key performance indicators from security findings.
    
    Args:
        df: Security findings DataFrame
        
    Returns:
        dict: Dictionary containing KPI values
    """
    if df is None or df.empty:
        return {
            "total": 0,
            "open": 0,
            "critical_open": 0,
            "avg_mttr": 0
        }
    
    total = len(df)
    open_findings = len(df[df["Status"].isin(["Open", "In Progress"])])
    critical_open = len(df[(df["Status"].isin(["Open", "In Progress"])) & 
                           (df["Severity"] == "Critical")])
    avg_mttr = df["MTTR_Hours"].mean() if "MTTR_Hours" in df.columns else 0
    
    return {
        "total": total,
        "open": open_findings,
        "critical_open": critical_open,
        "avg_mttr": avg_mttr
    }


def calculate_risk_score(df: pd.DataFrame) -> float:
    """
    Calculate overall risk score (0–100) based on open findings by severity.
    Weights: Critical=5, High=3, Medium=2, Low=1.
    
    Args:
        df: Security findings DataFrame
        
    Returns:
        float: Risk score between 0-100
    """
    if df is None or df.empty:
        return 0.0

    weights = {"Critical": 5, "High": 3, "Medium": 2, "Low": 1}
    open_df = df[df["Status"].isin(["Open", "In Progress"])]
    
    if open_df.empty:
        return 0.0

    score_raw = sum(
        len(open_df[open_df["Severity"] == sev]) * w
        for sev, w in weights.items()
    )
    
    # Compress to 0–100 using exponential scaling
    score = 100 * (1 - math.exp(-score_raw / 50))
    return round(score, 1)


def calculate_trend_comparison(df: pd.DataFrame, window: str = "W") -> dict:
    """
    Compare current vs previous period (week or month) by total findings.
    
    Args:
        df: Security findings DataFrame
        window: "W" for week-over-week, "M" for month-over-month
        
    Returns:
        dict: Dictionary with current, previous, delta, and delta_pct
    """
    if df is None or df.empty:
        return {"current": 0, "previous": 0, "delta": 0, "delta_pct": 0}

    try:
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
    except Exception as e:
        return {"current": 0, "previous": 0, "delta": 0, "delta_pct": 0}


def calculate_sla_compliance(df: pd.DataFrame, sla_hours: dict = None) -> dict:
    """
    Calculate SLA compliance rates by severity.
    
    Args:
        df: Security findings DataFrame
        sla_hours: Dictionary mapping severity to SLA hours
        
    Returns:
        dict: Compliance rates by severity
    """
    if sla_hours is None:
        sla_hours = {"Critical": 24, "High": 72, "Medium": 168, "Low": 720}
    
    if df is None or df.empty:
        return {}
    
    compliance = {}
    for severity, hours in sla_hours.items():
        sev_df = df[df["Severity"] == severity]
        if len(sev_df) > 0:
            compliant = len(sev_df[sev_df["MTTR_Hours"] <= hours])
            compliance[severity] = round((compliant / len(sev_df)) * 100, 1)
        else:
            compliance[severity] = 0.0
    
    return compliance
