# Copyright 2026 Duncan Brown
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Syracuse University F&A and Fringe Rate Lookup Functions

Self-contained within su-osp-budget v2.0 — no external skill dependencies.

Provides programmatic access to historical and current F&A and fringe benefit rates.
Rate data files are stored in the skill's assets/ directory.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

# Default assets directory relative to this script
_DEFAULT_ASSETS_DIR = Path(__file__).parent.parent / "assets"


def get_fiscal_year(date=None):
    """
    Calculate Syracuse University fiscal year from a date.
    
    SU fiscal year runs July 1 - June 30, named by ending calendar year.
    
    Args:
        date: datetime object (default: today)
        
    Returns:
        int: Fiscal year (e.g., 2026 for dates in July 1, 2025 - June 30, 2026)
    """
    if date is None:
        date = datetime.now()
    
    if date.month >= 7:  # July or later
        return date.year + 1
    else:  # January - June
        return date.year


def load_fa_rates(data_dir=None):
    """Load F&A rate history from the skill's assets directory."""
    if data_dir is None:
        data_dir = _DEFAULT_ASSETS_DIR
    path = Path(data_dir) / "fa_rate_history.xlsx"
    return pd.read_excel(path)


def load_fringe_rates(data_dir=None):
    """Load fringe rate history from rate agreements."""
    if data_dir is None:
        data_dir = _DEFAULT_ASSETS_DIR
    path = Path(data_dir) / "fringe_rate_history.xlsx"
    return pd.read_excel(path)


def load_fringe_account_rates(fiscal_year, data_dir=None):
    """
    Load account-level fringe rates for a specific fiscal year.
    
    Args:
        fiscal_year: int (e.g., 2025, 2026)
        data_dir: path to assets directory (default: skill's assets/)
        
    Returns:
        DataFrame with account-level fringe rates
    """
    if data_dir is None:
        data_dir = _DEFAULT_ASSETS_DIR
    filename = f"fringe_rates_by_account_fy{fiscal_year}.xlsx"
    path = Path(data_dir) / filename
    
    if not path.exists():
        raise FileNotFoundError(f"Fringe rate file not found for FY{fiscal_year}: {path}")
    
    return pd.read_excel(path)


def get_fa_rate(fiscal_year, activity_type="research", location="on-campus"):
    """
    Get F&A rate for a specific fiscal year and activity type.
    
    Args:
        fiscal_year: int or str (e.g., 2026 or "FY26")
        activity_type: "research", "training", or "other" (default: "research")
        location: "on-campus" or "off-campus" (default: "on-campus")
        
    Returns:
        float: F&A rate as decimal (e.g., 0.495 for 49.5%)
    """
    df = load_fa_rates()
    
    # Normalize fiscal year format
    if isinstance(fiscal_year, int):
        fy_str = f"FY{fiscal_year % 100}"
    else:
        fy_str = fiscal_year if fiscal_year.startswith("FY") else f"FY{fiscal_year}"
    
    # Handle FY26+ (provisional)
    if isinstance(fiscal_year, int) and fiscal_year >= 2026:
        fy_str = "FY26+"
    
    # Find the fiscal year row
    row = df[df['Fiscal Year'] == fy_str]
    if row.empty:
        raise ValueError(f"No F&A rates found for {fy_str}")
    
    row = row.iloc[0]
    
    # Select the appropriate rate column
    if location.lower() == "off-campus":
        rate_str = row['Off-Campus All Programs']
    else:
        if activity_type.lower() == "research":
            rate_str = row['On-Campus Research']
        elif activity_type.lower() in ["training", "instruction"]:
            rate_str = row['On-Campus Sponsored Training']
        elif activity_type.lower() == "other":
            rate_str = row['On-Campus Other Sponsored Activities']
        else:
            raise ValueError(f"Unknown activity type: {activity_type}")
    
    # Convert percentage string to float
    return float(rate_str.rstrip('%')) / 100


def get_fringe_rate(account_code, fund, fiscal_year=None):
    """
    Get fringe rate for a specific account code and fund.
    
    Args:
        account_code: str or int (e.g., "500011" or 500011)
        fund: str or int (11, 13, 15, 16, "11", etc.)
        fiscal_year: int (default: current fiscal year)
        
    Returns:
        float: Fringe rate as decimal (e.g., 0.295 for 29.5%)
    """
    if fiscal_year is None:
        fiscal_year = get_fiscal_year()
    
    # Load account-level rates
    df = load_fringe_account_rates(fiscal_year)
    
    # Normalize account code to string
    account_str = str(account_code)
    df['Account'] = df['Account'].astype(str)
    
    # Find account row
    row = df[df['Account'] == account_str]
    if row.empty:
        raise ValueError(f"Account {account_code} not found in FY{fiscal_year} fringe rates")
    
    row = row.iloc[0]
    
    # Determine column based on fund
    fund_str = str(fund)
    
    if fund_str in ['11', '14']:
        col = 'Unrestricted & Non-Sponsored (Fund 11 & 14)'
    elif fund_str in ['15', '16']:
        col = 'Restricted Gifts, Reserve & Endowment (Fund 15 & 16)'
    elif fund_str in ['13', '91']:
        # Default to federal for most cases
        col = 'Sponsored Federal (Fund 13 & 91)'
    else:
        raise ValueError(f"Unknown fund: {fund}")
    
    rate_str = row[col]
    
    # Handle N/A values
    if pd.isna(rate_str) or rate_str == 'N/A':
        return None
    
    # Convert percentage string to float
    return float(rate_str.rstrip('%')) / 100


def get_fringe_rate_nonfederal(account_code, fiscal_year=None):
    """
    Get non-federal sponsored fringe rate for a specific account code.
    
    Used primarily for graduate assistants on non-federal sponsored projects
    where the rate includes tuition remission (55.0% vs 10.8% federal).
    
    Args:
        account_code: str or int (e.g., "503259")
        fiscal_year: int (default: current fiscal year)
        
    Returns:
        float: Fringe rate as decimal (e.g., 0.55 for 55.0%)
    """
    if fiscal_year is None:
        fiscal_year = get_fiscal_year()
    
    df = load_fringe_account_rates(fiscal_year)
    df['Account'] = df['Account'].astype(str)
    account_str = str(account_code)
    
    row = df[df['Account'] == account_str]
    if row.empty:
        raise ValueError(f"Account {account_code} not found in FY{fiscal_year} fringe rates")
    
    row = row.iloc[0]
    rate_str = row['Sponsored Non-Federal (Fund 13 & 91)']
    
    if pd.isna(rate_str) or rate_str == 'N/A':
        return None
    
    return float(rate_str.rstrip('%')) / 100


def get_fringe_rate_with_context(employee_type, fund_type, fiscal_year=None, 
                                   is_summer=False, is_nonfederal_sponsored=False):
    """
    Get fringe rate with contextual information about employee type.
    
    Args:
        employee_type: "faculty", "research_faculty", "postdoc", "grad_assistant", 
                       "staff", "temp", "mod_pt_faculty"
        fund_type: "sponsored_federal", "sponsored_nonfederal", "unrestricted", "gift"
        fiscal_year: int (default: current)
        is_summer: bool (only relevant for faculty and some staff)
        is_nonfederal_sponsored: bool (for graduate assistants)
        
    Returns:
        tuple: (account_code, fringe_rate)
    """
    if fiscal_year is None:
        fiscal_year = get_fiscal_year()
    
    # Map employee type to account code
    account_map = {
        "faculty": "530011" if is_summer else "500011",
        "research_faculty": "500013",
        "postdoc": "513001",
        "grad_assistant": "536259" if is_summer else "503259",
        "grad_assistant_summer": "536259",
        "staff_exempt": "513021",
        "staff_nonexempt": "514072",
        "temp": "543021",
        "mod_pt_faculty": "520514"
    }
    
    account_code = account_map.get(employee_type)
    if not account_code:
        raise ValueError(f"Unknown employee type: {employee_type}")
    
    # Map fund type to fund code
    if fund_type in ["sponsored_federal", "sponsored_nonfederal"]:
        fund = "13"
    elif fund_type == "unrestricted":
        fund = "11"
    elif fund_type == "gift":
        fund = "15"
    else:
        raise ValueError(f"Unknown fund type: {fund_type}")
    
    # Get base rate
    rate = get_fringe_rate(account_code, fund, fiscal_year)
    
    # For non-federal sponsored graduate assistants, use non-federal column
    if employee_type in ["grad_assistant", "grad_assistant_summer"] and is_nonfederal_sponsored:
        rate = get_fringe_rate_nonfederal(account_code, fiscal_year)
    
    return account_code, rate
