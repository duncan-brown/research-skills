#!/usr/bin/env python3
"""
Visualization utilities for Syracuse University Detailed Sponsored Expenditures
Creates charts and reports for expenditure analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Tuple
import numpy as np


def setup_plot_style():
    """Set up consistent plot styling."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10


def plot_monthly_trend(df: pd.DataFrame, 
                      title: Optional[str] = None,
                      figsize: Tuple[int, int] = (14, 6)) -> plt.Figure:
    """
    Create a monthly expenditure trend chart.
    
    Args:
        df: Expenditure dataframe
        title: Chart title
        figsize: Figure size
    
    Returns:
        Matplotlib figure
    """
    # Set fiscal year month order
    month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
                  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    # Calculate monthly totals
    monthly = df.groupby('Expenditure Month Abrevation')['Expenditure Amount'].sum()
    monthly = monthly.reindex(month_order, fill_value=0)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Bar chart
    ax1.bar(range(len(monthly)), monthly.values / 1e6)
    ax1.set_xticks(range(len(monthly)))
    ax1.set_xticklabels(monthly.index, rotation=45)
    ax1.set_ylabel('Expenditures ($M)')
    ax1.set_title('Monthly Expenditures')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(monthly.values):
        ax1.text(i, v/1e6 + 0.1, f'${v/1e6:.1f}M', ha='center', va='bottom')
    
    # Cumulative line chart
    cumulative = monthly.cumsum()
    ax2.plot(range(len(cumulative)), cumulative.values / 1e6, marker='o', linewidth=2)
    ax2.fill_between(range(len(cumulative)), cumulative.values / 1e6, alpha=0.3)
    ax2.set_xticks(range(len(cumulative)))
    ax2.set_xticklabels(cumulative.index, rotation=45)
    ax2.set_ylabel('Cumulative Expenditures ($M)')
    ax2.set_title('Cumulative Spending Through Fiscal Year')
    ax2.grid(alpha=0.3)
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_category_breakdown(df: pd.DataFrame,
                           title: Optional[str] = None) -> plt.Figure:
    """
    Create pie and bar charts for expense category breakdown.
    
    Args:
        df: Expenditure dataframe
        title: Chart title
    
    Returns:
        Matplotlib figure
    """
    # Calculate category totals
    category_totals = df.groupby('Expense Category')['Expenditure Amount'].sum().sort_values(ascending=False)
    subcategory_totals = df.groupby('Expense SubCategory')['Expenditure Amount'].sum().sort_values(ascending=False)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart for main categories
    colors = ['#1f77b4', '#ff7f0e', '#d62728']
    wedges, texts, autotexts = ax1.pie(
        category_totals.values,
        labels=category_totals.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.05, 0.05, 0.05][:len(category_totals)]
    )
    ax1.set_title('Direct vs Indirect Costs')
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    # Horizontal bar chart for subcategories
    top_subcats = subcategory_totals.head(8)
    ax2.barh(range(len(top_subcats)), top_subcats.values / 1e6)
    ax2.set_yticks(range(len(top_subcats)))
    ax2.set_yticklabels(top_subcats.index)
    ax2.set_xlabel('Expenditures ($M)')
    ax2.set_title('Top Expense Subcategories')
    
    # Add value labels
    for i, v in enumerate(top_subcats.values):
        ax2.text(v/1e6 + 0.2, i, f'${v/1e6:.1f}M', va='center')
    
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_unit_comparison(df: pd.DataFrame,
                        top_n: int = 10) -> plt.Figure:
    """
    Create comparison chart for top administrative units.
    
    Args:
        df: Expenditure dataframe
        top_n: Number of top units to show
    
    Returns:
        Matplotlib figure
    """
    # Calculate unit totals
    unit_summary = df.groupby('PI Administrative Unit').agg({
        'Expenditure Amount': 'sum',
        'Contract Num': 'nunique'
    }).sort_values('Expenditure Amount', ascending=False).head(top_n)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Total expenditure by unit
    ax1.barh(range(len(unit_summary)), unit_summary['Expenditure Amount'].values / 1e6)
    ax1.set_yticks(range(len(unit_summary)))
    ax1.set_yticklabels(unit_summary.index)
    ax1.set_xlabel('Total Expenditures ($M)')
    ax1.set_title(f'Top {top_n} Units by Total Expenditure')
    
    for i, v in enumerate(unit_summary['Expenditure Amount'].values):
        ax1.text(v/1e6 + 0.2, i, f'${v/1e6:.1f}M', va='center')
    
    # Number of contracts by unit
    ax2.barh(range(len(unit_summary)), unit_summary['Contract Num'].values)
    ax2.set_yticks(range(len(unit_summary)))
    ax2.set_yticklabels(unit_summary.index)
    ax2.set_xlabel('Number of Active Contracts')
    ax2.set_title(f'Top {top_n} Units by Contract Count')
    
    for i, v in enumerate(unit_summary['Contract Num'].values):
        ax2.text(v + 2, i, str(v), va='center')
    
    plt.tight_layout()
    return fig


def plot_sponsor_analysis(df: pd.DataFrame) -> plt.Figure:
    """
    Create sponsor type analysis charts.
    
    Args:
        df: Expenditure dataframe
    
    Returns:
        Matplotlib figure
    """
    # Calculate sponsor type totals
    sponsor_totals = df.groupby('Primary Sponsor Type')['Expenditure Amount'].sum().sort_values(ascending=False)
    
    # Federal department breakdown (if federal data exists)
    federal_df = df[df['Primary Sponsor Type'] == 'Federal Agencies']
    if len(federal_df) > 0:
        fed_dept = federal_df.groupby('Federal Department')['Expenditure Amount'].sum().sort_values(ascending=False).head(8)
    else:
        fed_dept = pd.Series()
    
    # Create figure
    if len(fed_dept) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(8, 6))
        ax2 = None
    
    # Sponsor type pie chart
    colors = sns.color_palette('Set2', n_colors=len(sponsor_totals))
    wedges, texts, autotexts = ax1.pie(
        sponsor_totals.values,
        labels=[f"{l}\n${v/1e6:.1f}M" for l, v in zip(sponsor_totals.index, sponsor_totals.values)],
        autopct='%1.1f%%',
        colors=colors
    )
    ax1.set_title('Expenditures by Sponsor Type')
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    # Federal department breakdown (if applicable)
    if ax2 and len(fed_dept) > 0:
        ax2.barh(range(len(fed_dept)), fed_dept.values / 1e6)
        ax2.set_yticks(range(len(fed_dept)))
        ax2.set_yticklabels([label[:30] + '...' if len(label) > 30 else label 
                             for label in fed_dept.index])
        ax2.set_xlabel('Expenditures ($M)')
        ax2.set_title('Top Federal Departments')
        
        for i, v in enumerate(fed_dept.values):
            ax2.text(v/1e6 + 0.1, i, f'${v/1e6:.1f}M', va='center')
    
    plt.tight_layout()
    return fig


def create_summary_report(df: pd.DataFrame, 
                         output_file: Optional[str] = None) -> str:
    """
    Create a text summary report of expenditure data.
    
    Args:
        df: Expenditure dataframe
        output_file: Optional file path to save report
    
    Returns:
        Report text
    """
    report = []
    report.append("=" * 80)
    report.append("SYRACUSE UNIVERSITY - DETAILED SPONSORED EXPENDITURES REPORT")
    report.append("=" * 80)
    
    # Get fiscal year
    fy = df['Expenditure Fiscal Year'].iloc[0] if 'Expenditure Fiscal Year' in df.columns else 'Unknown'
    report.append(f"\nFiscal Year: {int(fy) if not pd.isna(fy) else 'Unknown'}")
    report.append(f"Report Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Overall statistics
    report.append("\n" + "=" * 80)
    report.append("OVERALL STATISTICS")
    report.append("=" * 80)
    total_exp = df['Expenditure Amount'].sum()
    report.append(f"Total Expenditures: ${total_exp:,.2f}")
    report.append(f"Total Contracts: {df['Contract Num'].nunique()}")
    report.append(f"Total PIs: {df['PI Name'].nunique()}")
    report.append(f"Total Transactions: {len(df)}")
    
    # Direct vs Indirect
    direct = df[df['Expense Category'] == 'DIRECT COSTS']['Expenditure Amount'].sum()
    indirect = df[df['Expense Category'] == 'INDIRECT COSTS']['Expenditure Amount'].sum()
    report.append(f"\nDirect Costs: ${direct:,.2f} ({direct/total_exp*100:.1f}%)")
    report.append(f"Indirect Costs: ${indirect:,.2f} ({indirect/total_exp*100:.1f}%)")
    report.append(f"Effective F&A Rate: {indirect/direct*100:.1f}%")
    
    # Top categories
    report.append("\n" + "=" * 80)
    report.append("TOP EXPENSE SUBCATEGORIES")
    report.append("=" * 80)
    subcats = df.groupby('Expense SubCategory')['Expenditure Amount'].sum().sort_values(ascending=False)
    for subcat, amount in subcats.head(5).items():
        report.append(f"{subcat:30} ${amount:15,.2f} ({amount/total_exp*100:5.1f}%)")
    
    # Top units
    report.append("\n" + "=" * 80)
    report.append("TOP ADMINISTRATIVE UNITS")
    report.append("=" * 80)
    units = df.groupby('PI Administrative Unit')['Expenditure Amount'].sum().sort_values(ascending=False)
    for unit, amount in units.head(5).items():
        report.append(f"{unit:30} ${amount:15,.2f} ({amount/total_exp*100:5.1f}%)")
    
    # Top PIs
    report.append("\n" + "=" * 80)
    report.append("TOP PRINCIPAL INVESTIGATORS")
    report.append("=" * 80)
    pis = df.groupby('PI Name')['Expenditure Amount'].sum().sort_values(ascending=False)
    for pi, amount in pis.head(10).items():
        dept = df[df['PI Name'] == pi]['PI Department (if any)'].iloc[0]
        report.append(f"{pi:30} ${amount:12,.2f}  ({dept})")
    
    # Monthly summary
    report.append("\n" + "=" * 80)
    report.append("MONTHLY EXPENDITURE SUMMARY")
    report.append("=" * 80)
    month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
                  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    monthly = df.groupby('Expenditure Month Abrevation')['Expenditure Amount'].sum()
    monthly = monthly.reindex(month_order, fill_value=0)
    
    cumulative = 0
    for month, amount in monthly.items():
        cumulative += amount
        report.append(f"{month:3}  ${amount:12,.2f}  Cumulative: ${cumulative:12,.2f}")
    
    # Join report lines
    report_text = '\n'.join(report)
    
    # Save if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"Report saved to: {output_file}")
    
    return report_text


if __name__ == "__main__":
    # Example usage
    from load_expenditure_data import load_expenditure_data
    import sys
    
    if len(sys.argv) > 1:
        df = load_expenditure_data(sys.argv[1])
        
        # Set up style
        setup_plot_style()
        
        # Create visualizations
        fig1 = plot_monthly_trend(df, "FY25 Monthly Expenditure Trend")
        fig2 = plot_category_breakdown(df, "FY25 Expense Category Analysis")
        fig3 = plot_unit_comparison(df)
        fig4 = plot_sponsor_analysis(df)
        
        # Generate report
        report = create_summary_report(df, "expenditure_summary.txt")
        print(report)
        
        # Show plots
        plt.show()
