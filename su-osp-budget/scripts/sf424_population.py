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
SF424 R&R Budget Population Script for DOE Genesis Mission

This script populates the SF424 R&R Budget template from computed budget
values. It is designed to work alongside the OSP Budget Template population
script, using the same Python-computed values as the single source of truth.

All dollar amounts, fringe calculations, MTDC bases, and F&A computations
must be performed in Python code — never by LLM arithmetic.

Phase I only: populates Budget Period 1 sheets and the Cumulative sheet.
"""

from openpyxl import load_workbook
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import shutil


# === DATA CLASSES ===

@dataclass
class SF424SeniorPerson:
    """A senior/key person for the SF424 R&R Section A."""
    prefix: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    suffix: str = ""
    project_role: str = ""  # "Principal Investigator", "Co-PI", etc.
    base_salary: float = 0
    cal_months: float = 0
    acad_months: float = 0
    sum_months: float = 0
    requested_salary: float = 0   # Must be computed in Python
    fringe_benefits: float = 0    # Must be computed in Python
    funds_requested: float = 0    # Must be computed in Python (salary + fringe)


@dataclass
class SF424OtherPersonnel:
    """Aggregated other personnel for SF424 R&R Section B."""
    # Each entry is (count, cal_months, acad_months, sum_months, salary, fringe, total)
    postdoc_count: int = 0
    postdoc_cal_months: float = 0
    postdoc_acad_months: float = 0
    postdoc_sum_months: float = 0
    postdoc_salary: float = 0
    postdoc_fringe: float = 0
    postdoc_total: float = 0

    grad_count: int = 0
    grad_cal_months: float = 0
    grad_acad_months: float = 0
    grad_sum_months: float = 0
    grad_salary: float = 0
    grad_fringe: float = 0
    grad_total: float = 0

    undergrad_count: int = 0
    undergrad_salary: float = 0
    undergrad_fringe: float = 0
    undergrad_total: float = 0

    secretarial_count: int = 0
    secretarial_salary: float = 0
    secretarial_fringe: float = 0
    secretarial_total: float = 0

    # Up to 6 additional "other" categories (rows 31-36 on SF424)
    other_categories: List[Dict[str, Any]] = field(default_factory=list)
    # Each dict: {"label": str, "count": int, "salary": float,
    #             "fringe": float, "total": float}


@dataclass
class SF424Equipment:
    """Equipment items for SF424 R&R Section C."""
    # List of (description, cost) tuples
    items: List[tuple] = field(default_factory=list)


@dataclass
class SF424Travel:
    """Travel costs for SF424 R&R Section D."""
    domestic: float = 0
    foreign: float = 0


@dataclass
class SF424ParticipantSupport:
    """Participant/trainee support for SF424 R&R Section E."""
    tuition_fees: float = 0
    stipends: float = 0
    travel: float = 0
    subsistence: float = 0
    other: float = 0
    num_participants: int = 0


@dataclass
class SF424OtherDirect:
    """Other direct costs for SF424 R&R Section F."""
    materials_supplies: float = 0
    publication_costs: float = 0
    consultant_services: float = 0
    adp_computer_services: float = 0   # Cloud computing goes here
    subawards: float = 0
    equipment_rental: float = 0
    alterations_renovations: float = 0
    # Up to 3 "other" line items (rows 19-21)
    other_items: List[tuple] = field(default_factory=list)
    # Each tuple: (description, amount)


@dataclass
class SF424IndirectCosts:
    """Indirect costs for SF424 R&R Section H."""
    # Up to 4 indirect cost entries
    entries: List[Dict[str, Any]] = field(default_factory=list)
    # Each dict: {"type": str, "rate": float, "base": float, "amount": float}
    cognizant_agency: str = ""


@dataclass
class SF424BudgetPeriod:
    """Complete budget data for one SF424 R&R budget period."""
    organization_name: str = ""
    org_duns: str = ""
    start_date: str = ""
    end_date: str = ""
    budget_period: int = 1

    senior_personnel: List[SF424SeniorPerson] = field(default_factory=list)
    other_personnel: SF424OtherPersonnel = field(
        default_factory=SF424OtherPersonnel)
    equipment: SF424Equipment = field(default_factory=SF424Equipment)
    travel: SF424Travel = field(default_factory=SF424Travel)
    participant_support: SF424ParticipantSupport = field(
        default_factory=SF424ParticipantSupport)
    other_direct: SF424OtherDirect = field(default_factory=SF424OtherDirect)
    indirect_costs: SF424IndirectCosts = field(
        default_factory=SF424IndirectCosts)

    # Computed totals — all must be set by Python code
    total_senior: float = 0
    total_other_personnel: float = 0
    total_salary_wages_fringe: float = 0
    total_equipment: float = 0
    total_travel: float = 0
    total_participant_support: float = 0
    total_other_direct: float = 0
    total_direct_costs: float = 0
    total_indirect_costs: float = 0
    total_direct_and_indirect: float = 0
    total_other_personnel_count: int = 0


# === POPULATION FUNCTION ===

def populate_sf424(template_path: str, output_path: str,
                   budget: SF424BudgetPeriod) -> Dict[str, Any]:
    """
    Populate the SF424 R&R Budget template for a single budget period.

    For Genesis Phase I, this populates Budget Period 1 only, then mirrors
    the values to the Cumulative sheet.

    All values in the budget object must be pre-computed in Python.
    This function only writes values — it performs no arithmetic.

    Args:
        template_path: Path to the blank SF424 R&R template
        output_path: Path for the populated output file
        budget: SF424BudgetPeriod with all values pre-computed

    Returns:
        Dict with cells_written count, warnings, and success status

    IMPORTANT: The SF424 template contains formulas in total/subtotal cells.
    This function writes ONLY to data-entry cells and lets the template
    formulas compute totals when the file is opened in Excel.

    Formula cells that must NOT be overwritten:
      A-B sheet: P12-P19 (=N+O), P21 (sum senior), P27-P36 (=N+O),
                 P37 (sum other), P39 (sum A+B)
      C-E sheet: J25 (sum equip), J34 (sum travel), J44 (sum participant),
                 J47 (sum C-E)
      F-K sheet: J22 (sum other direct), J26 (total direct cross-sheet),
                 J31-J34 (=H*G indirect), J35 (sum indirect),
                 J41 (total direct+indirect)
    """
    shutil.copy(template_path, output_path)
    wb = load_workbook(output_path)

    cells_written = []
    warnings = []

    # --- Sheet: Budget 1 A-B ---
    ws_ab = wb['Budget 1 A-B']

    # Header info
    ws_ab['D2'] = budget.org_duns
    ws_ab['A6'] = f'*Name of Organization: {budget.organization_name}'
    ws_ab['A8'] = f'*Start Date: {budget.start_date}'
    ws_ab['D8'] = f'*End Date: {budget.end_date}'
    ws_ab['H8'] = budget.budget_period
    cells_written.extend(['D2', 'A6', 'A8', 'D8', 'H8'])

    # Section A: Senior/Key Person (rows 12-19, up to 8 people)
    # P column has formulas =SUM(N+O), so write to N and O only
    for i, person in enumerate(budget.senior_personnel[:8]):
        row = 12 + i
        if person.prefix:
            ws_ab[f'B{row}'] = person.prefix
        ws_ab[f'C{row}'] = person.first_name
        if person.middle_name:
            ws_ab[f'E{row}'] = person.middle_name
        ws_ab[f'G{row}'] = person.last_name
        if person.suffix:
            ws_ab[f'H{row}'] = person.suffix
        ws_ab[f'I{row}'] = person.project_role
        ws_ab[f'J{row}'] = person.base_salary
        if person.cal_months > 0:
            ws_ab[f'K{row}'] = person.cal_months
        if person.acad_months > 0:
            ws_ab[f'L{row}'] = person.acad_months
        if person.sum_months > 0:
            ws_ab[f'M{row}'] = person.sum_months
        ws_ab[f'N{row}'] = person.requested_salary
        ws_ab[f'O{row}'] = person.fringe_benefits
        # P{row} is a formula =SUM(N{row}+O{row}) — do NOT write
        cells_written.append(f'A-B row {row}')

    # If more than 8 senior personnel, note overflow
    if len(budget.senior_personnel) > 8:
        overflow_total = sum(
            p.funds_requested for p in budget.senior_personnel[8:])
        ws_ab['P20'] = overflow_total
        warnings.append(
            f"{len(budget.senior_personnel) - 8} additional senior personnel "
            f"exceed SF424 row limit. Total overflow: ${overflow_total:,.0f}. "
            f"Use 'Additional Senior Key Persons' attachment.")

    # P21 is formula =SUM(P12:P20) — do NOT write

    # Section B: Other Personnel
    # P column has formulas =SUM(N:O), so write to N and O only
    op = budget.other_personnel

    # Row 27: Post Doctoral Associates
    if op.postdoc_count > 0:
        ws_ab['A27'] = op.postdoc_count
        ws_ab['K27'] = op.postdoc_cal_months
        ws_ab['L27'] = op.postdoc_acad_months
        ws_ab['M27'] = op.postdoc_sum_months
        ws_ab['N27'] = op.postdoc_salary
        ws_ab['O27'] = op.postdoc_fringe
        # P27 is formula — do NOT write

    # Row 28: Graduate Students
    if op.grad_count > 0:
        ws_ab['A28'] = op.grad_count
        ws_ab['K28'] = op.grad_cal_months
        ws_ab['L28'] = op.grad_acad_months
        ws_ab['M28'] = op.grad_sum_months
        ws_ab['N28'] = op.grad_salary
        ws_ab['O28'] = op.grad_fringe
        # P28 is formula — do NOT write

    # Row 29: Undergraduate Students
    if op.undergrad_count > 0:
        ws_ab['A29'] = op.undergrad_count
        ws_ab['N29'] = op.undergrad_salary
        ws_ab['O29'] = op.undergrad_fringe
        # P29 is formula — do NOT write

    # Row 30: Secretarial/Clerical
    if op.secretarial_count > 0:
        ws_ab['A30'] = op.secretarial_count
        ws_ab['N30'] = op.secretarial_salary
        ws_ab['O30'] = op.secretarial_fringe
        # P30 is formula — do NOT write

    # Rows 31-36: Other categories
    for idx, cat in enumerate(op.other_categories[:6]):
        row = 31 + idx
        if cat.get('count', 0) > 0:
            ws_ab[f'A{row}'] = cat['count']
        ws_ab[f'C{row}'] = cat.get('label', '')
        ws_ab[f'N{row}'] = cat.get('salary', 0)
        ws_ab[f'O{row}'] = cat.get('fringe', 0)
        # P{row} is formula — do NOT write

    # A37 (total count) is data entry
    ws_ab['A37'] = budget.total_other_personnel_count
    # P37, P39 are formulas — do NOT write
    cells_written.append('A37')

    # --- Sheet: Budget 1 C-E ---
    ws_ce = wb['Budget 1 C-E']

    # Header info (mirrors A-B header)
    ws_ce['D2'] = budget.org_duns
    ws_ce['D6'] = budget.organization_name
    ws_ce['C8'] = budget.start_date
    ws_ce['E8'] = budget.end_date
    ws_ce['H8'] = budget.budget_period

    # Section C: Equipment (rows 14-23, up to 10 items)
    for i, (desc, cost) in enumerate(budget.equipment.items[:10]):
        row = 14 + i
        ws_ce[f'B{row}'] = desc
        ws_ce[f'J{row}'] = cost
        cells_written.append(f'C-E equipment row {row}')

    if len(budget.equipment.items) > 10:
        overflow_total = sum(cost for _, cost in budget.equipment.items[10:])
        ws_ce['J24'] = overflow_total
        warnings.append(
            f"{len(budget.equipment.items) - 10} equipment items exceed "
            f"SF424 row limit. Use 'Additional Equipment' attachment.")

    # J25 is formula =SUM(J14:K24) — do NOT write

    # Section D: Travel (data entry cells)
    ws_ce['J32'] = budget.travel.domestic
    ws_ce['J33'] = budget.travel.foreign
    # J34 is formula =SUM(J32:K33) — do NOT write
    cells_written.extend(['J32', 'J33'])

    # Section E: Participant/Trainee Support (data entry cells)
    ps = budget.participant_support
    ws_ce['J38'] = ps.tuition_fees
    ws_ce['J39'] = ps.stipends
    ws_ce['J40'] = ps.travel
    ws_ce['J41'] = ps.subsistence
    ws_ce['J42'] = ps.other
    ws_ce['A44'] = ps.num_participants  # A44 is data entry (not D44 — merged)
    # J44 is formula =SUM(J38:K42) — do NOT write
    # J47 is formula — do NOT write
    cells_written.extend(['J38', 'J39', 'J40', 'J41', 'J42', 'A44'])

    # --- Sheet: Budget 1 F-K ---
    ws_fk = wb['Budget 1 F-K']

    # Header info
    ws_fk['D2'] = budget.org_duns
    ws_fk['D6'] = budget.organization_name
    ws_fk['C8'] = budget.start_date
    ws_fk['E8'] = budget.end_date
    ws_fk['H8'] = budget.budget_period

    # Section F: Other Direct Costs (data entry cells)
    od = budget.other_direct
    ws_fk['J12'] = od.materials_supplies
    ws_fk['J13'] = od.publication_costs
    ws_fk['J14'] = od.consultant_services
    ws_fk['J15'] = od.adp_computer_services
    ws_fk['J16'] = od.subawards
    ws_fk['J17'] = od.equipment_rental
    ws_fk['J18'] = od.alterations_renovations

    # Other items (rows 19-21, data entry)
    for i, (desc, amount) in enumerate(od.other_items[:3]):
        row = 19 + i
        ws_fk[f'B{row}'] = desc
        ws_fk[f'J{row}'] = amount
        cells_written.append(f'F-K other row {row}')

    # J22 is formula =SUM(J12:J21) — do NOT write
    # J26 is formula (cross-sheet total direct) — do NOT write
    cells_written.extend(
        ['J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18'])

    # Section H: Indirect Costs
    # J31-J34 are formulas =SUM(H*G), so write to B (type), G (rate), H (base)
    ic = budget.indirect_costs
    for i, entry in enumerate(ic.entries[:4]):
        row = 31 + i
        ws_fk[f'B{row}'] = entry.get('type', '')
        ws_fk[f'G{row}'] = entry.get('rate', 0)
        ws_fk[f'H{row}'] = entry.get('base', 0)
        # J{row} is formula =SUM(H{row}*G{row}) — do NOT write
        cells_written.append(f'F-K indirect row {row}')

    # J35 is formula =SUM(J31:J34) — do NOT write

    # Cognizant agency
    if ic.cognizant_agency:
        ws_fk['A38'] = ic.cognizant_agency

    # J41 is formula =SUM(J26+J35) — do NOT write
    # J44 (Fee) is data entry
    ws_fk['J44'] = 0

    # --- Sheet: Cumulative ---
    # The Cumulative sheet does NOT have cross-sheet formulas, so we must
    # write all values directly. For Phase I (single period), this mirrors
    # the Budget Period 1 values.
    ws_cum = wb['Cumulative']

    ws_cum['A1'] = budget.organization_name
    ws_cum['E2'] = budget.total_senior               # Section A
    ws_cum['E3'] = budget.total_other_personnel       # Section B
    ws_cum['B4'] = budget.total_other_personnel_count  # Total # Other
    ws_cum['E5'] = budget.total_salary_wages_fringe   # Total A+B
    ws_cum['E6'] = budget.total_equipment             # Section C
    ws_cum['E7'] = budget.travel.domestic + budget.travel.foreign  # Section D
    ws_cum['B8'] = budget.travel.domestic             # Domestic
    ws_cum['B9'] = budget.travel.foreign              # Foreign
    ws_cum['E10'] = budget.total_participant_support   # Section E
    ws_cum['B11'] = ps.tuition_fees
    ws_cum['B12'] = ps.stipends
    ws_cum['B13'] = ps.travel
    ws_cum['B14'] = ps.subsistence
    ws_cum['B15'] = ps.other
    ws_cum['B16'] = ps.num_participants
    ws_cum['E17'] = budget.total_other_direct         # Section F
    ws_cum['B18'] = od.materials_supplies
    ws_cum['B19'] = od.publication_costs
    ws_cum['B20'] = od.consultant_services
    ws_cum['B21'] = od.adp_computer_services
    ws_cum['B22'] = od.subawards
    ws_cum['B23'] = od.equipment_rental
    ws_cum['B24'] = od.alterations_renovations

    # Other items for cumulative (rows 25-27)
    for i, (desc, amount) in enumerate(od.other_items[:3]):
        ws_cum[f'B{25 + i}'] = amount

    ws_cum['E28'] = budget.total_direct_costs         # Section G
    ws_cum['E29'] = budget.total_indirect_costs        # Section H
    ws_cum['E30'] = budget.total_direct_and_indirect   # Section I
    ws_cum['E31'] = 0                                  # Section J (Fee)

    cells_written.append('Cumulative sheet populated')

    # Save
    wb.save(output_path)

    return {
        'success': True,
        'cells_written_count': len(cells_written),
        'warnings': warnings,
        'output_path': output_path
    }


def compute_mtdc_base(
    total_salaries_wages_fringe: float,
    materials_supplies: float,
    publication_costs: float,
    consultant_services: float,
    adp_computer_services: float,
    equipment_rental: float,
    alterations_renovations: float,
    other_direct_items_subject: float,
    travel_domestic: float,
    travel_foreign: float,
    human_subjects: float,
    purchased_services: float,
    subaward_mtdc_portions: float,
    # Items EXCLUDED from MTDC:
    equipment_total: float,
    participant_support_total: float,
    tuition_remitted: float,
    subaward_excess: float
) -> Dict[str, float]:
    """
    Compute the MTDC base and F&A-excluded amounts.

    The MTDC base includes all direct costs EXCEPT:
    - Equipment
    - Participant/trainee support costs
    - Tuition (remitted)
    - Subaward amounts above $25K per sub

    Args:
        All individual cost categories as computed in Python.
        subaward_mtdc_portions: sum of first $25K of each subaward
        subaward_excess: sum of amounts above $25K per subaward

    Returns:
        Dict with 'mtdc_base', 'excluded_from_mtdc', and 'total_direct'
    """
    # Costs included in MTDC
    mtdc_base = (
        total_salaries_wages_fringe
        + materials_supplies
        + publication_costs
        + consultant_services
        + adp_computer_services
        + equipment_rental
        + alterations_renovations
        + other_direct_items_subject
        + travel_domestic
        + travel_foreign
        + human_subjects
        + purchased_services
        + subaward_mtdc_portions
    )

    # Costs excluded from MTDC
    excluded = (
        equipment_total
        + participant_support_total
        + tuition_remitted
        + subaward_excess
    )

    total_direct = mtdc_base + excluded

    return {
        'mtdc_base': mtdc_base,
        'excluded_from_mtdc': excluded,
        'total_direct': total_direct
    }


def compute_fa_amount(mtdc_base: float, fa_rate: float) -> float:
    """
    Compute the F&A (indirect cost) amount.

    Args:
        mtdc_base: The modified total direct cost base
        fa_rate: The F&A rate as a decimal (e.g., 0.495 for 49.5%)

    Returns:
        The F&A dollar amount
    """
    return mtdc_base * fa_rate
