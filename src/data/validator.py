"""
Data validation and quality checks
"""
import pandas as pd
from src.utils.logger import logger

def validate_data_quality(df: pd.DataFrame) -> list:
    """
    Check data integrity and quality

    Args:
        df: DataFrame to validate

    Returns:
        list: List of validation issues found
    """
    issues = []

    # Check for required columns
    required_cols = [
        "Source", "Category", "Severity", "Status", 
        "Assigned_Team", "Repo/Account", "Opened_At", "MTTR_Hours"
    ]
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")

    # Check for null values in critical fields
    critical_fields = ["Source", "Severity", "Status", "Opened_At"]
    for field in critical_fields:
        if field in df.columns:
            null_count = df[field].isnull().sum()
            if null_count > 0:
                issues.append(f"Found {null_count} null values in '{field}'")

    # Validate severity values
    valid_severities = ["Critical", "High", "Medium", "Low"]
    if "Severity" in df.columns:
        invalid_sev = df[~df["Severity"].isin(valid_severities)]["Severity"].unique()
        if len(invalid_sev) > 0:
            issues.append(f"Invalid severity values: {invalid_sev.tolist()}")

    # Validate MTTR values
    if "MTTR_Hours" in df.columns:
        negative_mttr = df[df["MTTR_Hours"] < 0]
        if len(negative_mttr) > 0:
            issues.append(f"Found {len(negative_mttr)} negative MTTR values")

    # Log results
    if issues:
        for issue in issues:
            logger.warning(f"Data quality issue: {issue}")
    else:
        logger.info("Data quality validation passed")

    return issues
