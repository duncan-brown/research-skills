#!/usr/bin/env python3
"""
Query and analysis functions for Sponsored Proposals and Award Details data.

Provides common filtering and aggregation patterns including:
- Status, date, PI, and sponsor filtering
- Academic vs administrative department filtering
- Instrument type and program type consolidation
- Faculty cross-referencing
- Fiscal year calculations
- Summary and aggregation functions
- Award total calculations with supplement tracking
- Active/completed award filtering
- Annual rate calculations
"""

import pandas as pd
from datetime import datetime
from typing import Optional, Union, List


# =============================================================================
# PROPOSAL QUERY FUNCTIONS
# =============================================================================

def filter_by_status(df: pd.DataFrame, 
                     status: Union[str, List[str]]) -> pd.DataFrame:
    """
    Filter proposals by status.
    
    Args:
        df: Proposals DataFrame
        status: Single status or list of statuses
                Valid: 'Funded', 'Not Funded', 'Pending'
    
    Returns:
        Filtered DataFrame
    """
    if isinstance(status, str):
        status = [status]
    
    return df[df['Proposal Status'].isin(status)]


def filter_by_date_range(df: pd.DataFrame,
                         start_after: Optional[datetime] = None,
                         start_before: Optional[datetime] = None,
                         end_after: Optional[datetime] = None,
                         end_before: Optional[datetime] = None) -> pd.DataFrame:
    """
    Filter proposals by project start/end dates.
    
    Args:
        df: Proposals DataFrame
        start_after: Start date must be after this
        start_before: Start date must be before this
        end_after: End date must be after this
        end_before: End date must be before this
    
    Returns:
        Filtered DataFrame
    """
    result = df.copy()
    
    if start_after:
        result = result[result['Award Project Start Date'] > start_after]
    if start_before:
        result = result[result['Award Project Start Date'] < start_before]
    if end_after:
        result = result[result['Award Project End Date'] > end_after]
    if end_before:
        result = result[result['Award Project End Date'] < end_before]
    
    return result


def filter_by_pi(df: pd.DataFrame,
                 pi_name: Optional[str] = None,
                 pi_deptid: Optional[int] = None,
                 pi_unit: Optional[str] = None) -> pd.DataFrame:
    """
    Filter proposals or awards by PI characteristics.
    
    Args:
        df: Proposals or Awards DataFrame
        pi_name: PI name (partial match supported)
        pi_deptid: PI department ID (exact match)
        pi_unit: PI administrative unit (partial match)
    
    Returns:
        Filtered DataFrame
    """
    result = df.copy()
    
    if pi_name:
        result = result[result['PI Name'].str.contains(pi_name, case=False, na=False)]
    if pi_deptid:
        result = result[result['PI Deptid'] == pi_deptid]
    if pi_unit:
        result = result[result['PI Administrative Unit'].str.contains(pi_unit, case=False, na=False)]
    
    return result


def filter_by_sponsor(df: pd.DataFrame,
                     sponsor_type: Optional[str] = None,
                     primary_sponsor: Optional[str] = None,
                     federal_department: Optional[str] = None,
                     is_federal: Optional[bool] = None) -> pd.DataFrame:
    """
    Filter proposals or awards by sponsor characteristics.
    
    Args:
        df: Proposals or Awards DataFrame
        sponsor_type: Primary Sponsor Type (partial match)
        primary_sponsor: Primary Sponsor name (partial match)
        federal_department: Federal Department (partial match)
        is_federal: True for federal only, False for non-federal only
    
    Returns:
        Filtered DataFrame
    """
    result = df.copy()
    
    if sponsor_type:
        result = result[result['Primary Sponsor Type'].str.contains(sponsor_type, case=False, na=False)]
    if primary_sponsor:
        result = result[result['Primary Sponsor'].str.contains(primary_sponsor, case=False, na=False)]
    if federal_department:
        result = result[result['Federal Department'].str.contains(federal_department, case=False, na=False)]
    if is_federal is not None:
        if is_federal:
            result = result[result['Primary Sponsor Type'] == 'Federal Agencies']
        else:
            result = result[result['Primary Sponsor Type'] != 'Federal Agencies']
    
    return result


def identify_subcontracts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify proposals that are subcontracts or subgrants.
    
    Returns proposals where Primary Sponsor != Sponsor Name,
    indicating SU is a subcontractor/subgrantee.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        DataFrame with subcontract/subgrant proposals only
    """
    return df[df['Primary Sponsor'] != df['Sponsor Name']]


def summarize_by_unit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize proposals by PI Administrative Unit.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        Summary DataFrame with counts and totals by unit
    """
    summary = df.groupby('PI Administrative Unit').agg({
        'Proposal ID': 'count',
        'Proposed Amount': ['sum', 'mean', 'median']
    }).round(0)
    
    summary.columns = ['Count', 'Total Amount', 'Mean Amount', 'Median Amount']
    summary = summary.sort_values('Total Amount', ascending=False)
    
    return summary


def summarize_by_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize proposals by status.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        Summary DataFrame with counts and totals by status
    """
    summary = df.groupby('Proposal Status').agg({
        'Proposal ID': 'count',
        'Proposed Amount': ['sum', 'mean']
    }).round(0)
    
    summary.columns = ['Count', 'Total Amount', 'Mean Amount']
    summary = summary.sort_values('Count', ascending=False)
    
    return summary


def summarize_by_sponsor_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize proposals by Primary Sponsor Type.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        Summary DataFrame with counts and totals by sponsor type
    """
    summary = df.groupby('Primary Sponsor Type').agg({
        'Proposal ID': 'count',
        'Proposed Amount': ['sum', 'mean']
    }).round(0)
    
    summary.columns = ['Count', 'Total Amount', 'Mean Amount']
    summary = summary.sort_values('Total Amount', ascending=False)
    
    return summary


def get_top_pis(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get top PIs by number of proposals or total amount.
    
    Args:
        df: Proposals DataFrame
        n: Number of top PIs to return
    
    Returns:
        Summary DataFrame with top PIs
    """
    summary = df.groupby('PI Name').agg({
        'Proposal ID': 'count',
        'Proposed Amount': 'sum',
        'PI Administrative Unit': 'first',
        'PI Deptid': 'first'
    }).round(0)
    
    summary.columns = ['Proposal Count', 'Total Amount', 'Unit', 'Deptid']
    summary = summary.sort_values('Total Amount', ascending=False).head(n)
    
    return summary


def filter_academic_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to academic department proposals/awards only (exclude administrative).
    
    Excludes area codes: 10xxx, 19xxx, 20xxx, 30xxx, 31xxx, 40xxx
    Includes: 21xxx (schools/colleges), 22xxx (research centers), 23xxx (VPA)
    
    Args:
        df: Proposals or Awards DataFrame
    
    Returns:
        DataFrame with only academic department entries
        
    Notes:
        Research centers like CASE (20305) are excluded even though
        faculty may submit there. Use cross_reference_faculty() for
        more nuanced filtering.
    """
    result = df.copy()
    result['Area_Code'] = (result['PI Deptid'] // 1000).astype('Int64')
    academic_areas = [21, 22, 23]
    return result[result['Area_Code'].isin(academic_areas)]


def filter_administrative_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to administrative department proposals/awards only.
    
    Includes area codes: 10xxx, 19xxx, 20xxx, 30xxx, 31xxx, 40xxx
    
    Args:
        df: Proposals or Awards DataFrame
    
    Returns:
        DataFrame with only administrative department entries
    """
    result = df.copy()
    result['Area_Code'] = (result['PI Deptid'] // 1000).astype('Int64')
    admin_areas = [10, 19, 20, 30, 31, 40]
    return result[result['Area_Code'].isin(admin_areas)]


def consolidate_instrument_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolidate Instrument Type by removing 'Inst Type - ' prefix.
    
    PeopleSoft adds 'Inst Type - ' prefix. This function standardizes
    by removing the prefix and consolidating variations.
    
    Args:
        df: Proposals or Awards DataFrame
    
    Returns:
        DataFrame with 'Instrument Type Clean' column added
    """
    result = df.copy()
    
    result['Instrument Type Clean'] = result['Instrument Type'].str.replace(
        'Inst Type - ', '', regex=False
    )
    
    result['Instrument Type Clean'] = result['Instrument Type Clean'].replace({
        'Subgrant (Prime = Grant)': 'Subgrant',
        'Subcontract (Prime = Contract)': 'Subcontract'
    })
    
    return result


def consolidate_program_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolidate Program Type values.
    
    Consolidates InfoEd and PeopleSoft terminology differences.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        DataFrame with 'Program Type Clean' column added
    """
    result = df.copy()
    
    result['Program Type Clean'] = result['Program Type'].replace({
        'Research': 'Research - Basic',
        'Instruction/Training': 'Training',
        'Appropriation: Instruction/Training': 'Training'
    })
    
    return result


def cross_reference_faculty(df_proposals: pd.DataFrame, 
                            df_faculty: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-reference proposals with faculty data.
    
    Matches on PI last name and first name, handling middle initial variations.
    Handles "I First" format (e.g., "Smith, J Robert" -> matches on "Michael").
    
    Args:
        df_proposals: Proposals DataFrame (from load_proposal_data)
        df_faculty: Faculty DataFrame (from faculty-by-unit data, with forward-filled columns)
    
    Returns:
        Merged DataFrame with faculty information added.
        Use '_merge' column to identify matches ('both' = matched, 'left_only' = unmatched).
    """
    proposals = df_proposals.copy()
    
    proposals['PI_Last'] = proposals['PI Name'].str.split(',', n=1).str[0].str.strip()
    proposals['PI_First_Full'] = proposals['PI Name'].str.split(',', n=1).str[1].str.strip()
    
    def get_first_name(full_first):
        if pd.isna(full_first):
            return None
        parts = full_first.split()
        if len(parts) == 0:
            return None
        if len(parts) > 1 and len(parts[0]) == 1 and parts[0].isalpha():
            return parts[1]
        return parts[0]
    
    proposals['PI_First'] = proposals['PI_First_Full'].apply(get_first_name)
    
    result = proposals.merge(
        df_faculty[['MAIN_LAST_NAME', 'MAIN_FIRST_NAME', 'UNIT', 'EMPLID', 
                   'JOBCODE_DESC', 'TENURE_STATUS_DESC', 'EG_ACADEMIC_RANK_DESC',
                   'DEPARTMENT_DESC', 'REGULAR_OR_TEMP_EMPL']],
        left_on=['PI_Last', 'PI_First'],
        right_on=['MAIN_LAST_NAME', 'MAIN_FIRST_NAME'],
        how='left',
        indicator=True,
        suffixes=('_proposal', '_faculty')
    )
    
    return result


def identify_faculty_pis(df_proposals: pd.DataFrame,
                        df_faculty: pd.DataFrame) -> pd.DataFrame:
    """
    Identify which PIs are faculty (vs staff/directors).
    
    Args:
        df_proposals: Proposals DataFrame
        df_faculty: Faculty DataFrame
    
    Returns:
        DataFrame with 'Is_Faculty' boolean column added
    """
    matched = cross_reference_faculty(df_proposals, df_faculty)
    
    result = df_proposals.copy()
    result['Is_Faculty'] = matched['_merge'] == 'both'
    
    return result


def get_fiscal_year(date: datetime) -> int:
    """
    Get fiscal year for a date (July 1 - June 30).
    
    Args:
        date: Date to convert
    
    Returns:
        Fiscal year (e.g., FY2025 for dates between July 1, 2024 and June 30, 2025)
    """
    if date.month >= 7:
        return date.year + 1
    else:
        return date.year


def add_fiscal_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add fiscal year columns based on project start date.
    
    Args:
        df: Proposals DataFrame
    
    Returns:
        DataFrame with 'Fiscal Year' column added
    """
    result = df.copy()
    result['Fiscal Year'] = result['Award Project Start Date'].apply(
        lambda x: get_fiscal_year(x) if pd.notna(x) else None
    )
    return result


# =============================================================================
# AWARD QUERY FUNCTIONS (for Award Details data)
# =============================================================================

def calculate_total_award(df_awards: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total anticipated award per CON (base + all supplements).
    
    Sums all rows per Contract Num including base, supplements, and
    deobligations (negative amounts).
    
    Args:
        df_awards: Award Details DataFrame (from load_award_data)
    
    Returns:
        DataFrame indexed by Contract Num with columns:
        - Total_Award: Sum of all amounts
        - Base_Amount: Anticipated Amount only
        - Supplement_Total: Sum of all supplements
        - Supplement_Count: Number of supplement rows
        - Award_Title: Title of the award
        - PI_Name: PI name
        - Award_Status: Active or Completed
    """
    # Base awards (Award Label == 'Anticipated Amount')
    base = df_awards[df_awards['Award Label'] == 'Anticipated Amount'].groupby('Contract Num').agg({
        'Anticipated & Supplement Award Amount': 'sum',
        'Award Title': 'first',
        'PI Name': 'first',
        'Award Status': 'first',
        'PI Administrative Unit': 'first'
    })
    base.columns = ['Base_Amount', 'Award_Title', 'PI_Name', 'Award_Status', 'PI_Unit']
    
    # Supplements (Award Label != 'Anticipated Amount' or NaN)
    supps = df_awards[df_awards['Award Label'] != 'Anticipated Amount'].groupby('Contract Num').agg({
        'Anticipated & Supplement Award Amount': ['sum', 'count']
    })
    supps.columns = ['Supplement_Total', 'Supplement_Count']
    
    # Total per CON
    totals = df_awards.groupby('Contract Num')['Anticipated & Supplement Award Amount'].sum()
    totals.name = 'Total_Award'
    
    # Combine
    result = base.join(supps, how='left').join(totals)
    result['Supplement_Total'] = result['Supplement_Total'].fillna(0)
    result['Supplement_Count'] = result['Supplement_Count'].fillna(0).astype(int)
    
    return result.sort_values('Total_Award', ascending=False)


def filter_active_awards(df_awards: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to currently active awards only.
    
    Args:
        df_awards: Award Details DataFrame
    
    Returns:
        DataFrame with only active awards (Award Status == 'Active')
    """
    return df_awards[df_awards['Award Status'] == 'Active']


def filter_completed_awards(df_awards: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to completed awards only.
    
    Args:
        df_awards: Award Details DataFrame
    
    Returns:
        DataFrame with only completed awards (Award Status == 'Completed')
    """
    return df_awards[df_awards['Award Status'] == 'Completed']


def get_awards_with_supplements(df_awards: pd.DataFrame) -> pd.DataFrame:
    """
    Identify awards that have supplements.
    
    Returns one row per CON that has at least one supplement,
    with base amount, supplement total, and overall total.
    
    Args:
        df_awards: Award Details DataFrame
    
    Returns:
        DataFrame with columns: Contract Num, Award_Title, PI_Name,
        Base_Amount, Supplement_Total, Supplement_Count, Total_Award
    """
    totals = calculate_total_award(df_awards)
    with_supps = totals[totals['Supplement_Count'] > 0].copy()
    return with_supps.sort_values('Total_Award', ascending=False)


def calculate_annual_rate(df_awards: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate annual award rate ($/year) for awards.
    
    Uses Award Project Start Date and End Date to determine duration,
    then divides total award by number of years.
    
    Args:
        df_awards: Award Details DataFrame (typically filtered to base awards)
    
    Returns:
        DataFrame with 'Annual_Rate' and 'Duration_Years' columns added
    """
    result = df_awards.copy()
    
    # Ensure dates are datetime
    for col in ['Award Project Start Date', 'Award Project End Date']:
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], errors='coerce')
    
    # Calculate duration in years
    result['Duration_Days'] = (
        result['Award Project End Date'] - result['Award Project Start Date']
    ).dt.days
    result['Duration_Years'] = result['Duration_Days'] / 365.25
    
    # Get total award per CON
    con_totals = result.groupby('Contract Num')['Anticipated & Supplement Award Amount'].sum()
    result = result.merge(
        con_totals.rename('Total_Award_Amount'),
        left_on='Contract Num',
        right_index=True,
        how='left'
    )
    
    # Calculate annual rate
    result['Annual_Rate'] = result.apply(
        lambda row: row['Total_Award_Amount'] / row['Duration_Years'] 
        if pd.notna(row['Duration_Years']) and row['Duration_Years'] > 0 
        else None,
        axis=1
    )
    
    return result


def parse_project_ids(project_id_str: str) -> list:
    """
    Parse semicolon-separated Project IDs from Award Details.
    
    Args:
        project_id_str: Project ID string (e.g., "06938; 07164")
    
    Returns:
        List of individual Project ID strings
    """
    if pd.isna(project_id_str):
        return []
    return [pid.strip() for pid in str(project_id_str).split(';') if pid.strip()]


if __name__ == '__main__':
    print("proposal_query.py - Query helper functions for Sponsored Proposals and Award Details data")
    print("\nThis module provides filtering and aggregation functions.")
    print("Import and use with loaded proposals or awards DataFrames.")
    print("\nExample:")
    print("  from scripts.load_proposal_data import load_proposal_data")
    print("  from scripts.proposal_query import filter_by_status, summarize_by_unit")
    print("  ")
    print("  df = load_proposal_data('20251209_Proposal_Details.xlsx')")
    print("  funded = filter_by_status(df, 'Funded')")
    print("  summary = summarize_by_unit(funded)")
