"""
Syracuse University Budget Calculator

Self-contained within su-osp-budget v2.0 — no external skill dependencies.

Calculate fully loaded costs for personnel, equipment, and other budget items
on sponsored projects.
"""

from datetime import datetime
from rate_lookup import get_fiscal_year, get_fa_rate, get_fringe_rate


def calculate_faculty_monthly_rate(academic_year_salary):
    """
    Calculate faculty monthly rate from academic year salary.
    
    SU faculty have 8.5-month academic year appointments.
    
    Args:
        academic_year_salary: float
        
    Returns:
        float: Monthly rate
    """
    return academic_year_salary / 8.5


def calculate_mtdc(salary, fringe, exclude_items=None):
    """
    Calculate Modified Total Direct Costs.
    
    MTDC includes: salaries, wages, fringe, materials, supplies, services, 
    travel, and first $25K of each subaward.
    
    MTDC excludes: equipment (≥$5K), capital expenditures, patient care, 
    rental costs, tuition remission, scholarships, fellowships, participant 
    support, and subaward amounts >$25K.
    
    Args:
        salary: float
        fringe: float
        exclude_items: dict with keys like 'tuition', 'equipment', etc.
        
    Returns:
        float: MTDC amount
    """
    mtdc = salary + fringe
    
    # Add other direct costs that are in MTDC (if provided)
    if exclude_items:
        for item in ['supplies', 'travel', 'services', 'subaward_first_25k']:
            if item in exclude_items:
                mtdc += exclude_items[item]
    
    return mtdc


def calculate_fully_loaded_cost(salary, fringe_rate, fa_rate, on_sponsored=True):
    """
    Calculate fully loaded cost for a budget item.
    
    Args:
        salary: float - direct salary cost
        fringe_rate: float - fringe rate as decimal (e.g., 0.295)
        fa_rate: float - F&A rate as decimal (e.g., 0.495)
        on_sponsored: bool - whether on sponsored project (affects F&A)
        
    Returns:
        dict: {'salary': float, 'fringe': float, 'mtdc': float, 
               'fa': float, 'total': float}
    """
    fringe = salary * fringe_rate
    mtdc = salary + fringe
    fa = mtdc * fa_rate if on_sponsored else 0.0
    total = salary + fringe + fa
    
    return {
        'salary': salary,
        'fringe': fringe,
        'mtdc': mtdc,
        'fa': fa,
        'total': total
    }


def calculate_equipment_cost(equipment_cost, fa_rate):
    """
    Calculate fully loaded equipment cost.
    
    Equipment ≥$5,000 is excluded from MTDC (no F&A).
    Items <$5,000 are supplies/materials (F&A applies).
    
    Syracuse University equipment threshold: $5,000 per unit
    (per NICRA dated 06/04/2024).
    
    Args:
        equipment_cost: float
        fa_rate: float - F&A rate as decimal
        
    Returns:
        dict: {'direct_cost': float, 'fa': float, 'total': float, 
               'is_equipment': bool}
    """
    EQUIPMENT_THRESHOLD = 5000
    
    is_equipment = equipment_cost >= EQUIPMENT_THRESHOLD
    
    if is_equipment:
        return {
            'direct_cost': equipment_cost,
            'fa': 0.0,
            'total': equipment_cost,
            'is_equipment': True,
            'classification': 'Equipment (≥$5,000)'
        }
    else:
        fa = equipment_cost * fa_rate
        return {
            'direct_cost': equipment_cost,
            'fa': fa,
            'total': equipment_cost + fa,
            'is_equipment': False,
            'classification': 'Supplies/Materials (<$5,000)'
        }


def calculate_subaward_cost(subaward_amount, fa_rate):
    """
    Calculate F&A on subaward/subcontract.

    Syracuse University follows our federally negotiated rate agreement (DHHS, 
    dated 06/04/2024), which uses the $25,000 threshold per OMB regulations 
    in effect at the time of negotiation.
    
    First $25,000 of each subaward is included in MTDC.
    Amounts >$25,000 are excluded from MTDC.
    
    Args:
        subaward_amount: float - total subaward amount (Direct + Indirect)
        fa_rate: float - Syracuse F&A rate (e.g., 0.495 for 49.5%)
        
    Returns:
        dict: {'subaward_amount': float, 'mtdc_portion': float, 
               'excluded_portion': float, 'fa': float, 'total': float}
    """
    SUBAWARD_THRESHOLD = 25000  # Per SU NICRA 06/04/2024
    
    mtdc_portion = min(subaward_amount, SUBAWARD_THRESHOLD)
    excluded_portion = max(0, subaward_amount - SUBAWARD_THRESHOLD)
    fa = mtdc_portion * fa_rate
    
    return {
        'subaward_amount': subaward_amount,
        'mtdc_portion': mtdc_portion,
        'excluded_portion': excluded_portion,
        'fa': fa,
        'total': subaward_amount + fa
    }


def calculate_course_buyout(academic_year_salary, num_courses, fringe_rate, fa_rate, 
                             on_sponsored=True, full_teaching_buyout=False):
    """
    Calculate course buy-out cost.
    
    Per course = 15% of AY salary + fringe + F&A
    Full teaching = 80% of AY salary + fringe + F&A
    
    Args:
        academic_year_salary: float
        num_courses: int (1 or 2 without Provost approval)
        fringe_rate: float - fringe rate as decimal
        fa_rate: float - F&A rate as decimal
        on_sponsored: bool
        full_teaching_buyout: bool - if True, use 80% instead of 15% per course
        
    Returns:
        dict: Cost breakdown
    """
    if full_teaching_buyout:
        buyout_percent = 0.80
        note = "Full teaching buy-out (80%) - Requires Provost approval"
    else:
        buyout_percent = 0.15 * num_courses
        note = f"{num_courses} course(s) at 15% each"
        if num_courses > 2:
            note += " - Requires Provost approval for >2 courses"
    
    salary = academic_year_salary * buyout_percent
    fringe = salary * fringe_rate
    mtdc = salary + fringe
    fa = mtdc * fa_rate if on_sponsored else 0.0
    total = salary + fringe + fa
    
    return {
        'salary': salary,
        'fringe': fringe,
        'mtdc': mtdc,
        'fa': fa,
        'total': total,
        'note': note
    }


def apply_escalation(base_amount, years, rate=0.03):
    """
    Apply annual salary escalation.
    
    Syracuse University uses 3% annual escalation for grant budgeting.
    
    Args:
        base_amount: float - starting amount
        years: int - number of years to escalate
        rate: float - escalation rate (default: 0.03 for 3%)
        
    Returns:
        float: Escalated amount
    """
    return base_amount * ((1 + rate) ** years)


# === NIH Salary Cap Functions ===

NIH_SALARY_CAPS = {
    ('2026-01-01', '2026-12-31'): 228000,
    ('2025-01-01', '2025-12-31'): 225700,
    ('2024-10-01', '2024-12-31'): 221900,
    ('2024-01-01', '2024-09-30'): 221900,
    ('2023-10-01', '2023-12-31'): 212100,
    ('2023-01-01', '2023-09-30'): 212100,
}


def get_nih_salary_cap(date=None):
    """Get NIH salary cap for a specific date."""
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    
    date_str = date.strftime('%Y-%m-%d')
    
    for (start, end), cap in NIH_SALARY_CAPS.items():
        if start <= date_str <= end:
            return cap
    
    # Default to most recent known cap
    return 228000


def calculate_nih_capped_salary(actual_salary, months, date=None, is_calendar_year=False):
    """
    Calculate NIH salary cap compliance and cost sharing.
    
    Args:
        actual_salary: float - actual annual salary
        months: float - months of effort
        date: datetime or str - date for cap lookup (default: now)
        is_calendar_year: bool - True for 12-month, False for 8.5-month AY
        
    Returns:
        dict with actual/capped amounts and cost sharing calculation
    """
    cap = get_nih_salary_cap(date)
    
    if is_calendar_year:
        actual_monthly = actual_salary / 12
    else:
        actual_monthly = actual_salary / 8.5
    
    capped_monthly = cap / 12
    actual_total = actual_monthly * months
    capped_total = min(actual_total, capped_monthly * months)
    cost_share = actual_total - capped_total
    
    return {
        'actual_monthly_rate': actual_monthly,
        'capped_monthly_rate': capped_monthly,
        'actual_total': actual_total,
        'capped_total': capped_total,
        'cost_share_required': cost_share,
        'cap_amount': cap,
        'is_over_cap': cost_share > 0
    }
