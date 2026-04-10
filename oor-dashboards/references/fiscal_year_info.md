# Fiscal Year Analysis - UPDATED v1.3

## Syracuse University Fiscal Year

**Definition**: July 1 through June 30

**Examples**:
- FY2025 = July 1, 2024 to June 30, 2025
- FY2026 = July 1, 2025 to June 30, 2026

---

## Assigning Proposals to Fiscal Years - RESOLVED! [OK]

**Solution (v1.3)**: Use **Submitted Date** column

**New column added December 2025:**
- Column 5: "Submitted Date"
- 100% populated
- Actual date when proposal/request was submitted
- Format: M/D/YYYY

```python
from scripts.proposal_query import add_fiscal_year

# Add fiscal year based on Submitted Date
df['Submitted_parsed'] = pd.to_datetime(df['Submitted Date'], format='%m/%d/%Y')
df['Fiscal Year'] = df['Submitted_parsed'].apply(lambda d: d.year + 1 if d.month >= 7 else d.year)
```

### Previous Ambiguity (v1.0-1.2) - NOW RESOLVED

**Old Problem**: Unclear which date dashboard used for FY assignment
- Award Project Start Date (expenditure start)
- Submission date (not in export)
- Other business logic

**Resolution**: Submitted Date column added to Proposal Details export
- Now have actual submission date
- Can calculate FY accurately
- Should match dashboard assignments

---

## Fiscal Year Calculations

### Assign Proposal to FY

```python
from datetime import datetime

def get_fiscal_year(date: datetime) -> int:
    """
    Get fiscal year for a submission date (July 1 - June 30).
    
    Examples:
        2024-09-01 -> FY2025
        2025-06-30 -> FY2025
        2025-07-01 -> FY2026
    """
    if date.month >= 7:
        return date.year + 1
    else:
        return date.year
```

### Filter by Fiscal Year

```python
from scripts.load_proposal_data import load_proposal_data
import pandas as pd

df = load_proposal_data('20251209_Proposal_Details.xlsx')

# Parse Submitted Date if not already parsed
df['Submitted_parsed'] = pd.to_datetime(df['Submitted Date'], format='%m/%d/%Y')

# Calculate FY
df['Fiscal Year'] = df['Submitted_parsed'].apply(
    lambda d: d.year + 1 if d.month >= 7 else d.year
)

# Get FY2025 proposals
fy2025 = df[df['Fiscal Year'] == 2025]
```

---

## Multi-Submission CONs

Some CONs have multiple funding requests submitted over time:

**Example - CON04525 (HEOP):**
- Submission 1: June 2021 (FY2022) - $1,526,000
- Submission 2: Feb 2022 (FY2022) - $393,086
- Submission 3: May 2022 (FY2022) - $1,943,841
- Submission 4: Dec 2022 (FY2023) - $268,237
- Submission 5: Apr 2023 (FY2023) - $2,235,865
- Submission 6: Mar 2024 (FY2024) - $95,688

**Each submission** has its own Submitted Date and fiscal year assignment.

**Important**: These are **independent requests**, not phases or budget splits.

---

## Analysis Examples

### Total Proposals by Fiscal Year

```python
# Count unique CONs per FY (dedup multi-submissions)
fy_summary = df.groupby('Fiscal Year')['Proposal ID'].nunique()
print("Unique CONs by fiscal year:")
print(fy_summary)
```

### Submission Activity by FY

```python
# Count all submissions (includes multi-row CONs)
submission_counts = df.groupby('Fiscal Year').size()
print("Total submissions by fiscal year:")
print(submission_counts)
```

### Current Fiscal Year (Partial)

The most recent fiscal year represents a partial year (July 1 through data export date).

**Example**: For data exported December 9, 2025
- FY2026 started July 1, 2025
- Data includes July 1 - December 9, 2025 (161 days of 365)
- FY2026 totals are incomplete

```python
from datetime import datetime

current_date = datetime(2025, 12, 9)  # Data export date
current_fy = 2026  # Since we're in Dec 2025

# Flag current FY as partial
df['Is_Partial_FY'] = df['Fiscal Year'] == current_fy
```

---

## Dashboard Reconciliation

### Why Use Submitted Date

The Tableau dashboard assigns proposals to fiscal years based on when they were submitted, not when they were awarded or when the expenditure period starts.

**Submitted Date** provides the actual submission date, enabling accurate FY assignment that matches the dashboard.

### Best Practices

- [OK] Use Submitted Date for FY assignment (matches dashboard)
- [OK] Flag current FY as partial (incomplete data)
- [OK] Use unique CON counts (dedup multi-submissions) or total submission counts as appropriate
- [OK] Note that multi-submission CONs can span multiple FYs

---

## Common Fiscal Year Queries

### Proposals by FY and Status

```python
# Unique CONs by FY and status
fy_status = df.drop_duplicates('Proposal ID').groupby(['Fiscal Year', 'Proposal Status']).size().unstack(fill_value=0)
print(fy_status)
```

### Funding Success Rate by FY

```python
fy_stats = df.drop_duplicates('Proposal ID').groupby('Fiscal Year').agg({
    'Proposal ID': 'count',
    'Proposal Status': lambda x: (x == 'Funded').sum()
})
fy_stats['Success_Rate'] = fy_stats['Proposal Status'] / fy_stats['Proposal ID'] * 100
```

### Federal vs Non-Federal by FY

```python
df_dedup = df.drop_duplicates('Proposal ID')
df_dedup['Is_Federal'] = df_dedup['Primary Sponsor Type'] == 'Federal Agencies'

fy_federal = df_dedup.groupby(['Fiscal Year', 'Is_Federal']).size()
```
