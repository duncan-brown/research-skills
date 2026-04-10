# Cross-Reference Guide

## Overview

Sponsored Proposals data can be linked with other Syracuse University data sources for comprehensive analysis. This guide explains how to cross-reference with faculty-by-unit and su-chart-of-accounts skills.

## Cross-Referencing with Faculty Data (faculty-by-unit)

### PI Administrative Unit -> UNIT

**Mapping**: Direct correspondence

**Proposals Field**: `PI Administrative Unit` (24 unique values)
**Faculty Field**: `UNIT` (same 24 values)

**Examples**:
- "Arts & Sciences" in both
- "Engineering" in both
- "Maxwell" in both

**Usage**:
```python
# Get faculty in same unit as proposals
proposals_df['PI Administrative Unit'].isin(faculty_df['UNIT'])
```

**Note**: Both datasets use identical school/college names, making this a clean join.

### PI Department -> DEPARTMENT_DESC

**Mapping**: Approximate match with caveats

**Proposals Field**: `PI Department (if any)` (descriptive name)
**Faculty Field**: `DEPARTMENT_DESC` (HR department name)

**Challenge**: Department names may differ slightly:
- Proposals: "Writing Program"
- Faculty: "Writing Program" (usually matches)
- Proposals: "Ctr on Disability & Inclusion"
- Faculty: "Center On Disability And Inclusion" (formatting differences)

**Best Practice**: Use PI Deptid instead for reliable matching.

### PI Deptid -> Lookup via su-chart-of-accounts

**Mapping**: PI Deptid is a Chart of Accounts department ID

**Proposals Field**: `PI Deptid` (5-digit integer, e.g., 21812)
**Chart of Accounts**: Department ID in department listing

**Usage**:
```python
from scripts.coa_data_query import ChartOfAccountsData

coa = ChartOfAccountsData()
dept_info = coa.get_department(21812)
# Returns: {'deptid': 21812, 'description': '...', 'status': 'A'}
```

**Then cross-reference with faculty**:
```python
# Use HR to Comptroller mapping from faculty-by-unit skill
# See: /mnt/skills/user/faculty-by-unit/references/department-mapping.md
```

### PI Name -> Faculty Data

**Mapping**: Name matching with format conversion and middle initial handling

**Proposals Format**: "Last Name, First Name Middle Initial" (e.g., "Jones, Maria L")
**Faculty Format**: Separate MAIN_LAST_NAME, MAIN_FIRST_NAME fields

**Critical**: Handle "I First" format (e.g., "Smith, J Robert" where middle initial precedes first name)

**Matching Strategy**:
```python
from scripts.proposal_query import cross_reference_faculty

# Cross-reference with automatic name parsing
matched = cross_reference_faculty(proposals, faculty)

# Faculty PIs
faculty_pis = matched[matched['_merge'] == 'both']

# Non-faculty PIs (staff, directors, historical)
non_faculty = matched[matched['_merge'] == 'left_only']
```

**Expected Match Rate: ~73%**
- 451 unique faculty PIs (from 2,690 faculty proposals)
- 216 unique non-faculty PIs (directors, staff, historical faculty)

**Name Parsing Logic**:
```python
def get_first_name(full_first):
    """Handle both 'First Middle' and 'I First' patterns."""
    parts = full_first.split()
    # If first part is single letter initial, use second part
    if len(parts) > 1 and len(parts[0]) == 1:
        return parts[1]  # "J Michael" -> "Michael"
    return parts[0]      # "Brice A" -> "Maria"
```

**Examples**:
- "Jones, Maria L" -> Last: "Jones", First: "Maria"
- "Smith, J Robert" -> Last: "Smith", First: "Robert" (not "J")
- "Garcia, David R" -> Last: "Garcia", First: "David"

**Why 27% Don't Match (Expected & Legitimate)**:

**1. Administrative/Staff PIs (director or higher per PI policy):**
- Veteran & Military Affairs (80% unmatched): IVMF staff directors
- Library (100% unmatched): Librarians and staff
- Office of Research: Senior administrators (some are faculty with admin roles)
- Other administrative units: Program directors, staff

**2. Faculty with Administrative Appointments:**
Some faculty ARE in faculty data but may submit in different units:
- Faculty PI A: Physics faculty (21825) + VP for Research (20301, 20305)
- Faculty PI B: Public Health faculty + Assoc VP Research
- Faculty PI C: Whitman faculty + Vice Chancellor (submits in IVMF 31301)
- Faculty PI D: Academic Affairs + Burton Blatt Institute

**3. Research Staff:**
- Falk (78% unmatched): Research scientists, postdocs with director status
- Clinical/field faculty not in main faculty listing

**4. Temporal Mismatch:**
- Proposals span 2013-2026+
- Faculty snapshot is November 23, 2025
- Historical PIs who have left

**5. Special Appointments:**
- Adjunct/clinical faculty
- Visiting scholars
- Postdocs with PI waivers from VP for Research

### Example: Faculty Proposals Analysis

```python
from load_proposal_data import load_proposal_data
import pandas as pd

# Load both datasets
proposals = load_proposal_data('20251123_Proposal_Details.xlsx')
faculty = pd.read_excel('20251123_Faculty_by_Unit.xlsx')

# Forward-fill faculty merged cells
faculty['UNIT'] = faculty['UNIT'].ffill()
faculty['SUB_UNIT'] = faculty['SUB_UNIT'].ffill()
faculty['DEPARTMENT_DESC'] = faculty['DEPARTMENT_DESC'].ffill()

# Match by unit
unit_match = proposals.merge(
    faculty[['UNIT', 'MAIN_LAST_NAME', 'MAIN_FIRST_NAME', 'JOBCODE_DESC']].drop_duplicates(),
    left_on='PI Administrative Unit',
    right_on='UNIT',
    how='inner'
)

# Count proposals by faculty type
by_faculty_type = unit_match.groupby('JOBCODE_DESC')['Proposal ID'].count()
```

## Cross-Referencing with Chart of Accounts (su-chart-of-accounts)

### Project ID -> Chart of Accounts Project

**Mapping**: Direct correspondence (when data is correct)

**Proposals Field**: `Project ID` (e.g., 7883, 6245)
**Chart of Accounts**: Project ID in SAMTool listings

**Current Status**: [!] Known data quality issue
- Project ID in proposals data is incorrect for multi-proposal CONs
- Wait for bug fix before relying on this mapping

**Once Fixed**:
```python
from scripts.coa_data_query import ChartOfAccountsData

coa = ChartOfAccountsData()
project_info = coa.get_project(7883)
# Returns: {'project_id': 7883, 'title': '...', 'activity_count': 1}
```

### PI Deptid -> Chart of Accounts Department

**Mapping**: Direct correspondence

**Proposals Field**: `PI Deptid` (e.g., 21812)
**Chart of Accounts**: DEPTID in department listings

**Usage**:
```python
from scripts.coa_data_query import ChartOfAccountsData

coa = ChartOfAccountsData()
dept = coa.get_department(21812)
print(dept['description'])  # Official Chart of Accounts department name
```

**Statistics**:
- Proposals has 125 unique PI Deptids
- Chart of Accounts has 740 active departments
- All proposal Deptids should exist in CoA (subset relationship)

### Linking to Chartstrings

**Once Project ID bug is fixed**, proposals can be linked to financial transactions:

```python
from scripts.chartstring_parser import parse_chartstring

# For a funded proposal with Project ID
project_id = 7883

# Build chartstring pattern
# Sponsored projects use Fund 13, Program 00013
chartstring_pattern = f"13-*-00013-*-*-{project_id:05d}-*-*"

# Query financial transactions using this project
# (Would require additional financial data not in proposals dataset)
```

### Department Cross-Walk

PI departments in proposals map to both:
1. **HR departments** (in faculty data)
2. **Comptroller departments** (in Chart of Accounts)

These are often the same but can differ:

**Example**:
- Proposals PI Deptid: 21301 
- Chart of Accounts: DEPTID 21301 -> "College of Engineering & Computer Science"
- Faculty: DEPARTMENT_DESC -> "Engineering & Computer Science"

**Use the mapping file**:
```
/mnt/skills/user/faculty-by-unit/references/department-mapping.md
```

## Common Cross-Reference Analyses

### 1. Proposal Success Rate by Faculty Type

```python
# Merge proposals with faculty on PI name and unit
# Calculate success rate by JOBCODE_DESC
```

### 2. Proposals by Department with CoA Details

```python
from scripts.coa_data_query import ChartOfAccountsData

coa = ChartOfAccountsData()

# Add CoA department names
proposals['CoA_Dept_Name'] = proposals['PI Deptid'].apply(
    lambda x: coa.get_department(int(x))['description'] if pd.notna(x) else None
)
```

### 3. Tenure-Stream Faculty Proposals

```python
# Get tenure-stream faculty
tenure_stream = faculty[faculty['TENURE_STATUS_DESC'].isin(['Tenure', 'Non Tenure On Track'])]

# Match with proposals
proposals_with_faculty = proposals.merge(
    tenure_stream[['MAIN_LAST_NAME', 'MAIN_FIRST_NAME', 'TENURE_STATUS_DESC']],
    left_on=['Last_Name', 'First_Name'],
    right_on=['MAIN_LAST_NAME', 'MAIN_FIRST_NAME']
)
```

### 4. Projects by Area Code (CoA)

```python
# Department area codes (first 2 digits of 5-digit Deptid)
proposals['Area_Code'] = (proposals['PI Deptid'] // 1000).astype('Int64')

# Area codes:
# 21xxx = Schools/Colleges
# 22xxx = Research Centers
# 23xxx = Academic Support
# etc.
```

## Matching Limitations

### Not All PIs Are in Faculty Data

Proposals may have PIs who are:
- Staff researchers (not faculty)
- Administrators with research roles
- Adjunct instructors (may not be in snapshot)
- External collaborators (off-campus)
- Faculty who left (proposals from past years)

**Result**: Inner joins will lose proposals. Use left joins and analyze unmatched records.

### Project ID Data Quality

**Current state**: Cannot reliably link to Chart of Accounts projects until bug is fixed.

**Once fixed**: Will enable powerful cross-analysis with financial data.

### Department Name Variations

Department names are not standardized across systems:
- Proposals: PI Department (descriptive)
- Faculty: DEPARTMENT_DESC (HR system)
- Chart of Accounts: Description (Comptroller system)

**Best Practice**: Always use Deptid (numeric) for matching, not names.

### Temporal Mismatches

- Proposals data: Multi-year proposals (FY2010-FY2026+)
- Faculty data: Single point-in-time snapshot (November 23, 2025)
- Chart of Accounts: Current active records

**Implication**: Historical proposals may reference departments or faculty that no longer exist or have changed.

## Best Practices

1. **Use numeric IDs** (Deptid, Project ID) for matching, not names
2. **Validate matches** - Check join results for unexpected nulls
3. **Use left joins** when proposals are the primary dataset
4. **Document unmatched records** - Analyze why proposals don't match faculty
5. **Consider temporal issues** - Historical proposals may not match current faculty
6. **Leverage skills** - Use faculty-by-unit and su-chart-of-accounts skills for lookups
7. **Wait for bug fix** - Don't rely on Project ID until data quality issue is resolved

## Integration Example

```python
from load_proposal_data import load_proposal_data
from scripts.coa_data_query import ChartOfAccountsData

# Load proposals
proposals = load_proposal_data('20251123_Proposal_Details.xlsx')

# Initialize Chart of Accounts
coa = ChartOfAccountsData()

# Enrich proposals with CoA department names
proposals['CoA_Department'] = proposals['PI Deptid'].apply(
    lambda x: coa.get_department(int(x))['description'] if pd.notna(x) else None
)

# Get fund description (assuming you know the fund)
# Most operating: Fund 11
# Sponsored: Fund 13

# For funded proposals, could eventually link Project ID to full chartstrings
# (once Project ID bug is fixed)
```

## Academic vs Administrative Capacity

### Understanding Faculty Roles in Proposals

Faculty with administrative appointments (Deans, VPs, Department Chairs) may submit proposals in either:
1. **Faculty capacity**: In their academic department
2. **Administrative capacity**: In their administrative unit

### Identifying Capacity by Department

**Academic Departments** (Area Codes: 21xxx, 22xxx, 23xxx):
- 21xxx: Schools and colleges
- 22xxx: Research centers (Maxwell, Falk, SUCE)
- 23xxx: VPA

**Administrative Departments** (Area Codes: 10xxx, 19xxx, 20xxx, 30xxx, 31xxx, 40xxx):
- 10xxx: Chancellor's Office, HR
- 19xxx: Capital Development, Facilities
- 20xxx: Office of Research, Library, Academic Affairs, Graduate School
- 30xxx: Administrative Operations
- 31xxx: IVMF (administrative unit)
- 40xxx: VP for Student Affairs

### Special Cases: Research Centers

Some proposals in 20xxx may be faculty capacity:
- **CASE Center (20305)**: Accepts faculty proposals from affiliated faculty
  - Center Director: Administrative
  - Affiliated faculty: Faculty capacity
  
**Rule of Thumb**:
- VP/Provost offices (20301, 20034, etc.): Administrative capacity
- Research centers (20305, 20311, 20321): Often faculty capacity
- When in doubt, check if PI is center director

### Examples from Data

**Faculty PI A (Vice President for Research)**:
- 21825 (Physics): Faculty capacity - 7 proposals
- 20301 (VP for Research): Administrative capacity - 3 proposals
- 20305 (CASE Center): Administrative capacity (as director) - 6 proposals

**Faculty PI B (Associate VP for Research)**:
- 22033/22470 (Public Health): Faculty capacity - 15 proposals
- Holds admin title but submits as faculty in her department

**Faculty PI C (Vice Chancellor)**:
- 31301 (IVMF): Administrative capacity - 35 proposals
- Faculty appointment in Whitman, but submits in admin role

**Faculty PI E (Associate Dean ECS)**:
- 21406 (Mechanical & Aerospace): Faculty capacity - 39 proposals
- 20305 (CASE Center): Faculty capacity (affiliated) - 1 proposal
- Holds admin title but submits as faculty

**Faculty PI F (Vice Provost)**:
- 22025 (Autonomous Systems Policy Inst): Faculty capacity - 2 proposals
- 20034 (Assoc Provost Faculty Affairs): Administrative capacity - 1 proposal

**Most Department Chairs**:
- Submit in their academic department (faculty capacity)
- Administrative role doesn't change where they submit

### Filtering Strategy

**For faculty-only analysis** (excluding administrative proposals):
```python
from scripts.proposal_query import filter_academic_only

# Get only academic department proposals (21xxx, 22xxx, 23xxx)
academic_only = filter_academic_only(df)

# This excludes:
# - All VP/Provost office proposals
# - IVMF administrative proposals
# - Library, facilities, etc.
# But includes:
# - All school/college proposals
# - Research center proposals (Maxwell, Falk, CASE)
```

**Note**: This approach treats research center proposals as academic (mostly correct), but may include a few administrative submissions like a center director in CASE.

**For pure faculty capacity** (more complex):
- Cross-reference with faculty data
- Check if PI Deptid matches faculty department
- Manually identify administrators and their admin departments
