---
name: su-osp-budget
description: Syracuse University OSP Budget Template population for sponsored research proposals. Use when PIs need to create, populate, or modify the OSP Budget Workbook (FY26) for federal or non-federal grants. Handles personnel (senior/other), non-personnel costs (equipment, travel, participant support, materials, consultants, subawards, tuition, human subjects), F&A rates, fringe rate lookups, and generates Excel workbooks. Self-contained — includes all rate data, policy references, and calculation functions with no external skill dependencies. Requires Claude Opus 4.5+ and the xlsx skill.
---

# SU OSP Budget Template Skill

> **⚠️ CRITICAL: Complete File Reading Required**
> 
> The `view` tool may truncate large files, showing only the beginning and end while omitting the middle. Before proceeding with any budget work:
> 1. Check if any file output shows "truncated lines X-Y" 
> 2. If truncated, use `view` with `view_range` parameter to read the missing sections
> 3. Do NOT proceed until you have read the complete contents of this SKILL.md and any reference files you need
> 
> This applies to all files in this skill, especially `references/safe_cells.md` which contains critical information about which cells can be written to.

## Version Information

| Field | Value |
|-------|-------|
| **Version** | 2.2 |
| **Created** | November 26, 2025 |
| **Last Updated** | March 13, 2026 |

### Version History
- **2.2** (Mar 13, 2026): Added explicit GitHub repository update instructions to versioning workflow. No functional changes to budget logic.
- **2.1** (Mar 13, 2026): Updated OSP Budget Template to 1/30/2026 version. NIH salary cap updated to $228,000 (effective January 1, 2026, per NOT-OD-26-034). Removed personally identifying information and research-domain-specific references from examples. All example names replaced with generic placeholders.
- **2.0** (Feb 9, 2026): MAJOR — Self-contained release. Incorporated all rate data, policy references, calculation scripts, and lookup functions from su-research-budget and su-chart-of-accounts. No external skill dependencies (except xlsx). Added rate_lookup.py and budget_calculator.py to scripts/. Added fringe rate data files, F&A rate history, and all policy reference files to skill. Updated all documentation to reference internal files only.
- **1.3** (Nov 26, 2025): CRITICAL FIX — Added mandatory su-research-budget consultation requirement; removed inline fringe rate values to prevent stale data; added explicit rate lookup workflow; fixed error where faculty summer fringe was assumed rather than looked up, causing ~$7K/year overestimate
- **1.2** (Nov 26, 2025): Added OSP Budget Template to assets; skill is now self-contained
- **1.1** (Nov 26, 2025): Critical warning about file truncation; models must verify complete file reading before proceeding
- **1.0** (Nov 26, 2025): Initial release with complete Personnel and Non-personnel support

### Versioning Instructions for Skill Updates

When this skill is updated and rebuilt using the skill-creator:
1. **Auto-increment the minor version**: 2.2 → 2.3 → 2.4 → 2.5, etc.
2. **Update "Last Updated" date** to the current date
3. **Add entry to Version History** with brief description of changes
4. **Major version updates** (e.g., 2.x → 3.0) require explicit user instruction

### GitHub Repository Update Workflow

This skill is maintained in the `duncan-brown/research-skills` GitHub repository. When a new version is built, the repository must be updated following this procedure:

**Repository structure:**
```
research-skills/
├── README.md
├── su-osp-budget/           # Source files (git-tracked with full history)
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   └── scripts/
└── dist/
    └── su-osp-budget/       # Packaged .skill files by version
        ├── v2.0/
        │   └── su-osp-budget.skill
        ├── v2.1/
        │   └── su-osp-budget.skill
        └── v{X.Y}/
            └── su-osp-budget.skill
```

**Step 1: Commit source file changes**

Push all modified source files under `su-osp-budget/` to the `main` branch. The commit message should summarize the changes, e.g.:
```
v2.3: Brief description of what changed
```

**Step 2: Package the .skill file**

Use the skill-creator's `package_skill.py` script (or equivalent) to create the `.skill` zip file from the source directory.

**Step 3: Commit the packaged .skill file**

Push the `.skill` file to `dist/su-osp-budget/v{X.Y}/su-osp-budget.skill` with a commit message like:
```
added binary package for su-osp-budget.skill v{X.Y}
```

**Step 4: Tag the release**

Create a lightweight git tag on the source commit (from Step 1, not the dist commit) named:
```
su-osp-budget-v{X.Y}
```

The tag naming convention is `{skill-name}-v{version}` to support multiple skills in the same repository without tag collisions.

**Privacy reminder:** Before committing, verify that no personally identifying information (real names, salaries, or identifying research domain references) has been introduced during development. Run a grep scan across all `.md` and `.py` files.

---

## Prerequisites Check

**BEFORE using this skill, Claude MUST verify the following:**

### 1. Model Requirement
This skill requires **Claude Opus 4.5 or higher**. The complex natural language interpretation, policy calculations, and bespoke code generation require the most capable model.

If running on a lesser model (Sonnet, Haiku), inform the user:
> "This skill requires Claude Opus 4.5 for reliable execution. Please switch to Opus 4.5 in your model settings before proceeding."

### 2. Required Skills Check
Run this check at the start of any budget work:

```bash
# Check for required skills — only xlsx is external now
ls -d /mnt/skills/public/xlsx 2>/dev/null && echo "✓ xlsx found" || echo "✗ MISSING: xlsx"
```

### Required Skills Summary

| Skill | Location | Purpose |
|-------|----------|---------|
| `xlsx` | `/mnt/skills/public/xlsx` | Excel file creation and manipulation |

**All rate data, policy references, and calculation functions are included within this skill.**

---

## Rate Lookups (Self-Contained)

### Fringe Rate & F&A Rate Data

All rate data is stored in the skill's `assets/` directory:

| File | Content |
|------|---------|
| `assets/fringe_rates_by_account_fy2025.xlsx` | Account-level fringe rates for FY2025 |
| `assets/fringe_rates_by_account_fy2026.xlsx` | Account-level fringe rates for FY2026 |
| `assets/fringe_rate_history.xlsx` | Historical fringe rates from rate agreements |
| `assets/fa_rate_history.xlsx` | Historical F&A rates from rate agreements |

### Rate Lookup Scripts

Rate lookup functions are in `scripts/rate_lookup.py`:

```python
import sys
sys.path.insert(0, '/path/to/su-osp-budget/scripts')
from rate_lookup import get_fiscal_year, get_fa_rate, get_fringe_rate, get_fringe_rate_nonfederal

# Determine current fiscal year
fy = get_fiscal_year()  # Returns 2026 for dates July 1, 2025 - June 30, 2026

# F&A rate lookup
fa_rate = get_fa_rate(2026, "research", "on-campus")  # 0.495 (49.5%)

# Fringe rate lookup by account code and fund
faculty_ay = get_fringe_rate("500011", "13", 2026)     # 0.295 (29.5%)
faculty_sum = get_fringe_rate("530011", "13", 2026)    # 0.158 (15.8%)
ga_federal = get_fringe_rate("503259", "13", 2026)     # 0.108 (10.8%)
postdoc = get_fringe_rate("513001", "13", 2026)        # 0.295 (29.5%)

# Non-federal GA fringe (includes tuition remission)
ga_nonfed = get_fringe_rate_nonfederal("503259", 2026) # 0.55 (55.0%)
```

### Budget Calculator Scripts

Budget calculation functions are in `scripts/budget_calculator.py`:

```python
from budget_calculator import (
    calculate_faculty_monthly_rate,
    calculate_fully_loaded_cost,
    calculate_equipment_cost,
    calculate_subaward_cost,
    calculate_course_buyout,
    apply_escalation,
    calculate_nih_capped_salary
)
```

### Quick Rate Reference (FY2026 — verify against data files)

**F&A Rates (MTDC base, per DHHS agreement 06/04/2024):**

| Activity | Location | Rate |
|----------|----------|------|
| Research | On-Campus | 49.50% |
| Training/Instruction | On-Campus | 34.00% |
| Other Sponsored Activities | On-Campus | 35.00% |
| All Programs | Off-Campus | 26.00% |

**Common Fringe Rates — Sponsored Federal (Fund 13, FY2026):**

| Account | Description | Rate |
|---------|-------------|------|
| 500011 | Faculty (Academic Year) | 29.5% |
| 500013 | Research Faculty FT | 29.5% |
| 530011 | Faculty - Summer | 15.8% |
| 503259 | Graduate Assistants (Federal) | 10.8% |
| 503259 | Graduate Assistants (Non-Federal) | 55.0% |
| 536259 | Grad Assistant - Summer (Federal) | 0.0% |
| 536259 | Grad Assistant - Summer (Non-Federal) | 55.0% |
| 513001 | Post Doctoral Scholar | 29.5% |
| 513021 | Exempt Staff | 29.5% |
| 543021 | Casual/Temporary | 7.9% |
| 520514 | PT Faculty-Union (Modified) | 12.8% |
| 549979 | Extra Service/Overload | 7.9% |

**Common Fringe Rates — Unrestricted (Fund 11, FY2026):**

| Account | Description | Rate |
|---------|-------------|------|
| 500011 | Faculty | 37.5% |
| 530011 | Faculty - Summer | 25.3% |
| 503259 | Graduate Assistants | 22.1% |
| 513001 | Postdoc | 37.5% |

> **IMPORTANT:** Always use `rate_lookup.py` for actual calculations — the tables above are for quick reference only and must be verified against the data files for the appropriate fiscal year.

### Updating Rate Data

To update rates for a new fiscal year:
1. Obtain new fringe rate data file from Comptroller
2. Name as `fringe_rates_by_account_fyYYYY.xlsx` (matching existing format)
3. Place in `assets/` directory
4. The `rate_lookup.py` script auto-selects by fiscal year parameter

---

## Overview

This skill helps Syracuse University PIs populate the OSP Budget Template (FY26 version) for sponsored research proposals. It translates natural language budget requests into correct cell values and generates populated Excel workbooks.

## Key Concepts

### Syracuse University Federally Negotiated Thresholds

**IMPORTANT:** Syracuse University operates under a federally negotiated indirect cost rate agreement (DHHS, dated June 4, 2024). These thresholds are CORRECT for Syracuse and may differ from general 2 CFR 200 definitions.

**Equipment Threshold: $5,000** (per SU institutional capitalization policy)
**Subaward MTDC Threshold: $25,000** (per SU NICRA, not the revised $50,000 in 2 CFR 200)

### Sponsor Types

| Dropdown Value | Meaning | GA Fringe Rate |
|----------------|---------|----------------|
| Federal - NIH | NIH grants only | Look up in rate_lookup.py |
| Federal - Other | NSF, DOE, DOD, NASA, other federal | Look up in rate_lookup.py |
| Fnd/Prof Soc | **All non-federal** (foundations, industry, state) | Look up in rate_lookup.py |

**For graduate assistants, federal vs. non-federal matters significantly:**
- Federal: 10.8% fringe (FY26) — use `get_fringe_rate("503259", "13", 2026)`
- Non-federal: 55.0% fringe (includes tuition remission) — use `get_fringe_rate_nonfederal("503259", 2026)`

### Appointment Types & Month Bases

| Personnel Type | Month Base | Notes |
|----------------|------------|-------|
| Faculty (Academic) | 8.5 months | Use Acad Months + Sum Months |
| Faculty (Calendar) | 12 months | Use Cal Months |
| Graduate Assistants | 9 months | 18 semi-monthly pays (NOT 8.5) |
| Postdocs/Staff | 12 months | Use Cal Months |

### Key Policy Rules

1. **NSF Two-Month Rule**: Senior personnel limited to 2 months salary per year (unless PO approves exception). See `references/nsf_policies.md`.
2. **NIH Salary Cap**: $228,000 (calendar) / ~$161,500 (academic equivalent). See `references/nih_policies.md`.
3. **Course Buyout**: 15% of academic year = 1.275 months per course. See `references/salary_policies.md`.
4. **Summer Limit**: Maximum 3.5 months from ALL sources
5. **Cost Sharing**: Requires SEPARATE OSP Budget Template workbook
6. **Escalation Rate**: Salary escalates 3% per year (cell D5, protected). Note: Tuition escalates at 8.16% — see `references/tuition_policies.md`.

### Federal vs. Non-Federal Sponsor Identification

See `references/federal_agencies.md` for a comprehensive list.

**Federal sponsors include:** NSF, NIH, DOD, DOE, NASA, USDA, EPA, NEH, NEA, and all cabinet departments/independent federal agencies.

**Non-federal sponsors:** Foundations, non-profits, corporations, state governments (using own funds), foreign governments.

**Federal pass-through awards:** If a non-federal entity distributes federal funds and the award references 2 CFR 200 or includes a FAIN, treat as federal for fringe rate purposes.

## Workbook Structure

### Personnel Yr 1 (Data Entry Sheet)

**Project Info (Row 5):**
- I5: Start Date
- K5: Project Duration (1-5 years)
- O5: Sponsor Type
- D5: Escalation Rate (3%, protected - read only)

**Senior Personnel (Rows 7-14, 20-34):**
- Row 7 must be PI
- Columns: Name (B-F), Role (G), Designation (H), Base Salary (I), Cal/Acad/Sum Months (J-L)
- Columns M-O are formulas (DO NOT WRITE)
- Column P: Justification text (ALWAYS populate)

**Grad Fringe Type (I43):**
- Must be set BEFORE entering Graduate Assistants
- Should match Sponsor Type (O5)

**Other Personnel Detail (Rows 53-72):**
- Columns: Name (B-F), Role (G), Cal/Acad/Sum Months (J-L), Requested Salary (M)
- Note: Other Personnel salary is entered directly in M (unlike Senior Personnel)
- Columns N-O are formulas (DO NOT WRITE)
- Column P: Justification text (ALWAYS populate)

### Personnel Yr 2-5 (Auto-Calculated with Modifications)

- Values reference previous year with 3% escalation (from D5)
- Write to these sheets when:
  - Effort changes in out years
  - Personnel added/removed in out years
  - Need to override escalation
- **Column P required for ALL rows with salary:**
  - If unchanged: "Effort same as prior year. Salary escalated 3% per cell D5."
  - If modified: Explain the change and calculation

### Row Assignment Rules

1. **One row per person** - even for TBD positions
2. Use descriptive TBD names: "TBD Hourly Undergraduate", "TBD New Graduate Student"
3. Keep people on their assigned row across all years
4. Zero out rows when people leave (don't delete)

## Column P Justification Requirements

**EVERY row with salary must have a justification in column P.**

### Senior Personnel Justifications (explain effort):
- Course buyouts: "1 course buyout at 15% of academic year = 1.275 academic months"
- Summer months: "Plus 0.725 summer months. Total: 2.000 months."
- PO exceptions: "PO exception: 12 months approved for full-time research faculty"

### Other Personnel Justifications (explain salary calculation):
- Hourly: "$20/hr × 5 hrs/wk × 16 weeks = 80 hours = $1,600"
- Grad students: "Full AY stipend $28,750 + 2 summer mo × $3,194.44/mo = $6,389. Total: $35,139"
- Salaried: "0.5 FTE × $65,000 annual = $32,500"

### Out-Year Justifications:
- Escalation only: "Effort same as prior year. Salary escalated 3% per cell D5."
- Modifications: Explain the change and new calculation

## Technical Requirements

### openpyxl External Link Corruption

openpyxl corrupts external link files by stripping XML namespaces. After saving with openpyxl, MUST call:
```python
preserve_external_links(template_path, output_path)
```

Without this fix, Excel reports: "We found a problem with some content"

### Non-Linear Budget Building

PIs build budgets iteratively ("oh wait, add this..."). The skill uses:
- `BudgetState` - Complete budget state that can be modified
- `PersonnelChange` - Tracks intent, not just cell values
- Changes are additive and can be reordered

### Common Calculation Mistakes

**Mistake 1: Using a single fringe rate for all faculty effort**

A PI with academic-year buyout AND summer salary requires TWO different fringe calculations because they use different account codes:
- Course buyout (academic months): Account 500011 → 29.5% (FY26 sponsored)
- Summer salary (summer months): Account 530011 → 15.8% (FY26 sponsored)

**Mistake 2: Assuming fringe rates without lookup**

Never assume a fringe rate based on general knowledge or previous budgets. Rates change annually and vary by:
- Personnel type (faculty, postdoc, GA, staff, temporary)
- Payment period (academic year vs. summer)
- Funding source (sponsored vs. unrestricted vs. gift)
- Sponsor type (federal vs. non-federal, for GAs)

**Always use rate_lookup.py for current rates.**

## Architecture

```python
# Core data classes (in budget_population.py)
ProjectInfo          # Start date, duration, sponsor type
SeniorPerson         # PI, Co-PI, etc. with effort details
OtherPerson          # Postdocs, grads, staff with salary details
PersonnelChange      # Out-year modifications (remove, modify, add)
BudgetState          # Complete budget state

# Key functions (in budget_population.py)
populate_budget()           # Year 1 only
apply_out_year_changes()    # Years 2-5 modifications
populate_budget_full()      # Complete budget generation
preserve_external_links()   # Fix openpyxl corruption

# Rate lookups (in rate_lookup.py)
get_fiscal_year()           # SU fiscal year from date
get_fa_rate()               # F&A rate by activity/location/year
get_fringe_rate()           # Fringe rate by account/fund/year
get_fringe_rate_nonfederal()# Non-federal GA fringe rate

# Budget calculations (in budget_calculator.py)
calculate_faculty_monthly_rate()   # AY salary ÷ 8.5
calculate_fully_loaded_cost()      # salary + fringe + F&A
calculate_equipment_cost()         # Equipment vs supplies
calculate_subaward_cost()          # $25K MTDC threshold
calculate_course_buyout()          # 15% per course
apply_escalation()                 # 3% annual
calculate_nih_capped_salary()      # NIH salary cap compliance
```

## Usage Example

First, copy the template and set up script paths:

```bash
cp /path/to/su-osp-budget/assets/OSP-Budget-Template-FY-26-Web.xlsx /home/claude/
```

```python
import sys
sys.path.insert(0, '/path/to/su-osp-budget/scripts')

from rate_lookup import get_fa_rate, get_fringe_rate, get_fringe_rate_nonfederal
from budget_population import (
    BudgetState, ProjectInfo, SeniorPerson, OtherPerson, PersonnelChange,
    SponsorType, Designation, SeniorRole, OtherRole,
    populate_budget_full
)

# Look up current rates
fa_rate = get_fa_rate(2026, "research", "on-campus")          # 0.495
faculty_ay_fringe = get_fringe_rate("500011", "13", 2026)     # 0.295
faculty_sum_fringe = get_fringe_rate("530011", "13", 2026)    # 0.158
ga_fringe_federal = get_fringe_rate("503259", "13", 2026)     # 0.108
postdoc_fringe = get_fringe_rate("513001", "13", 2026)        # 0.295

state = BudgetState(
    project_info=ProjectInfo(
        start_date="7/1/26",
        duration_years=3,
        sponsor_type=SponsorType.FEDERAL_OTHER
    ),
    year1_senior=[
        SeniorPerson(
            first_name="Jane",
            last_name="Smith",
            role=SeniorRole.PI,
            designation=Designation.TENURE_TRACK_ACAD_SUM,
            base_salary=100000,
            acad_months=1.275,
            sum_months=0.725,
            course_buyouts=1  # Auto-generates justification
        ),
    ],
    year1_other=[
        OtherPerson(
            first_name="TBD",
            last_name="Graduate Student",
            role=OtherRole.GRAD_ASSISTANT,
            acad_months=9,
            sum_months=2,
            requested_salary=35139,
            annual_stipend=28750,
            stipend_months_base=9  # Auto-generates justification
        ),
    ],
    grad_fringe_type=SponsorType.FEDERAL_OTHER
)

# Add out-year changes
state.add_change(PersonnelChange(
    description="Increase to 1 FTE in Y3",
    person_name="TBD Graduate Student",
    row=53,
    section="other",
    change_type="modify",
    effective_year=3,
    new_values={"J": 12, "M": 68959},
    justification="1.0 FTE × $68,959 = $68,959"
))

result = populate_budget_full(
    template_path='/home/claude/OSP-Budget-Template-FY-26-Web.xlsx',
    output_path='/home/claude/Budget-v1.xlsx',
    state=state
)
```

## Common Calculations

### Course Buyout
```
1 course = 15% of academic year = 15% × 8.5 months = 1.275 academic months
```

### Graduate Student Salary
```
FY26 minimum stipend = $28,750 (academic year, paid over 9 months)
Monthly rate = $28,750 ÷ 9 = $3,194.44
Full AY + 2 summer = $28,750 + ($3,194.44 × 2) = $35,139
```

### Graduate Student Stipend Minimums (Union Rates)
- 2025-2026: PhD $28,750 / Master's $24,250
- 2026-2027: PhD $29,500 / Master's $24,750
- 2027-2028: PhD $30,000 / Master's $25,000

### Salary Escalation
```
Year 2 = Year 1 × 1.03
Year 3 = Year 1 × 1.0609
Year N = Year 1 × (1.03)^(N-1)
```

### FTE to Calendar Months
```
0.25 FTE = 3 calendar months
0.5 FTE = 6 calendar months
1.0 FTE = 12 calendar months
```

### NYS Exempt Salary Thresholds (affects postdocs, research associates)
- **2025:** $60,405.80 annually (Syracuse region)
- **2026:** $62,353.20 annually (Syracuse region)

## College-Specific Tuition Policies

**Always ask which college when budgeting graduate students on federal grants.**

| College | Remission | PI Budgets (FY26) |
|---------|-----------|-------------------|
| Arts & Sciences | 100% | $0 |
| Engineering & CS | 50% | $18,135 |
| Education | 0% | $36,270 |
| Other Schools | Assume ECS model, confirm with Associate Dean for Research |

**Tuition rate:** $2,015/credit × 18 credits = $36,270/year
**Tuition escalation:** 8.16% per year (NOT 3% like salary)

See `references/tuition_policies.md` for complete policies.

## Files

### OSP Budget Template (Required)

**`assets/OSP-Budget-Template-FY-26-Web.xlsx`** — The official FY26 OSP Budget Template workbook. Copy this file to the working directory before populating.

```bash
cp /path/to/su-osp-budget/assets/OSP-Budget-Template-FY-26-Web.xlsx /home/claude/
```

### Rate Data Files

| File | Content | Update Frequency |
|------|---------|------------------|
| `assets/fringe_rates_by_account_fy2025.xlsx` | FY25 fringe by account/fund | Annual |
| `assets/fringe_rates_by_account_fy2026.xlsx` | FY26 fringe by account/fund | Annual |
| `assets/fringe_rate_history.xlsx` | Historical fringe from rate agreements | When renegotiated |
| `assets/fa_rate_history.xlsx` | Historical F&A rates | When renegotiated |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/budget_population.py` | Main budget population script (data classes, population functions) |
| `scripts/rate_lookup.py` | F&A and fringe rate lookup functions |
| `scripts/budget_calculator.py` | Fully loaded cost calculations, NIH cap, course buyout |

### Reference Files

**Budget Template:**
- `references/safe_cells.md` — Which cells can be written to, dropdown values
- `references/reading_budgets.md` — Guide for parsing completed OSP Budget workbooks

**Non-Personnel Cost Guidance:**
- `references/gsa_per_diem.md` — GSA per diem rates and M&IE calculations
- `references/participant_support.md` — Participant support cost rules (NSF vs NIH)
- `references/other_direct_costs.md` — Materials, supplies, equipment, publication costs
- `references/consultant_contractor_rental.md` — Consultant vs contractor distinction, rental/lease rules
- `references/tuition.md` — Graduate student tuition (Row 41 vs 42, college remission)
- `references/human_subjects.md` — Human subject payments (Row 43, IRB escrow, tax reporting)
- `references/subawards.md` — Subaward entry (Rows 70-88, $25K MTDC rule, collaborator budgets)

**SU OSP Guidance:**
- `references/osp_personnel_guidance.md` — SU OSP personnel/salary/fringe guidance
- `references/osp_non_personnel_guidance.md` — SU OSP non-personnel guidance

**Policy References:**
- `references/nih_policies.md` — NIH salary cap, NRSA, training grants, graduate student compensation cap
- `references/nsf_policies.md` — NSF two-month rule, cost sharing prohibition, participant support
- `references/salary_policies.md` — Appointments, buy-outs, thresholds, stipends, union rates
- `references/tuition_policies.md` — College tuition remission policies (critical!)
- `references/federal_agencies.md` — Federal sponsor identification list
- `references/budget_justification_templates.md` — Standard proposal text templates

### Per Diem Assets
- `assets/FY2026_PerDiemMasterRatesFile.xlsx` — Current FY GSA per diem rates
- `assets/FY2025_PerDiemMasterRatesFile.xlsx` — Previous FY GSA per diem rates
- `assets/FY2025PerDiemRatesHighlights.docx` — Per diem explanation
- `assets/FY_2025_MIE_Breakdown.docx` — M&IE breakdown by tier

### Images
- `assets/images/` — Dropdown screenshots, subaward detail section

## File Versioning

**IMPORTANT**: Increment the version number in the output filename every time you generate a new Excel file for the PI.

Example: `OSP-Budget-Template-v11.xlsx` → `OSP-Budget-Template-v12.xlsx`

## Non-Personnel Budget Structure

### ⚠️ FORMULA ROWS — DO NOT WRITE ⚠️

The following rows contain formulas and must NEVER be written to:

| Row | Content | Why |
|-----|---------|-----|
| 14 | Equipment subtotal | Formula row |
| 21 | Total Travel | Formula: =SUM(rows 19-20) |
| 29 | Total Participant Support | Formula: =SUM(rows 25-28) |
| 38 | Subawards Total | Formula from rows 70-88 |
| 48 | Other Direct Costs subtotal | Formula row |
| 52 | Total Direct Costs | Formula row |
| 57 | F&A Year 1 | **EXCEPTION: Columns B and C are DATA ENTRY for F&A Type/Rate** |
| 66 | F&A subtotal | Formula row |
| 71, 73, 75, 77, 79, 81, 83, 85, 87 | Subaward row totals | Formula rows |
| 90 | Subaward grand total | Formula row |

**Quick Reference:**
- **Travel**: Write to rows **19-20**, NOT row 21
- **Participant Support**: Write to rows **25-28**, NOT row 29
- **Subawards**: Row **38** is auto-calculated — NEVER write
- **Subaward Detail**: Write to **even rows only** (70, 72, 74, 76, 78, 80, 82, 84, 86, 88)
- **F&A Settings**: Write to rows **57-61 columns B and C only**

### Equipment (Rows 7-14)
- Items ≥$5,000 (total cost, can span multiple years)
- Include ALL costs: purchase + shipping + installation + renovation
- Excluded from MTDC (no F&A)

### Travel (Rows 19-20) — DATA ENTRY ROWS

**⚠️ CRITICAL: Write to rows 19-20 ONLY. Row 21 is a FORMULA row (Total Travel) - DO NOT WRITE!**

- Row 19: Domestic (NSF: includes Canada/Mexico) — DATA ENTRY ✓
- Row 20: Foreign — DATA ENTRY ✓
- Row 21: Total Travel — FORMULA ✗ (DO NOT WRITE)
- Use GSA per diem for M&IE calculations
- Column T: Store itemized breakdowns for justification

### Participant Support (Rows 25-28)
- Row 25: Stipends
- Row 26: Travel
- Row 27: Subsistence
- Row 28: Other (including Fees)
- **NSF**: Excluded from MTDC, allowed by default
- **NIH**: Only if in NOFO, excluded from MTDC
- **Other Federal**: Usually included in MTDC

### Other Direct Costs (Rows 34-47)
- Row 34: Materials and Supplies (<$5K items)
- Row 35: Publication Costs (APCs, page charges)
- Row 36: Consultant Services (expert individuals - requires OSP Consulting Agreement)
- Row 37: Purchased Services (vendor/contractor - uses Procurement, not OSP)
- Row 38: Subawards (FORMULA - don't write)
- Row 39: Rental/Lease (per 2 CFR 200.465, must be reasonable/comparable)
- Row 40: Alterations (**VPR approval required** - direct PI to vpr@syr.edu)
- Row 41: Tuition - Remitted (GRAs on project, per 2 CFR 200.466(b))
- Row 42: Tuition - Scholarship (training grants/fellowships, excluded from MTDC)
- Row 43: Human Subjects (research subjects, OSA escrows until IRB approval, included in MTDC)
- Rows 44-47: Other (customizable description in column B)

### F&A Rates (Rows 57-61)
- B57-B61: F&A Type per year (MTDC-Fed, MTDC-NonFed, TDC, SWFB)
- C57-C61: F&A Rate per year
- Default: Research - On Campus - 49.50%
- **CRITICAL: Rate must be SAME for all years** unless VPR approves (vpr@syr.edu)
- Even if SU's negotiated rate changes, use same rate ("actual rates at time charged")

### Subawards (Rows 70-88)
- **10 slots** on even rows: 70, 72, 74, 76, 78, 80, 82, 84, 86, 88
- **Collaborators provide their own budgets** with their F&A rates
- Enter: Institution name (B), Direct (H,J,L,N,P), Indirect (I,K,M,O,Q)
- Row 38 auto-populates from detail
- **$25K MTDC rule:** First $25K of each subaward in MTDC, remainder excluded
- Each subaward gets its own $25K (3 subawards = up to $75K in MTDC)
- Template handles F&A calculation automatically

## Key Policy Reminders

### Computing Devices
- Must be ≥75% project use for full charge
- General-purpose PI computers typically NOT allowable
- Project-specific workstations ARE allowable

### Tuition Rules
- **8.16% annual escalation** (NOT 3%)
- **College determines PI's budget** (see College-Specific Tuition Policies above)
- Row 41 = GRAs doing project work (2 CFR 200.466(b))
- Row 42 = Training grants/fellowships (2 CFR 200.466(a), Dean signature required)
- F41 dropdown is NOT useful - enter tuition directly
- Excluded from MTDC (no F&A)
- Don't use tuition for cost-sharing
- If tuition disallowed, can't use 55% GA fringe rate

### Alterations (Row 40)
- **Requires VPR approval** - do not budget without prior discussion
- If PI asks, direct them to contact: vpr@syr.edu

### Travel Rules
- US flag carriers required for federal (Open Skies exceptions)
- NSF: Canada/Mexico = domestic
- Conference hotel can exceed GSA rate (document it)

### Consultant vs Contractor
- **Consultant** (Row 36): Individual expert, advisory services, OSP agreement
- **Contractor** (Row 37): Vendor providing routine goods/services, Procurement process
- NSF: No daily rate limit (since FY06)
- Document reasonableness: customary fees, comparable services

### Rental/Lease
- Must be reasonable (comparable properties, market conditions)
- Arm's-length lease: rental payments allowable
- Less-than-arm's-length: limited to depreciation/maintenance/taxes/insurance
- Home office space: UNALLOWABLE

### Human Subjects (Row 43)
- Payments to research subjects (NOT participants in workshops/training)
- **OSA escrows funds until IRB approval** - critical timeline consideration
- **Included in MTDC** (F&A applies) - unlike Participant Support Costs
- Tax reporting: ≥$600/year to US person = 1099-MISC; non-resident aliens = 30% withholding
- IRB must approve incentive amounts to avoid undue influence

### Subawards
- PI gets budgets from collaborators using **their institutional rates**
- Enter Direct and Indirect as provided - don't recalculate
- **$25K rule:** Only first $25K of each subaward in MTDC
- Each subaward gets its own $25K (3 subawards = up to $75K in MTDC)
- Template handles F&A calculation automatically

### F&A Rates
- **Rate must be SAME for all years (Rows 57-61)**
- Different rates year-to-year requires **VPR approval** (vpr@syr.edu)
- Even if SU's negotiated rate changes mid-project, budget same rate throughout
- SU uses "actual rates in place at time will be charged" language
- Exception: Sponsor-capped rate (use MTDC-NonFed and enter custom %)

## Version History

- FY26: Current version, developed November 2025, self-contained release February 2026, template and NIH cap update March 2026
