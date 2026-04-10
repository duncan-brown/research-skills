---
name: oor-dashboards
description: Analyze Syracuse University Office of Research data from three DataInsights dashboards (Sponsored Proposals, Award Details, Detailed Sponsored Expenditures). Handles Tableau Excel exports with merged cells requiring forward-fill. Covers proposal tracking, award amounts with supplements, expenditure analysis by fiscal year, PI/department/sponsor queries, direct vs indirect cost analysis, burn rate calculations, and cross-referencing with faculty and Chart of Accounts data. Does NOT include General Ledger (GL) transaction parsing. ALWAYS use this skill when the user mentions Office of Research data, sponsored research analysis, proposal tracking, award analysis, research expenditures, DataInsights dashboards, or provides Excel files with names like Proposal_Details, Award_Details, or Expenditure_Details.
---

# Research Dashboards Analysis

## Version Information

| Field | Value |
|-------|-------|
| **Version** | 1.1 |
| **Created** | February 16, 2026 |
| **Last Updated** | April 10, 2026 |

### Version History
- **1.1** (Apr 10, 2026): Added Apache License 2.0. Added GitHub repository update workflow documentation. Enhanced description with explicit trigger phrases for reliable skill activation. Removed invalid metadata field from YAML frontmatter.
- **1.0** (Feb 16, 2026): Initial release. Consolidated sponsored-proposals (v1.4) and detailed-expenditures (v1.0) into a single self-contained skill covering three DataInsights dashboards: Sponsored Proposals, Award Details (Anticipated & Supplement Amounts), and Detailed Sponsored Expenditures. Excludes General Ledger parsing.

### Versioning Instructions for Skill Updates

When this skill is updated and rebuilt using the skill-creator:
1. **Auto-increment the minor version**: 1.1 -> 1.2 -> 1.3 -> 1.4, etc.
2. **Update "Last Updated" date** to the current date
3. **Add entry to Version History** with brief description of changes
4. **Major version updates** (e.g., 1.x -> 2.0) require explicit user instruction

### GitHub Repository Update Workflow

This skill is maintained in the `duncan-brown/research-skills` GitHub repository. When a new version is built, the repository must be updated following this procedure:

**Repository structure:**
```
research-skills/
├── README.md
├── oor-dashboards/              # Source files (git-tracked with full history)
│   ├── SKILL.md
│   ├── LICENSE
│   ├── references/
│   └── scripts/
└── dist/
    └── oor-dashboards/          # Packaged .skill files by version
        ├── v1.0/
        │   └── oor-dashboards.skill
        ├── v1.1/
        │   └── oor-dashboards.skill
        └── v{X.Y}/
            └── oor-dashboards.skill
```

**Step 1: Commit source file changes**

Push all modified source files under `oor-dashboards/` to the `main` branch. The commit message should summarize the changes, e.g.:
```
v1.1: Brief description of what changed
```

**Step 2: Package the .skill file**

Use the skill-creator's `package_skill.py` script (or equivalent) to create the `.skill` zip file from the source directory.

**Step 3: Commit the packaged .skill file**

Push the `.skill` file to `dist/oor-dashboards/v{X.Y}/oor-dashboards.skill` with a commit message like:
```
added binary package for oor-dashboards.skill v{X.Y}
```

**Step 4: Tag the release**

Create a lightweight git tag on the source commit (from Step 1, not the dist commit) named:
```
oor-dashboards-v{X.Y}
```

The tag naming convention is `{skill-name}-v{version}` to support multiple skills in the same repository without tag collisions.

**Privacy reminder:** Before committing, verify that no personally identifying information (real names, salaries, or identifying research domain references) has been introduced during development. Run a grep scan across all `.md` and `.py` files.

### License

This skill is licensed under the Apache License, Version 2.0. See the `LICENSE` file in the skill root directory.

---

**CRITICAL**: Read this entire skill file before proceeding with any analysis.

This skill analyzes Syracuse University Office of Research data exported from three DataInsights dashboards. It consolidates the former `sponsored-proposals` (v1.4) and `detailed-expenditures` (v1.0) skills into a single self-contained package.

## Data Sources

| Dashboard | URL | File Pattern | Content |
|-----------|-----|--------------|---------|
| Sponsored Proposals | [Details](https://datainsights.syr.edu/#/site/data/views/SponsoredProposalsatSyracuseUniversity/Details) | `YYYYMMDD_Proposal_Details.xlsx` | All proposals: Pending, Not Funded, Funded |
| Anticipated & Supplement Amounts | [Details](https://datainsights.syr.edu/#/site/data/views/OfficeofResearchAnticipatedandSupplementAmounts/Details) | `YYYYMMDD_Award_Details.xlsx` | Funded awards only with supplement tracking |
| Detailed Sponsored Expenditures | [Details](https://datainsights.syr.edu/#/site/data/views/OfficeofResearchDetailedExpenditures/Details) | `YYYYMMDD_Expenditure_Details_FYXX.xlsx` | Expenditures by fiscal year |

**Note**: This skill does NOT include General Ledger (GL) parsing. GL analysis requires the separate `sponsored-transactions` skill and users may not have GL access.

**Data Coverage**: Proposal and Award dashboards include FY2014 onwards only. Expenditure data is per fiscal year.

---

## Data Source Priority for Funded Awards

**For ALL funded awards, ALWAYS read Award Details first:**
- Award Details = Authoritative PeopleSoft live data (current PI, dates, sponsors, amounts, supplements, project-level detail)
- Proposal Details for funded awards = Only use for Submitted Date and Proposed Amount

**Use Proposal Details as primary for:**
- Pending proposals (not yet awarded)
- Not Funded proposals (rejected)
- Historical submission activity and success rate analysis

**Important**: Proposal Details is CON-level only (no project-level detail). Award Details has project-level information with semicolon-separated Project IDs.

---

## Quick Start

### Loading Proposal Data

```python
from scripts.load_proposal_data import load_proposal_data, get_data_date

df_proposals = load_proposal_data('20251209_Proposal_Details.xlsx')
data_date = get_data_date('20251209_Proposal_Details.xlsx')
print(f"Proposal data as of: {data_date}")
```

### Loading Award Data

```python
from scripts.load_award_data import load_award_data, get_award_data_date, check_data_date_match

df_awards = load_award_data('20251209_Award_Details.xlsx')
award_date = get_award_data_date('20251209_Award_Details.xlsx')
print(f"Award data as of: {award_date}")
```

**IMPORTANT -- Award Details Column Names:**
- Use `'Award Label'` to filter base vs supplements ("Anticipated Amount", "Supplement Amount", or NaN)
- Use `'Award Status'` to filter active vs completed ("Active" or "Completed")
- There is NO `'Status'` column in Award Details

**Filtering examples:**
```python
# Base awards only (no supplements)
base_awards = df_awards[df_awards['Award Label'] == 'Anticipated Amount']

# Active awards only
active_awards = df_awards[df_awards['Award Status'] == 'Active']

# Active base awards
active_base = df_awards[
    (df_awards['Award Label'] == 'Anticipated Amount') &
    (df_awards['Award Status'] == 'Active')
]
```

### Loading Expenditure Data

```python
from scripts.load_expenditure_data import load_expenditure_data, get_fiscal_year

df_exp = load_expenditure_data('20251123_Expenditure_Details_FY25.xlsx')
fy = get_fiscal_year('20251123_Expenditure_Details_FY25.xlsx')
print(f"Analyzing FY{fy} expenditures")
```

### Verifying Data Date Match

Always check that Award Details and Proposal Details are from the same date:
```python
dates_match, award_date, prop_date = check_data_date_match(
    '20251209_Award_Details.xlsx', '20251209_Proposal_Details.xlsx'
)
if not dates_match:
    print(f"WARNING: Mismatched dates - Awards: {award_date}, Proposals: {prop_date}")
```

---

## Proposal ID System

Syracuse uses a two-tiered identifier system based on the April 12, 2025 migration from InfoEd to PeopleSoft:

- **CON##### (PeopleSoft)**: All post-migration proposals + all awarded proposals
- **3#### (InfoEd Inst #)**: Pre-migration unfunded proposals only

One CON can contain multiple rows in Proposal Details (multiple funding requests over time -- NOT budget splits). Each row is an independent submission.

In Award Details, multiple rows per CON = base award + supplements. Sum these for total anticipated award.

Use `scripts/identifier_parser.py` for parsing and validating proposal identifiers.

See `references/proposal_id_system.md` for complete documentation.

---

## Common Proposal Queries

```python
from scripts.proposal_query import (
    filter_by_status, filter_by_pi, filter_by_sponsor,
    filter_by_date_range, filter_academic_only,
    summarize_by_unit, summarize_by_status, summarize_by_sponsor_type,
    get_top_pis, identify_subcontracts,
    add_fiscal_year, cross_reference_faculty,
    consolidate_instrument_type, consolidate_program_type
)

# By status
funded = filter_by_status(df_proposals, 'Funded')

# By school/college
unit_summary = summarize_by_unit(df_proposals)

# By sponsor type
sponsor_summary = summarize_by_sponsor_type(df_proposals)

# Engineering funded proposals
engineering_funded = filter_by_status(
    filter_by_pi(df_proposals, pi_unit='Engineering'), 'Funded'
)

# Federal proposals
federal = filter_by_sponsor(df_proposals, is_federal=True)

# NSF proposals
nsf = filter_by_sponsor(df_proposals, federal_department='National Science Foundation')

# Subcontracts (where SU is subrecipient)
subs = identify_subcontracts(df_proposals)

# Academic departments only (21xxx, 22xxx, 23xxx)
academic = filter_academic_only(df_proposals)

# Add fiscal year based on Award Project Start Date
df_with_fy = add_fiscal_year(df_proposals)
```

---

## Common Award Queries

```python
from scripts.proposal_query import (
    calculate_total_award, filter_active_awards, filter_completed_awards,
    get_awards_with_supplements, calculate_annual_rate
)

# Total award amounts per CON (base + supplements)
totals = calculate_total_award(df_awards)

# Active awards only
active = filter_active_awards(df_awards)

# Awards with supplements
with_supps = get_awards_with_supplements(df_awards)

# Annual award rates for active academic awards
active_academic = filter_academic_only(filter_active_awards(df_awards))
with_rate = calculate_annual_rate(active_academic)
high_rate = with_rate[with_rate['Annual_Rate'] >= 100000]

# Proposed vs Awarded comparison
funded = df_proposals[df_proposals['Proposal Status'] == 'Funded']
award_totals = df_awards.groupby('Contract Num')['Anticipated & Supplement Award Amount'].sum()
comparison = funded.merge(
    award_totals.rename('Actual_Award'),
    left_on='Proposal ID', right_index=True, how='inner'
)
comparison['Difference'] = comparison['Actual_Award'] - comparison['Proposed Amount']
```

---

## Common Expenditure Queries

```python
from scripts.expenditure_query import (
    summarize_by_category, summarize_by_subcategory,
    summarize_by_month, summarize_by_unit,
    filter_by_pi, filter_by_department, filter_by_sponsor_type,
    analyze_direct_indirect, analyze_federal_spending,
    get_top_contracts, get_top_pis, get_burn_rate,
    compare_to_budget
)

# Category breakdown (Direct/Indirect/Undefined)
category_summary = summarize_by_category(df_exp)

# Monthly spending pattern
monthly_summary = summarize_by_month(df_exp, fiscal_year_order=True)

# By school/college
unit_summary = summarize_by_unit(df_exp)

# Direct vs Indirect / F&A rate
fna = analyze_direct_indirect(df_exp)
print(f"Effective F&A rate: {fna['effective_rate']:.1f}%")

# PI spending
pi_spending = filter_by_pi(df_exp, pi_name='Smith')

# Department analysis (using Syr Proj Deptid -- authoritative for expenditure)
dept_spending = filter_by_department(df_exp, deptid=21825)

# Top contracts and PIs
top_contracts = get_top_contracts(df_exp, n=10)
top_pis = get_top_pis(df_exp, n=20)

# Burn rate for a specific contract
burn = get_burn_rate(df_exp, contract_num='CON05409')

# Federal spending analysis
fed = analyze_federal_spending(df_exp)

# Budget vs actual (requires both proposal and expenditure data)
budget_comparison = compare_to_budget(df_exp, df_proposals, 'CON05409')
```

---

## Cross-Referencing with Faculty Data

The `cross_reference_faculty()` function handles PI name matching, including the "I First" format (e.g., "Smith, J Robert" -> matches on "Michael" not "J"):

```python
import pandas as pd

# Load faculty data with forward-fill for merged cells
df_faculty = pd.read_excel('20251123_Faculty_by_Unit.xlsx')
df_faculty['UNIT'] = df_faculty['UNIT'].ffill()
df_faculty['SUB_UNIT'] = df_faculty['SUB_UNIT'].ffill()
df_faculty['DEPARTMENT_DESC'] = df_faculty['DEPARTMENT_DESC'].ffill()
if 'JOBCODE_DESC.1' in df_faculty.columns:
    df_faculty = df_faculty.drop(columns=['JOBCODE_DESC.1'])

# Cross-reference proposals with faculty
matched = cross_reference_faculty(df_proposals, df_faculty)
faculty_pis = matched[matched['_merge'] == 'both']        # ~73% match
non_faculty_pis = matched[matched['_merge'] == 'left_only']  # ~27% (legitimate)
```

**Unit Name Mapping** (Proposal data -> Faculty data):
```python
unit_mapping = {
    'Arts & Sciences': 'Arts and Sciences',
    'Engineering': 'Engineering / Computer Science',
    'Information Studies': 'iSchool',
    'Whitman': 'Whitman School of Management',
    'Falk': 'FALK',
    'VPA': 'Visual and Performing Arts',
}
```

**Why 27% don't match (expected):** IVMF staff/directors, librarians, historical PIs, research staff, postdocs with PI waivers, faculty with admin appointments submitting in admin units.

See `references/cross_reference_guide.md` for complete matching strategies.

---

## Cross-Referencing with Chart of Accounts

PI Deptid in proposals maps to Chart of Accounts department IDs. If the `su-chart-of-accounts` skill is available:

```python
from scripts.coa_data_query import ChartOfAccountsData
coa = ChartOfAccountsData()
dept_info = coa.get_department(21812)
```

**Department Area Codes:**
- 21xxx = Schools and colleges (academic)
- 22xxx = Research centers (academic)
- 23xxx = VPA (academic)
- 10xxx, 19xxx, 20xxx, 30xxx, 31xxx, 40xxx = Administrative

---

## Critical Data Loading Requirements

### Merged Cell Handling

All three datasets have Tableau merged cells requiring forward-fill. The loading functions handle this automatically:

| Dataset | Merged Cell Columns | Forward-Fill Strategy |
|---------|--------------------|-----------------------|
| Proposals | Proposal ID, Proposal Title, Proposal Status | Global forward-fill |
| Awards | Contract Num, Award Title | Global forward-fill |
| Awards | Award Label | **DO NOT** forward-fill (blank = 2nd+ supplement) |
| Expenditures | 15 of 21 columns | Within each Contract Num group |

**Expenditure data is especially critical**: Forward-fill must be done WITHIN each contract to prevent data bleeding between CONs. The `load_expenditure_data()` function handles this correctly. Never use simple global forward-fill on expenditure data.

### Federal Data Cleanup (Expenditures)

Federal Department/Subtier/Office columns are automatically set to null for non-federal sponsors by `load_expenditure_data()` to fix Tableau export artifacts.

---

## Key Data Relationships

### Contract Num / Proposal ID Links All Three Datasets

- Proposals: `Proposal ID` (CON##### or 3####)
- Awards: `Contract Num` (CON##### only)
- Expenditures: `Contract Num` (CON##### only)

### Department IDs

- **PI Department (if any)** = PI's HR home department
- **Syr Proj Deptid** (expenditures only) = **AUTHORITATIVE** -- where expense actually occurred
- A Physics PI can charge expenses to Engineering for interdisciplinary work

### Amounts Have Different Meanings

- **Proposed Amount** (proposals) = What was requested from sponsor
- **Anticipated & Supplement Award Amount** (awards) = What was awarded (each row is one action; sum per CON for total)
- **Expenditure Amount** (expenditures) = Actual spending

### Multi-Row CONs Have Different Meanings

**In Proposal Details:** Multiple rows = multiple independent funding requests over time. Do NOT sum Proposed Amounts.

**In Award Details:** Multiple rows = base + supplements. DO sum amounts for total award. Negative amounts = deobligations (subtract from total).

---

## Fiscal Year Information

- Syracuse FY runs July 1 - June 30 (FY25 = July 1, 2024 - June 30, 2025)
- For proposals: Use **Submitted Date** column for FY assignment (matches dashboard)
- For expenditures: Data is already organized by FY in the file
- Higher spending typically May/June (year-end); lower in July/August (startup)

---

## Expenditure-Specific Notes

### Expense Categories
- **DIRECT COSTS** (~83%): Salaries, Fringe, Travel, Equipment, Subcontracts, Other Direct, Tuition/Stipends
- **INDIRECT COSTS** (~17%): F&A recovery
- **UNDEFINED ACCOUNT** (<1%): Cost share or special arrangements

### Project Type Codes
- 310/311/312 = Federal (Research/Training/Other)
- 320/321/322/323 = State
- 340/341/342 = Private

### F&A Rate Calculations
The simplified MTDC calculation in `analyze_direct_indirect()` excludes Equipment and Subcontracts. Actual MTDC calculations are more complex and project-specific. Effective F&A rates vary by sponsor type, project type, and on/off-campus status.

---

## Visualization

```python
from scripts.expenditure_visualization import (
    plot_monthly_trend, plot_category_breakdown,
    plot_unit_comparison, plot_sponsor_analysis,
    create_summary_report
)

fig = plot_monthly_trend(df_exp, "FY25 Monthly Expenditure Trend")
fig = plot_category_breakdown(df_exp, "FY25 Expense Categories")
fig = plot_unit_comparison(df_exp, top_n=10)
fig = plot_sponsor_analysis(df_exp)

report = create_summary_report(df_exp, "expenditure_summary.txt")
```

---

## Tips for Analysis

### General
1. **Data is dynamic** -- users provide their own exports; don't hard-code specifics
2. **Always verify data dates match** when combining proposals and awards
3. **Use numeric IDs for matching** (PI Deptid, not department names)
4. **Filter academic vs administrative** using area codes (21/22/23 = academic)
5. **Federal dominance** -- ~62% of proposals and ~65% of expenditures are federal

### Proposals
6. **Multi-row CONs** in proposals = independent requests (don't sum)
7. **InfoEd data quality** -- legacy data has free-form sponsor names
8. **Use Submitted Date** for fiscal year assignment
9. **PI Name variations** -- handle "I First" format; use fuzzy matching

### Awards
10. **Sum for totals** -- base + all supplements = total anticipated award
11. **Handle negatives** -- deobligations reduce the total
12. **Don't forward-fill Award Label** -- blanks are meaningful (2nd+ supplements)
13. **Award Status** -- Active vs Completed based on end date

### Expenditures
14. **Forward-fill within contracts** -- never global forward-fill
15. **Negative expenditures** -- normal adjustments; include in totals
16. **Monthly patterns** -- expect seasonality in spending
17. **Syr Proj Deptid is authoritative** for where money was spent

---

## Detailed References

- **references/proposal_data_structure.md** -- Proposal Details: Complete column-by-column documentation
- **references/award_details_structure.md** -- Award Details: Complete column documentation, supplements
- **references/expenditure_data_structure.md** -- Expenditure Details: Complete column documentation
- **references/proposal_id_system.md** -- CON vs InfoEd Inst # system, merged cells
- **references/sponsor_hierarchy.md** -- Primary Sponsor vs Sponsor Name, federal hierarchy
- **references/cross_reference_guide.md** -- Linking with faculty-by-unit and su-chart-of-accounts
- **references/fiscal_year_info.md** -- Fiscal year calculations, dashboard reconciliation

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/load_proposal_data.py` | Load Proposal Details with merged cell handling |
| `scripts/load_award_data.py` | Load Award Details with merged cell handling |
| `scripts/load_expenditure_data.py` | Load Expenditure Details with per-contract forward-fill |
| `scripts/proposal_query.py` | Query/filter/aggregate proposals and awards |
| `scripts/expenditure_query.py` | Query/filter/aggregate expenditures |
| `scripts/identifier_parser.py` | Parse and validate CON/InfoEd proposal identifiers |
| `scripts/expenditure_visualization.py` | Matplotlib charts and summary reports |
