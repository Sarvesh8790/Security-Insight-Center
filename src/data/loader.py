"""
Data loading and caching functionality
"""
import pandas as pd
from functools import lru_cache
from config.settings import DATA_PATH
from src.utils.logger import logger

@lru_cache(maxsize=1)
def load_security_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    """
    Load and preprocess security findings data with caching

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Processed security findings
    """
    try:
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath, parse_dates=["Opened_At"])
        # Basic preprocessing
        df["Week_Number"] = df["Opened_At"].dt.isocalendar().week.astype(int)
        df["View_Link"] = df["tool_url"].apply(
            lambda u: f"[View 🔗]({u})" if isinstance(u, str) and u else ""
        )

        logger.info(f"Successfully loaded {len(df)} findings from {df['Source'].nunique()} sources")
        return df

    except FileNotFoundError:
        logger.error(f"Data file not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def get_filtered_data(df: pd.DataFrame, source=None, severity=None, 
                      status=None, team=None, repo=None) -> pd.DataFrame:
    """
    Apply filters to the dataset

    Args:
        df: Source DataFrame
        source: List of sources to filter by
        severity: List of severity levels to filter by
        status: List of status values to filter by
        team: List of teams to filter by
        repo: List of repositories to filter by

    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered = df.copy()

    if source and len(source) > 0:
        filtered = filtered[filtered["Source"].isin(source)]
    if severity and len(severity) > 0:
        filtered = filtered[filtered["Severity"].isin(severity)]
    if status and len(status) > 0:
        filtered = filtered[filtered["Status"].isin(status)]
    if team and len(team) > 0:
        filtered = filtered[filtered["Assigned_Team"].isin(team)]
    if repo and len(repo) > 0:
        filtered = filtered[filtered["Repo/Account"].isin(repo)]

    logger.debug(f"Filtered data: {len(filtered)} of {len(df)} findings")
    return filtered

def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Get unique values for all filter dropdowns

    Args:
        df: Source DataFrame

    Returns:
        dict: Dictionary with filter options
    """
    return {
        "sources": sorted(df["Source"].unique().tolist()),
        "severities": ["Critical", "High", "Medium", "Low"],
        "statuses": sorted(df["Status"].unique().tolist()),
        "teams": sorted(df["Assigned_Team"].unique().tolist()),
        "repos": sorted(df["Repo/Account"].unique().tolist()),
    }
