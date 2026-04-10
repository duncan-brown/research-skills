#!/usr/bin/env python3
"""
Data loading utilities for Syracuse University Detailed Sponsored Expenditures
Handles Tableau exports with merged cells that require forward-filling
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from typing import Optional, Union


def load_expenditure_data(filepath: Union[str, Path], 
                          verbose: bool = False) -> pd.DataFrame:
    """
    Load expenditure data from Excel export with automatic forward-fill for merged cells.
    
    IMPORTANT: Forward-fill is done WITHIN each contract to prevent data bleeding
    between different CON IDs.
    
    Args:
        filepath: Path to Excel file (typically YYYYMMDD_Expenditure_Details_FYXX.xlsx)
        verbose: Print loading progress and statistics
    
    Returns:
        DataFrame with forward-filled columns and cleaned data
    """
    if verbose:
        print(f"Loading expenditure data from: {filepath}")
    
    # Read Excel file
    df = pd.read_excel(filepath)
    
    if verbose:
        print(f"  Initial shape: {df.shape}")
    
    # First, forward-fill Contract Num to identify contract groups
    df['Contract Num'] = df['Contract Num'].ffill()
    
    # Remove rows where Contract Num is still null (header rows or errors)
    initial_len = len(df)
    df = df[df['Contract Num'].notna()].copy()
    if verbose and len(df) < initial_len:
        print(f"  Removed {initial_len - len(df)} rows with null Contract Num")
    
    # Columns that need forward-fill WITHIN each contract
    # These are contract-level fields that should not bleed between contracts
    contract_level_columns = [
        'Award Title',
        'PI Name',
        'PI Department (if any)',
        'PI Administrative Unit',
        'Award Status',
        'Project Type',
        'Syr Pt Descr',
        'SYR Proj Area',
        'Syr Proj Deptid Descr',
        'Syr Proj Deptid',
        'Federal Department',
        'Federal Subtier',
        'Federal Office',
        'Primary Sponsor',
        'Primary Sponsor Type'
    ]
    
    # Columns that can be forward-filled across contracts
    # These are typically expense classification fields
    global_ff_columns = [
        'Expense Category',
        'Expense SubCategory',
        'Expenditure Fiscal Year'
    ]
    
    # Forward-fill within each contract group
    if verbose:
        print(f"  Forward-filling {len(contract_level_columns)} columns within contracts...")
    
    for col in contract_level_columns:
        if col in df.columns:
            df[col] = df.groupby('Contract Num')[col].ffill()
    
    # Forward-fill global columns (these can span contracts)
    for col in global_ff_columns:
        if col in df.columns:
            df[col] = df[col].ffill()
    
    # Clean up Federal columns for non-federal sponsors
    # Set Federal columns to null when Primary Sponsor Type is not Federal
    if 'Primary Sponsor Type' in df.columns:
        non_federal_mask = df['Primary Sponsor Type'] != 'Federal Agencies'
        federal_cols = ['Federal Department', 'Federal Subtier', 'Federal Office']
        for col in federal_cols:
            if col in df.columns:
                df.loc[non_federal_mask, col] = None
        
        if verbose:
            cleaned_count = non_federal_mask.sum()
            print(f"  Cleaned federal data from {cleaned_count} non-federal rows")
    
    if verbose:
        null_count = df.isnull().sum().sum()
        print(f"  Remaining nulls after forward-fill: {null_count}")
    
    # Ensure numeric columns are properly typed
    numeric_cols = ['Syr Proj Deptid', 'Project Type', 'Expenditure Amount', 'Expenditure Fiscal Year']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add derived columns
    df = add_derived_columns(df)
    
    if verbose:
        print(f"  Final shape: {df.shape}")
        print(f"  Unique contracts: {df['Contract Num'].nunique()}")
        print(f"  Total expenditure: ${df['Expenditure Amount'].sum():,.2f}")
    
    return df


def get_fiscal_year(filepath: Union[str, Path]) -> Optional[int]:
    """
    Extract fiscal year from filename or data.
    
    Args:
        filepath: Path to Excel file
    
    Returns:
        Fiscal year as integer (e.g., 2025) or None if not found
    """
    # Try to extract from filename first
    filename = str(Path(filepath).name)
    fy_match = re.search(r'FY(\d{2,4})', filename)
    if fy_match:
        fy = fy_match.group(1)
        if len(fy) == 2:
            # Convert 2-digit year to 4-digit (assuming 20XX)
            return 2000 + int(fy)
        return int(fy)
    
    # If not in filename, check data
    try:
        df = pd.read_excel(filepath, nrows=100)
        if 'Expenditure Fiscal Year' in df.columns:
            df['Expenditure Fiscal Year'] = df['Expenditure Fiscal Year'].ffill()
            fy = df['Expenditure Fiscal Year'].dropna().iloc[0]
            return int(fy)
    except:
        pass
    
    return None


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add useful derived columns to the dataframe.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        DataFrame with additional columns
    """
    # Month number for sorting
    month_map = {
        'Jul': 1, 'Aug': 2, 'Sep': 3, 'Oct': 4, 'Nov': 5, 'Dec': 6,
        'Jan': 7, 'Feb': 8, 'Mar': 9, 'Apr': 10, 'May': 11, 'Jun': 12
    }
    df['Month_Num'] = df['Expenditure Month Abrevation'].map(month_map)
    
    # Academic vs Administrative flag
    df['Is_Academic'] = df['Syr Proj Deptid'].apply(
        lambda x: str(x).startswith(('21', '22', '23')) if pd.notna(x) else False
    )
    
    # Federal flag
    df['Is_Federal'] = df['Primary Sponsor Type'] == 'Federal Agencies'
    
    # Direct/Indirect simplified
    df['Cost_Type'] = df['Expense Category'].replace({
        'DIRECT COSTS': 'Direct',
        'INDIRECT COSTS': 'Indirect', 
        'UNDEFINED ACCOUNT': 'Undefined'
    })
    
    # Expense subcategory grouping
    df['Expense_Group'] = df['Expense SubCategory'].replace({
        'Salaries': 'Personnel',
        'Fringe Benefits': 'Personnel',
        'Tuition and Stipends': 'Student Support',
        'Travel': 'Operations',
        'Equipment': 'Operations',
        'Other Direct Costs': 'Operations',
        'Subcontracts': 'Subcontracts',
        'Indirect Costs': 'F&A',
        'Undefined Account': 'Other'
    })
    
    return df


def validate_expenditure_data(df: pd.DataFrame) -> dict:
    """
    Validate loaded expenditure data and return diagnostics.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'valid': True,
        'warnings': [],
        'errors': [],
        'statistics': {}
    }
    
    # Check required columns
    required_cols = ['Contract Num', 'Expenditure Amount', 'Expense Category']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        results['errors'].append(f"Missing required columns: {missing_cols}")
        results['valid'] = False
    
    # Check for remaining nulls in critical columns
    critical_cols = ['Contract Num', 'Expenditure Amount']
    for col in critical_cols:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                results['warnings'].append(f"{col} has {null_count} null values")
    
    # Statistics
    if 'Expenditure Amount' in df.columns:
        results['statistics']['total_amount'] = df['Expenditure Amount'].sum()
        results['statistics']['negative_count'] = (df['Expenditure Amount'] < 0).sum()
        results['statistics']['zero_count'] = (df['Expenditure Amount'] == 0).sum()
    
    if 'Contract Num' in df.columns:
        results['statistics']['unique_contracts'] = df['Contract Num'].nunique()
        results['statistics']['total_rows'] = len(df)
    
    # Check fiscal year consistency
    if 'Expenditure Fiscal Year' in df.columns:
        unique_fy = df['Expenditure Fiscal Year'].dropna().unique()
        if len(unique_fy) > 1:
            results['warnings'].append(f"Multiple fiscal years found: {unique_fy}")
    
    return results


def merge_with_proposal_data(expenditure_df: pd.DataFrame, 
                           proposal_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge expenditure data with proposal data on Contract Num.
    
    Args:
        expenditure_df: Expenditure dataframe
        proposal_df: Proposal dataframe (from sponsored-proposals skill)
    
    Returns:
        Merged dataframe
    """
    # Ensure proposal data has forward-filled Proposal ID
    if 'Proposal ID' in proposal_df.columns:
        proposal_df['Proposal ID'] = proposal_df['Proposal ID'].ffill()
    
    # Merge on Contract Num (CON ID)
    merged = expenditure_df.merge(
        proposal_df[['Proposal ID', 'Proposed Amount', 'Award Project Start Date', 
                     'Award Project End Date', 'Instrument Type', 'Program Type']],
        left_on='Contract Num',
        right_on='Proposal ID',
        how='left',
        suffixes=('', '_proposal')
    )
    
    return merged


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        df = load_expenditure_data(filepath, verbose=True)
        
        # Validate
        validation = validate_expenditure_data(df)
        print("\nValidation Results:")
        print(f"  Valid: {validation['valid']}")
        if validation['warnings']:
            print(f"  Warnings: {validation['warnings']}")
        if validation['errors']:
            print(f"  Errors: {validation['errors']}")
        print(f"  Statistics: {validation['statistics']}")
