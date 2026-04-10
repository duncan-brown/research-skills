#!/usr/bin/env python3
"""
Load and clean Award Details data from DataInsights Excel exports.

Handles merged cells in Contract Num and Award Title columns.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Union


def load_award_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load Award Details data with proper handling of merged cells.
    
    Args:
        file_path: Path to the Excel file (e.g., '20251208_Award_Details.xlsx')
    
    Returns:
        pd.DataFrame with cleaned data
        
    Notes:
        - Contract Num and Award Title columns have merged cells that are forward-filled
        - Award Label is NOT forward-filled (blank is meaningful for 2nd+ supplements)
        - Dates are parsed from string format to datetime
        - Project ID is string with semicolon-separated values for multiple projects
        - One CON can have multiple rows (base + supplements)
    """
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    # Forward-fill merged cells in Contract Num and Award Title
    # These are merged for base award + all supplements
    df['Contract Num'] = df['Contract Num'].ffill()
    df['Award Title'] = df['Award Title'].ffill()
    
    # Do NOT forward-fill Award Label - blank is meaningful (2nd+ supplements)
    
    # Parse date columns from string format "M/D/YYYY" to datetime
    date_columns = ['Date', 'Award Project Start Date', 'Award Project End Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
    
    # Clean up any whitespace in string columns
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    return df


def get_award_data_date(file_path: Union[str, Path]) -> Optional[str]:
    """
    Extract the data date from filename (YYYYMMDD format).
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Date string in YYYY-MM-DD format, or None if not in expected format
        
    Example:
        >>> get_award_data_date('20251208_Award_Details.xlsx')
        '2025-12-08'
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


def check_data_date_match(award_file: Union[str, Path], 
                          proposal_file: Union[str, Path]) -> tuple[bool, str, str]:
    """
    Check if award and proposal data files have matching dates.
    
    Args:
        award_file: Path to Award Details file
        proposal_file: Path to Proposal Details file
    
    Returns:
        Tuple of (dates_match, award_date, proposal_date)
    """
    award_date = get_award_data_date(award_file)
    proposal_date = get_award_data_date(proposal_file)
    
    if award_date is None or proposal_date is None:
        return False, award_date or "unknown", proposal_date or "unknown"
    
    return award_date == proposal_date, award_date, proposal_date


def warn_if_dates_mismatch(award_file: Union[str, Path],
                          proposal_file: Union[str, Path]) -> bool:
    """
    Warn user if data file dates don't match and get confirmation.
    
    Args:
        award_file: Path to Award Details file
        proposal_file: Path to Proposal Details file
    
    Returns:
        True if user confirms to proceed, False otherwise
        
    Note:
        This function is designed to be called interactively and will
        print warnings. For automated use, call check_data_date_match() directly.
    """
    dates_match, award_date, proposal_date = check_data_date_match(award_file, proposal_file)
    
    if not dates_match:
        print("[!]  WARNING: Data file dates do not match!")
        print(f"   Award Details date:    {award_date}")
        print(f"   Proposal Details date: {proposal_date}")
        print()
        print("For accurate analysis, you should use data files from the same date.")
        print()
        print("Download updated files from:")
        print("  * Proposals: https://datainsights.syr.edu/#/site/data/views/SponsoredProposalsatSyracuseUniversity/Details")
        print("  * Awards: https://datainsights.syr.edu/#/site/data/views/OfficeofResearchAnticipatedandSupplementAmounts/Details")
        print()
        print("If you have new files, upload them to this Claude project and this chat.")
        print()
        response = input("Do you want to continue with mismatched files? (yes/no): ")
        return response.lower() in ['yes', 'y']
    
    return True


def validate_award_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
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
        'Contract Num', 'Award Title', 'Award Label',
        'Date', 'Award Status',
        'Award Project Start Date', 'Award Project End Date',
        'Project ID', 'PI Administrative Unit', 'PI Deptid', 'PI Name',
        'Primary Sponsor', 'Anticipated & Supplement Award Amount'
    ]
    
    # Check for required columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        issues.append(f"Missing required columns: {', '.join(missing)}")
    
    # Check that Contract Num was forward-filled (no NaN after row 0)
    if 'Contract Num' in df.columns:
        null_count = df['Contract Num'].isna().sum()
        if null_count > 0:
            issues.append(f"Contract Num has {null_count} null values - forward-fill may have failed")
    
    # Check date columns are datetime
    if 'Date' in df.columns:
        if df['Date'].dtype != 'datetime64[ns]':
            issues.append("Date should be datetime type")
    
    # Check Award Label values
    if 'Award Label' in df.columns:
        valid_labels = {'Anticipated Amount', 'Supplement Amount', None, pd.NA}
        invalid = set(df['Award Label'].unique()) - valid_labels
        invalid = [x for x in invalid if pd.notna(x)]
        if invalid:
            issues.append(f"Invalid Award Label values: {invalid}")
    
    # Check Award Status values
    if 'Award Status' in df.columns:
        valid_status = {'Active', 'Completed'}
        invalid = set(df['Award Status'].unique()) - valid_status
        if invalid:
            issues.append(f"Invalid Award Status values: {invalid}")
    
    is_valid = len(issues) == 0
    return is_valid, issues


if __name__ == '__main__':
    # Test loading
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python load_award_data.py <path_to_excel_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"Loading award data from: {file_path}")
    df = load_award_data(file_path)
    
    print(f"\nData date: {get_award_data_date(file_path)}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Unique CONs: {df['Contract Num'].nunique()}")
    
    print("\nValidating data...")
    is_valid, issues = validate_award_data(df)
    
    if is_valid:
        print("[OK] Data structure is valid")
    else:
        print("[NO] Data validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    print("\nFirst few rows:")
    print(df.head(3))
    
    print("\nAward Label distribution:")
    print(df['Award Label'].value_counts(dropna=False))
    
    print("\nAward Status distribution:")
    print(df['Award Status'].value_counts())
