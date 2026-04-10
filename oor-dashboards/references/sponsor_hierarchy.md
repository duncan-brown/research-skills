# Sponsor Hierarchy Reference

## Overview

The Sponsored Proposals data tracks both the ultimate funding source and the direct contracting entity, which can differ when Syracuse University is a subcontractor or subgrantee.

## Two Sponsor Fields

### Primary Sponsor
**Definition**: The ultimate source of funding

**Examples**:
- National Science Foundation
- National Institutes of Health
- Department of Defense
- New York State Department of Economic Development

**Use**: Identifies where the money originally comes from

### Sponsor Name
**Definition**: The direct contracting entity with Syracuse University

**Examples**:
- Cornell University (when SU is a subcontractor)
- University of Rochester (when SU is a subgrantee)
- National Science Foundation (when direct award)

**Use**: Identifies who SU contracts with directly

## Identifying Subcontracts and Subgrants

**Rule**: When Primary Sponsor != Sponsor Name, SU is a subcontractor or subgrantee

### Direct Awards
```
Primary Sponsor: National Science Foundation
Sponsor Name:    National Science Foundation
Result: Direct award from NSF to SU
```

### Subcontracts/Subgrants
```
Primary Sponsor: National Science Foundation  (ultimate funding source)
Sponsor Name:    Cornell University           (prime institution)
Result: NSF funded Cornell, Cornell subcontracted to SU
```

### Example from Data
```
Proposal: Developing an AI-augmented tool to improve water quality
Primary Sponsor: NYS Dept of Environmental Conservation  (state funding)
Sponsor Name:    Cornell University                       (prime contractor)
```

## Sponsor Type Classifications

### Primary Sponsor Type
Categories for ultimate funding source:
1. **Federal Agencies** (62.0%) - U.S. government agencies
2. **Not for Profit/Foundation** (22.2%) - Private foundations, nonprofits
3. **Corporations/Companies** (6.2%) - Industry sponsors
4. **New York State** (4.9%) - NYS agencies
5. **Foreign** (1.9%) - International entities
6. **Other Governmental/Public Sect** (1.6%) - Other government
7. **University/College** (1.0%) - Other universities (direct awards)
8. **State - Other** (0.3%) - Non-NYS states
9. **European Organisation** (<0.1%) - EU entities

### Sponsor Type
Categories for direct contracting entity:
1. **Federal Agencies** (43.0%) - Lower than Primary due to subcontracts
2. **Not for Profit/Foundation** (23.3%)
3. **University/College** (17.7%) - **Much higher** than Primary (subcontracts)
4. **Corporations/Companies** (8.9%)
5. **New York State** (3.7%)
6. **Foreign** (1.8%)
7. **Other Governmental/Public Sect** (1.6%)
8. **State - Other** (0.1%)
9. **European Organisation** (<0.1%)

**Key Insight**: University/College sponsors are 17.7% of Sponsor Type but only 1.0% of Primary Sponsor Type. This indicates many proposals where SU is a subcontractor/subgrantee under another university.

## Federal Sponsor Hierarchy

For federal sponsors (Primary Sponsor Type = "Federal Agencies"), three additional fields provide organizational detail:

### Federal Department
**Level**: Cabinet-level department or independent agency

**Examples**:
- National Science Foundation (NSF is independent, so same at all levels)
- Department Of Health And Human Services
- Dept Of Defense
- Department Of Energy
- National Aeronautics And Space Administration
- Department Of Agriculture

**Total**: 26 federal departments in dataset

**Distribution**:
- NSF: 40.9% of federal proposals
- HHS: 28.1%
- DoD: 9.4%
- DoE: 4.9%
- NASA: 2.8%

### Federal Subtier
**Level**: Sub-agency within department

**Examples**:
- National Institutes Of Health (within HHS)
- National Science Foundation (independent)
- Air Force Office of Scientific Research (within DoD)
- Defense Advanced Research Projects Agency (within DoD)

**Note**: For independent agencies like NSF, all three federal fields are the same.

### Federal Office
**Level**: Program office or institute within subtier

**Examples**:
- National Institutes Of Health
- National Science Foundation
- Specific NIH institutes (NIGMS, NCI, etc.)

**Data Note**: In this dataset, Federal Office often matches Federal Subtier, suggesting program-level detail may not always be captured.

## Federal vs Non-Federal Split

**Federal proposals**: 62.0% of all proposals (Primary Sponsor Type = "Federal Agencies")

**Federal fields populated**: Only when Primary Sponsor Type = "Federal Agencies"
- Federal Department: 2,254 rows (61.5% of total)
- Federal Subtier: 2,254 rows
- Federal Office: 2,254 rows

**Non-federal proposals**: 38.0% (all other Primary Sponsor Types)
- Federal fields are blank

## Querying by Sponsor

### Find all federal proposals
```python
federal = df[df['Primary Sponsor Type'] == 'Federal Agencies']
```

### Find NSF proposals
```python
nsf = df[df['Federal Department'] == 'National Science Foundation']
# or
nsf = df[df['Primary Sponsor'].str.contains('National Science Foundation', na=False)]
```

### Find NIH proposals
```python
nih = df[df['Federal Subtier'] == 'National Institutes Of Health']
```

### Find all subcontracts/subgrants
```python
subs = df[df['Primary Sponsor'] != df['Sponsor Name']]
```

### Find proposals where SU is subcontractor under another university
```python
subs = df[df['Sponsor Type'] == 'University/College']
```

## Sponsor Naming Conventions

### Variations in Sponsor Names
Sponsor names may have slight variations in the data:
- "National Institutes of Health" vs "National Institutes Of Health"
- "NIH" vs "National Institutes of Health"
- Abbreviations vs full names

**Best Practice**: Use case-insensitive partial matching:
```python
nih = df[df['Primary Sponsor'].str.contains('National Institutes', case=False, na=False)]
```

### Federal Department Naming
Federal departments generally use full official names:
- "Department Of Health And Human Services" (not "DHHS" or "HHS")
- "Dept Of Defense" (abbreviated "Dept")
- "National Science Foundation" (no abbreviation)

## Instrument Type Context

While not part of sponsor hierarchy, **Instrument Type** provides additional context:

**Main Types**:
- Grant (42.5%)
- Subgrant (Prime = Grant) (12.8%)
- Contract (8.3%)
- Subcontract (Prime = Contract) (2.9%)
- Cooperative Agreement (0.9%)

**Note**: Instrument Type is frequently blank (27.6%), so don't rely on it exclusively to identify subcontracts. Use the Primary Sponsor != Sponsor Name rule instead.

## Analysis Examples

### Federal funding by department
```python
from proposal_query import filter_by_sponsor

federal = filter_by_sponsor(df, is_federal=True)
fed_summary = federal.groupby('Federal Department').agg({
    'Proposal ID': 'count',
    'Proposed Amount': 'sum'
})
```

### Subcontract analysis
```python
from proposal_query import identify_subcontracts

subs = identify_subcontracts(df)
print(f"Total subcontracts: {len(subs)}")
print(f"Percentage: {len(subs)/len(df)*100:.1f}%")
```

### Top sponsors by total amount
```python
sponsor_summary = df.groupby('Primary Sponsor').agg({
    'Proposal ID': 'count',
    'Proposed Amount': 'sum'
}).sort_values('Proposed Amount', ascending=False)
```

## Best Practices

1. **Use Primary Sponsor** for ultimate funding source analysis
2. **Use Sponsor Name** to understand direct relationships and subcontracts
3. **Compare both fields** to identify subcontracts/subgrants automatically
4. **Filter by Primary Sponsor Type** for federal vs non-federal splits
5. **Use Federal Department** for detailed federal analysis
6. **Use case-insensitive matching** to handle sponsor name variations
7. **Don't rely solely on Instrument Type** to identify subcontracts (often blank)
