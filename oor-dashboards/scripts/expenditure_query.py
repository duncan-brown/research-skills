#!/usr/bin/env python3
"""
Query and analysis functions for Syracuse University Detailed Sponsored Expenditures
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Dict
from datetime import datetime


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize expenditures by expense category (Direct/Indirect/Undefined).
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Summary dataframe with totals and percentages
    """
    summary = df.groupby('Expense Category').agg({
        'Expenditure Amount': ['sum', 'count', 'mean'],
        'Contract Num': 'nunique'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Transaction_Count', 'Avg_Amount', 'Contract_Count']
    summary['Percent_of_Total'] = (summary['Total_Amount'] / summary['Total_Amount'].sum() * 100).round(1)
    
    return summary.sort_values('Total_Amount', ascending=False)


def summarize_by_subcategory(df: pd.DataFrame, 
                            category: Optional[str] = None) -> pd.DataFrame:
    """
    Summarize expenditures by expense subcategory.
    
    Args:
        df: Expenditure dataframe
        category: Filter to specific category ('DIRECT COSTS', 'INDIRECT COSTS')
    
    Returns:
        Summary dataframe
    """
    data = df.copy()
    if category:
        data = data[data['Expense Category'] == category]
    
    summary = data.groupby(['Expense Category', 'Expense SubCategory']).agg({
        'Expenditure Amount': ['sum', 'count'],
        'Contract Num': 'nunique'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Transaction_Count', 'Contract_Count']
    summary['Percent_of_Total'] = (summary['Total_Amount'] / data['Expenditure Amount'].sum() * 100).round(1)
    
    return summary.sort_values('Total_Amount', ascending=False)


def summarize_by_month(df: pd.DataFrame, 
                      fiscal_year_order: bool = True) -> pd.DataFrame:
    """
    Summarize expenditures by month.
    
    Args:
        df: Expenditure dataframe
        fiscal_year_order: Sort by fiscal year order (Jul-Jun) vs calendar
    
    Returns:
        Summary dataframe by month
    """
    summary = df.groupby('Expenditure Month Abrevation').agg({
        'Expenditure Amount': ['sum', 'count', 'mean'],
        'Contract Num': 'nunique'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Transaction_Count', 'Avg_Amount', 'Active_Contracts']
    
    if fiscal_year_order:
        # Sort by fiscal year order
        month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
                      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        summary = summary.reindex(month_order, fill_value=0)
    else:
        summary = summary.sort_values('Total_Amount', ascending=False)
    
    summary['Cumulative_Amount'] = summary['Total_Amount'].cumsum()
    summary['Percent_of_Total'] = (summary['Total_Amount'] / summary['Total_Amount'].sum() * 100).round(1)
    
    return summary


def summarize_by_unit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize expenditures by PI Administrative Unit (school/college).
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Summary dataframe by unit
    """
    summary = df.groupby('PI Administrative Unit').agg({
        'Expenditure Amount': 'sum',
        'Contract Num': 'nunique',
        'PI Name': 'nunique',
        'Syr Proj Deptid': 'nunique'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Contract_Count', 'PI_Count', 'Dept_Count']
    summary['Percent_of_Total'] = (summary['Total_Amount'] / summary['Total_Amount'].sum() * 100).round(1)
    summary['Avg_per_Contract'] = (summary['Total_Amount'] / summary['Contract_Count']).round(2)
    
    return summary.sort_values('Total_Amount', ascending=False)


def filter_by_pi(df: pd.DataFrame, 
                pi_name: Optional[str] = None,
                pi_department: Optional[str] = None,
                pi_unit: Optional[str] = None) -> pd.DataFrame:
    """
    Filter expenditures by PI criteria.
    
    Args:
        df: Expenditure dataframe
        pi_name: PI name (partial match supported)
        pi_department: PI department name
        pi_unit: PI administrative unit
    
    Returns:
        Filtered dataframe
    """
    result = df.copy()
    
    if pi_name:
        result = result[result['PI Name'].str.contains(pi_name, case=False, na=False)]
    
    if pi_department:
        result = result[result['PI Department (if any)'].str.contains(pi_department, case=False, na=False)]
    
    if pi_unit:
        result = result[result['PI Administrative Unit'].str.contains(pi_unit, case=False, na=False)]
    
    return result


def filter_by_department(df: pd.DataFrame, 
                        deptid: Optional[int] = None,
                        dept_name: Optional[str] = None) -> pd.DataFrame:
    """
    Filter expenditures by department (using Syr Proj Deptid).
    
    Args:
        df: Expenditure dataframe
        deptid: Department ID number
        dept_name: Department name (partial match)
    
    Returns:
        Filtered dataframe
    """
    result = df.copy()
    
    if deptid:
        result = result[result['Syr Proj Deptid'] == deptid]
    
    if dept_name:
        result = result[result['Syr Proj Deptid Descr'].str.contains(dept_name, case=False, na=False)]
    
    return result


def filter_by_sponsor_type(df: pd.DataFrame, 
                          sponsor_type: str) -> pd.DataFrame:
    """
    Filter expenditures by primary sponsor type.
    
    Args:
        df: Expenditure dataframe
        sponsor_type: One of 'Federal Agencies', 'Not for Profit/Foundation', 
                     'Corporations/Companies', 'New York State', etc.
    
    Returns:
        Filtered dataframe
    """
    return df[df['Primary Sponsor Type'] == sponsor_type]


def analyze_federal_spending(df: pd.DataFrame) -> Dict:
    """
    Analyze federal spending by department and office.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Dictionary with federal spending analysis
    """
    federal_df = df[df['Primary Sponsor Type'] == 'Federal Agencies']
    
    if len(federal_df) == 0:
        return {'total': 0, 'by_department': pd.DataFrame(), 'by_office': pd.DataFrame()}
    
    by_dept = federal_df.groupby('Federal Department')['Expenditure Amount'].sum().sort_values(ascending=False)
    by_office = federal_df.groupby('Federal Office')['Expenditure Amount'].sum().sort_values(ascending=False)
    
    return {
        'total': federal_df['Expenditure Amount'].sum(),
        'by_department': by_dept,
        'by_office': by_office,
        'percent_of_total': federal_df['Expenditure Amount'].sum() / df['Expenditure Amount'].sum() * 100
    }


def analyze_direct_indirect(df: pd.DataFrame) -> Dict:
    """
    Analyze direct vs indirect costs and calculate effective F&A rate.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Dictionary with direct/indirect analysis
    """
    direct = df[df['Expense Category'] == 'DIRECT COSTS']['Expenditure Amount'].sum()
    indirect = df[df['Expense Category'] == 'INDIRECT COSTS']['Expenditure Amount'].sum()
    undefined = df[df['Expense Category'] == 'UNDEFINED ACCOUNT']['Expenditure Amount'].sum()
    
    # Calculate modified total direct costs (MTDC) - excluding equipment and subcontracts over $25k
    # Note: This is simplified - actual MTDC calculation is more complex
    mtdc = df[
        (df['Expense Category'] == 'DIRECT COSTS') & 
        (~df['Expense SubCategory'].isin(['Equipment', 'Subcontracts']))
    ]['Expenditure Amount'].sum()
    
    effective_rate = (indirect / mtdc * 100) if mtdc > 0 else 0
    
    return {
        'direct_costs': direct,
        'indirect_costs': indirect,
        'undefined_costs': undefined,
        'total': direct + indirect + undefined,
        'direct_percent': direct / (direct + indirect + undefined) * 100,
        'indirect_percent': indirect / (direct + indirect + undefined) * 100,
        'mtdc': mtdc,
        'effective_rate': effective_rate
    }


def get_top_contracts(df: pd.DataFrame, 
                     n: int = 10,
                     by: str = 'amount') -> pd.DataFrame:
    """
    Get top contracts by expenditure amount or transaction count.
    
    Args:
        df: Expenditure dataframe
        n: Number of top contracts to return
        by: 'amount' or 'count'
    
    Returns:
        Dataframe with top contracts
    """
    summary = df.groupby(['Contract Num', 'Award Title', 'PI Name', 'PI Administrative Unit']).agg({
        'Expenditure Amount': 'sum',
        'Expense Category': 'count'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Transaction_Count']
    
    if by == 'amount':
        summary = summary.sort_values('Total_Amount', ascending=False)
    else:
        summary = summary.sort_values('Transaction_Count', ascending=False)
    
    return summary.head(n)


def get_top_pis(df: pd.DataFrame, 
               n: int = 10) -> pd.DataFrame:
    """
    Get top PIs by total expenditure.
    
    Args:
        df: Expenditure dataframe
        n: Number of top PIs to return
    
    Returns:
        Dataframe with top PIs
    """
    summary = df.groupby(['PI Name', 'PI Department (if any)', 'PI Administrative Unit']).agg({
        'Expenditure Amount': 'sum',
        'Contract Num': 'nunique'
    }).round(2)
    
    summary.columns = ['Total_Amount', 'Contract_Count']
    summary['Avg_per_Contract'] = (summary['Total_Amount'] / summary['Contract_Count']).round(2)
    
    return summary.sort_values('Total_Amount', ascending=False).head(n)


def get_burn_rate(df: pd.DataFrame, 
                 contract_num: str) -> Dict:
    """
    Calculate burn rate for a specific contract.
    
    Args:
        df: Expenditure dataframe
        contract_num: Contract number (CON ID)
    
    Returns:
        Dictionary with burn rate analysis
    """
    contract_df = df[df['Contract Num'] == contract_num]
    
    if len(contract_df) == 0:
        return {'error': f'Contract {contract_num} not found'}
    
    # Monthly spending
    monthly = contract_df.groupby('Expenditure Month Abrevation')['Expenditure Amount'].sum()
    
    # Calculate metrics
    total_spent = contract_df['Expenditure Amount'].sum()
    months_active = contract_df['Expenditure Month Abrevation'].nunique()
    avg_monthly = total_spent / months_active if months_active > 0 else 0
    
    # Get first and last month
    month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
                  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    months_present = [m for m in month_order if m in monthly.index]
    
    return {
        'contract_num': contract_num,
        'award_title': contract_df['Award Title'].iloc[0],
        'pi_name': contract_df['PI Name'].iloc[0],
        'total_spent': total_spent,
        'months_active': months_active,
        'avg_monthly_burn': avg_monthly,
        'monthly_spending': monthly.to_dict(),
        'first_month': months_present[0] if months_present else None,
        'last_month': months_present[-1] if months_present else None,
        'direct_costs': contract_df[contract_df['Expense Category'] == 'DIRECT COSTS']['Expenditure Amount'].sum(),
        'indirect_costs': contract_df[contract_df['Expense Category'] == 'INDIRECT COSTS']['Expenditure Amount'].sum()
    }


def identify_cost_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify potential cost share expenditures.
    Cost share typically shows as specific MyCode patterns or fund sources.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Dataframe with potential cost share transactions
    """
    # This is a simplified version - actual cost share identification
    # would require Chart of Accounts data integration
    
    # Look for common cost share indicators
    # Negative expenditures sometimes indicate cost share corrections
    potential_cs = df[
        (df['Expenditure Amount'] < 0) |
        (df['Expense Category'] == 'UNDEFINED ACCOUNT')
    ].copy()
    
    return potential_cs


def compare_to_budget(expenditure_df: pd.DataFrame,
                     proposal_df: pd.DataFrame,
                     contract_num: str) -> Dict:
    """
    Compare actual expenditures to proposed budget.
    
    Args:
        expenditure_df: Expenditure dataframe
        proposal_df: Proposal dataframe (from sponsored-proposals skill)
        contract_num: Contract number to analyze
    
    Returns:
        Dictionary with budget vs actual comparison
    """
    # Get expenditure data
    exp_data = expenditure_df[expenditure_df['Contract Num'] == contract_num]
    
    if len(exp_data) == 0:
        return {'error': f'No expenditure data for {contract_num}'}
    
    # Get proposal data
    prop_data = proposal_df[proposal_df['Proposal ID'] == contract_num]
    
    if len(prop_data) == 0:
        return {'warning': 'No proposal data found', 'total_spent': exp_data['Expenditure Amount'].sum()}
    
    proposed_amount = prop_data['Proposed Amount'].iloc[0]
    total_spent = exp_data['Expenditure Amount'].sum()
    
    return {
        'contract_num': contract_num,
        'proposed_amount': proposed_amount,
        'total_spent': total_spent,
        'remaining': proposed_amount - total_spent,
        'percent_spent': (total_spent / proposed_amount * 100) if proposed_amount > 0 else 0,
        'direct_spent': exp_data[exp_data['Expense Category'] == 'DIRECT COSTS']['Expenditure Amount'].sum(),
        'indirect_spent': exp_data[exp_data['Expense Category'] == 'INDIRECT COSTS']['Expenditure Amount'].sum()
    }


if __name__ == "__main__":
    # Example usage
    from load_expenditure_data import load_expenditure_data
    import sys
    
    if len(sys.argv) > 1:
        df = load_expenditure_data(sys.argv[1])
        
        print("Category Summary:")
        print(summarize_by_category(df))
        
        print("\nMonthly Summary:")
        print(summarize_by_month(df))
        
        print("\nTop 5 Contracts:")
        print(get_top_contracts(df, n=5))
