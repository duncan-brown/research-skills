# Award Details Data Structure

## Overview

Award Details data from the DataInsights dashboard provides actual award amounts and supplement tracking for funded proposals. This complements the Proposal Details data which shows requested amounts.

**Data Source**: https://datainsights.syr.edu/#/site/data/views/OfficeofResearchAnticipatedandSupplementAmounts/Details

**File Pattern**: `YYYYMMDD_Award_Details.xlsx`

**Current Data**: As of December 8, 2025

---

## Key Differences from Proposal Details

| Aspect | Proposal Details | Award Details |
|--------|------------------|---------------|
| Scope | All proposals (Pending, Not Funded, Funded) | Funded awards only |
| Identifiers | CON + InfoEd Inst # | CON only |
| Count | 1,788 unique (as of Nov 2025) | 3,354 unique (includes historical) |
| Amount | Proposed Amount (requested) | Anticipated & Supplement Award Amount (actual) |
| Supplements | Not tracked separately | Tracked with Award Label |
| Project ID | Float, buggy | String, semicolon-separated, correct |
| Program Type | Detailed (Research - Basic/Applied) | Simplified (Research only) |
| Time Range | Recent (FY2010-2027) | Historical (2013-2026) |

---

## Column Definitions

### 1. **Contract Num** (object) **[MERGED CELLS - REQUIRES FORWARD FILL]**
- **Format**: CON##### (e.g., CON06760, CON05881)
- **Non-null after forward-fill**: 3,711 (100%)
- **Unique values**: 3,354 CONs
- **Notes**: 
  - Same as Proposal ID in Proposal Details
  - Only CON format (all funded awards, no InfoEd Inst #)
  - Merged cells for base + all supplements
  - Includes historical awards back to 2013
  - 2,047 CONs NOT in Proposal Details (historical awards before proposal data timeframe)

### 2. **Award Title** (object) **[MERGED CELLS - REQUIRES FORWARD FILL]**
- **Non-null after forward-fill**: 3,711 (100%)
- **Unique values**: 3,217 titles
- **Notes**:
  - Similar to Proposal Title but may differ (title changes between proposal and award)
  - Merged cells for base + all supplements
  - Examples of differences: typos corrected, wording refined, character encoding
  - Describes the project/award

### 3. **Award Label** (object) **[DO NOT FORWARD FILL]**
- **Values**:
  - "Anticipated Amount": 3,306 (89.1%) - Base award
  - "Supplement Amount": 279 (7.5%) - First supplement
  - Blank/NaN: 126 (3.4%) - Additional supplements (2nd, 3rd, etc.)
- **Purpose**: Labels the type of amount in "Anticipated & Supplement Award Amount" column
- **Important**: Do NOT forward-fill - blanks are meaningful (indicate additional supplements)

### 4. **Date** (object -> datetime)
- **Format**: "M/D/YYYY" -> datetime
- **Non-null**: 3,711 (100%)
- **Definition**: Award Action Date (when this specific award action occurred)
- **Notes**:
  - For base award: Date when original award was executed
  - For supplements: Date when supplement was added
  - In this Excel export: Date always equals Award Project Start Date
  - Different from SAMTool "Begin Date" which is the original award's start date

### 5. **Award Status** (object)
- **Values**:
  - "Active": 666 (17.9%) - Award Project End Date > current date
  - "Completed": 3,045 (82.1%) - Award Project End Date <= current date
- **Non-null**: 3,711 (100%)
- **Notes**:
  - Automatically calculated based on Award Project End Date
  - 100% correlation with end date (no mismatches)
  - Use for filtering to currently active awards

### 6. **Award Project Start Date** (object -> datetime)
- **Format**: "M/D/YYYY" -> datetime
- **Non-null**: 3,711 (100%)
- **Definition**: Start of expenditure period for this award action
- **Notes**:
  - For base award: Original expenditure period start
  - For supplements: Supplement expenditure period start (can differ from base)
  - Same as "Date" in this Excel export
  - OSA allows charges starting from this date

### 7. **Award Project End Date** (object -> datetime)
- **Format**: "M/D/YYYY" -> datetime
- **Non-null**: 3,711 (100%)
- **Definition**: End of expenditure period for this award action
- **Notes**:
  - OSA stops allowing charges after this date
  - Used to calculate Award Status (Active vs Completed)
  - Can differ for base vs supplements

### 8. **Instrument Type** (object)
- **Values**: 5 types (all with "Inst Type - " prefix)
  - Inst Type - Grant: 2,341 (63.1%)
  - Inst Type - Contract: 619 (16.7%)
  - Inst Type - Subgrant: 451 (12.2%)
  - Inst Type - Subcontract: 211 (5.7%)
  - Inst Type - Coop Agremnt: 89 (2.4%)
- **Non-null**: 3,711 (100%)
- **Notes**:
  - Cleaner than Proposal Details (no blanks, consistent prefix)
  - All PeopleSoft format
  - Can consolidate by removing "Inst Type - " prefix

### 9. **Program Type** (object)
- **Values**: 3 types (simplified from Proposal Details)
  - Research: 2,262 (60.9%)
  - Other: 926 (25.0%)
  - Training: 523 (14.1%)
- **Non-null**: 3,711 (100%)
- **Notes**:
  - Simpler than Proposal Details (no Research - Basic/Applied/Development subtypes)
  - Based on 2 CFR 200.1 definitions
  - Award system doesn't track research subtype granularity

### 10. **Project ID** (object)
- **Format**: 5-digit string with leading zeros (e.g., "07900", "06938")
- **Multiple Projects**: Semicolon-separated (e.g., "06938; 07164")
- **Non-null**: 3,711 (100%)
- **Unique values**: 3,354 unique Project ID strings
- **Notes**:
  - String type (preserves leading zeros) - different from Proposal Details (float)
  - **NO BUG**: Multiple Project IDs shown correctly with semicolons
  - Same value across base + supplements for a CON (correct behavior)
  - 268 CONs have multiple Project IDs (budget splits)
  - Can be parsed with `parse_project_ids()` function

### 11. **PI Administrative Unit** (object)
- Same as Proposal Details
- 24 unique units
- Maps to Chart of Accounts area codes

### 12. **PI Deptid** (int64)
- Same as Proposal Details
- 5-digit Chart of Accounts department ID
- First 3 digits = area code

### 13. **PI Department (if any)** (object)
- Same as Proposal Details
- Department name (may vary slightly from Chart of Accounts)

### 14. **PI Name** (object)
- **Format**: "Last, First Middle" (e.g., "Smith, J Robert")
- **Non-null**: 3,711 (100%)
- **Unique**: 765 PIs
- **Notes**:
  - Same format as Proposal Details
  - 240 PIs only in Awards (historical)
  - 142 PIs only in Proposals (unfunded)
  - [!] **May not match HR data exactly** - fuzzy matching recommended
  - Use `cross_reference_faculty()` function for matching

### 15. **Primary Sponsor** (object)
- Same as Proposal Details
- Ultimate funding source
- Moving toward standardized enumerated values

### 16. **Primary Sponsor Type** (object)
- Same as Proposal Details
- Federal Agencies, Not for Profit, etc.

### 17. **Sponsor Name** (object)
- Same as Proposal Details
- Direct contracting entity

### 18. **Sponsor Type** (object)
- Same as Proposal Details

### 19. **Federal Department** (object)
- Same as Proposal Details
- Only for federal sponsors
- 1,826 non-null (49.2%)

### 20. **Federal Subtier** (object)
- Same as Proposal Details
- 1,826 non-null (49.2%)

### 21. **Federal Office** (object)
- Same as Proposal Details
- 1,826 non-null (49.2%)

### 22. **Anticipated & Supplement Award Amount** (float64)
- **Non-null**: 3,703 (99.8%)
- **Null**: 8 (recent awards or missing data)
- **Range**: -$124,530 to $11,477,740
- **Statistics**:
  - Mean: $278,210
  - Median: $67,541
  - Total across all rows: $1,030,209,947 ($1.03 billion)

**Interpretation by Award Label**:
- **"Anticipated Amount"** (base awards):
  - Total intended award amount from sponsor
  - May be obligated all at once or incrementally (e.g., NSF incremental funding)
  - Total: $1.00B across 3,306 base awards
  - Mean: $304K, Median: $80K

- **"Supplement Amount"** (first supplement):
  - Amount of the first supplement to the award
  - NOT cumulative - just the supplement itself
  - Total: $17.9M across 279 supplements
  - Mean: $65K, Median: $16K

- **Blank** (additional supplements):
  - Amount of 2nd, 3rd, 4th+ supplements
  - Can be negative (deobligations/reductions)
  - Total: $9.2M across 126 additional supplements
  - Mean: $73K, Median: $27K

**Calculating Total Award**:
```python
# Sum all rows for same CON to get total
total_per_con = df.groupby('Contract Num')['Anticipated & Supplement Award Amount'].sum()
```

**Negative Amounts** (4 occurrences):
- Deobligations or reductions
- Should be SUBTRACTED from total (included in sum)
- Examples: -$36,714, -$25,940, -$29,983, -$124,530

---

## Data Loading Requirements

**Critical**: Contract Num and Award Title columns have merged cells.

**Required Processing**:
```python
df = pd.read_excel(file_path)
df['Contract Num'] = df['Contract Num'].ffill()
df['Award Title'] = df['Award Title'].ffill()
# Do NOT forward-fill Award Label - blank is meaningful
```

**Date Matching**: Always check that Award Details and Proposal Details files are from the same date:
```python
from scripts.load_award_data import check_data_date_match

dates_match, award_date, prop_date = check_data_date_match(
    'YYYYMMDD_Award_Details.xlsx',
    'YYYYMMDD_Proposal_Details.xlsx'
)

if not dates_match:
    print(f"[!]  Warning: Mismatched dates - {award_date} vs {prop_date}")
```

---

## Relationship to Proposal Details

### Overlapping CONs
- **1,307 CONs in both datasets** (funded proposals with award data)
- **2 CONs only in Proposals** (recently funded, not yet in awards)
- **2,047 CONs only in Awards** (historical awards before proposal data timeframe)

### Comparing Amounts
For the 1,307 common CONs:
- **Proposal Details "Proposed Amount"**: What was requested
- **Award Details "Anticipated & Supplement Award Amount"**: What was awarded (base + supplements)
- Amounts can differ (negotiated down, or increased with supplements)

### Example Comparison
```python
# CON05408
# Proposal: "Reducing Climate Change Impacts..." - $284,560 requested
# Award: "Wasting Less Food & Recycling More..." - $237,900 awarded
# Result: Negotiated down by $46,660 (16.4%)
```

---

## Use Cases

### Awards-Only Analysis
- Total active funding across university
- Awards with supplements
- Completed vs active award tracking
- Actual award amounts (not proposed)

### Combined Proposal + Award Analysis
- Proposal to award conversion rates
- Negotiated changes (proposed vs awarded)
- Time from proposal to award
- Success rates with actual award amounts

### Faculty Analysis
- Cross-reference with faculty-by-unit
- Total active funding per PI
- Awards with supplements by PI
- Faculty without active awards

---

## Best Practices

1. **Check data dates match** - Warn if Award Details and Proposal Details from different dates
2. **Sum for totals** - Add base + all supplements for total anticipated award
3. **Handle negatives** - Deobligations reduce the total (included in sum)
4. **Parse Project IDs** - Use `parse_project_ids()` for semicolon-separated values
5. **Filter by status** - Use Award Status for active vs completed
6. **Calculate annual rates** - Use `calculate_annual_rate()` function
7. **Identify supplements** - Use `get_awards_with_supplements()` function
8. **Don't forward-fill Award Label** - Blanks are meaningful
