#!/usr/bin/env python3
"""
Load and clean Sponsored Proposals data from DataInsights Excel exports.

Handles merged cells in Proposal ID column and date parsing.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Union


def load_proposal_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load Sponsored Proposals data with proper handling of merged cells.
    
    Args:
        file_path: Path to the Excel file (e.g., '20251209_Proposal_Details.xlsx')
    
    Returns:
        pd.DataFrame with cleaned data
        
    Notes:
        - Proposal ID, Proposal Title, and Proposal Status have merged cells (forward-filled)
        - Primary Project ID (Column 3, new as of Dec 2025) is CON-level only (not submission-level)
        - Submitted Date (Column 5, new as of Dec 2025) shows when each request was submitted
        - Multi-row CONs = multiple funding requests over time (NOT budget splits)
        - Each row is an independent submission that may or may not have been funded
        - For funded awards: Use Award Details for authoritative data (PI, dates, amounts)
        - Proposal Details for funded: Only use Submitted Date and Proposed Amount
    """
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    # Forward-fill merged cells in Proposal ID, Title, and Status columns
    df['Proposal ID'] = df['Proposal ID'].ffill()
    df['Proposal Title'] = df['Proposal Title'].ffill()
    df['Proposal Status'] = df['Proposal Status'].ffill()
    
    # Do NOT forward-fill Primary Project ID (CON-level, only on first row)
    # Do NOT forward-fill Submitted Date (each row has own submission date)
    
    # Parse date columns (try multiple formats for backward compatibility)
    # New format (Dec 2025+): "M/D/YYYY"
    # Old format (before Dec 2025): "M/D/YYYY 12:00:00 AM"
    date_columns = ['Submitted Date', 'Award Project Start Date', 'Award Project End Date']
    for col in date_columns:
        if col in df.columns:
            # Try new format first
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
            # If all failed, try old format
            if df[col].isna().all():
                df[col] = pd.to_datetime(df[col], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    
    # Clean up whitespace
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    return df


def get_data_date(file_path: Union[str, Path]) -> Optional[str]:
    """
    Extract the data date from filename (YYYYMMDD format).
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Date string in YYYY-MM-DD format, or None if not in expected format
        
    Example:
        >>> get_data_date('20251123_Proposal_Details.xlsx')
        '2025-11-23'
    """
    filename = Path(file_path).name
    
    # Try to extract YYYYMMDD from filename
    if filename.startswith('202') and len(filename) >= 8:
        date_str = filename[:8]
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass
    
    return None


def validate_proposal_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate that loaded data has expected structure.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Expected columns
    required_columns = [
        'Proposal ID', 'Proposal Title', 'Proposal Status',
        'Award Project Start Date', 'Award Project End Date',
        'PI Administrative Unit', 'PI Deptid', 'PI Name',
        'Primary Sponsor', 'Proposed Amount'
    ]
    
    # Check for required columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        issues.append(f"Missing required columns: {', '.join(missing)}")
    
    # Check that Proposal ID was forward-filled (no NaN after row 0)
    if 'Proposal ID' in df.columns:
        null_count = df['Proposal ID'].isna().sum()
        if null_count > 0:
            issues.append(f"Proposal ID has {null_count} null values - forward-fill may have failed")
    
    # Check date columns are datetime
    if 'Award Project Start Date' in df.columns:
        if df['Award Project Start Date'].dtype != 'datetime64[ns]':
            issues.append("Award Project Start Date should be datetime type")
    
    # Check for reasonable data ranges
    if 'Proposed Amount' in df.columns:
        if df['Proposed Amount'].min() < 0:
            issues.append("Proposed Amount has negative values")
    
    is_valid = len(issues) == 0
    return is_valid, issues


if __name__ == '__main__':
    # Test loading
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python load_proposal_data.py <path_to_excel_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"Loading data from: {file_path}")
    df = load_proposal_data(file_path)
    
    print(f"\nData date: {get_data_date(file_path)}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    print("\nValidating data...")
    is_valid, issues = validate_proposal_data(df)
    
    if is_valid:
        print("[OK] Data structure is valid")
    else:
        print("[NO] Data validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    print("\nFirst few rows:")
    print(df.head(3))
    
    print("\nProposal ID value counts (first 10):")
    print(df['Proposal ID'].value_counts().head(10))
