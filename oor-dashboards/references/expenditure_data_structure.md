# Expenditure Data Structure Reference

## Overview
Syracuse University Detailed Sponsored Expenditures data exported from DataInsights dashboard.
- **Hierarchical structure**: One CON has multiple expense categories, subcategories, and monthly entries
- **Critical**: 15 of 21 columns require forward-fill WITHIN each contract due to merged cells from Tableau export
- **Fiscal Year**: July 1 - June 30 (FY25 = July 1, 2024 - June 30, 2025)

## Column Documentation

### Contract Identifier
- **Contract Num**: CON##### format (e.g., CON06248)
  - Primary contract identifier from PeopleSoft
  - Links to Proposal ID in sponsored-proposals data
  - One contract has ~20 rows average (range: 1-291)
  - **MERGED CELLS - requires forward-fill within contract**

### Award Information
- **Award Title**: Full title of the sponsored project
  - Complete title (not abbreviated like in proposals data)
  - Can be 100+ characters with special characters
  - **MERGED CELLS - requires forward-fill within contract**

- **Award Status**: Current status of the award
  - Values: 'Active' or 'Closed'
  - Closed awards no longer incur new expenses (only corrections)
  - **MERGED CELLS - requires forward-fill within contract**

### PI Information
- **PI Name**: Current Principal Investigator
  - Format: "Last, First Middle" (e.g., "Smith, J Robert")
  - May differ from original PI if there was a change
  - Matches format in sponsored-proposals data
  - **MERGED CELLS - requires forward-fill within contract**

- **PI Department (if any)**: PI's HR home department
  - Different from project department (Syr Proj Deptid)
  - May be blank for non-departmental PIs
  - Matches Faculty by Unit data
  - **MERGED CELLS - requires forward-fill within contract**

- **PI Administrative Unit**: PI's school/college
  - 22 unique units (Arts & Sciences, Engineering, etc.)
  - HR administrative unit, not necessarily project unit
  - **MERGED CELLS - requires forward-fill within contract**

### Project Classification
- **Project Type**: Numeric code for project category
  - 310 = Federal-Research
  - 311 = Federal-Training  
  - 312 = Federal-Other
  - 320 = State-Research
  - 321 = State-Training
  - 322 = State-Other
  - 323 = State-HEOP Financial Aid
  - 340 = Private-Research
  - 341 = Private-Training
  - 342 = Private-Other
  - **MERGED CELLS - requires forward-fill within contract**

- **Syr Pt Descr**: Text description of Project Type
  - One-to-one mapping with Project Type code
  - Human-readable version of the numeric code
  - **MERGED CELLS - requires forward-fill within contract**

### Project Department (Authoritative for Expenditure)
- **Syr Proj Deptid**: 5-digit department ID where expense occurred
  - **PRIMARY KEY** - matches Comptroller's Chart of Accounts
  - Academic departments: 21xxx, 22xxx, 23xxx
  - Administrative: Other ranges
  - This is where the expense is charged, not PI's home dept
  - **MERGED CELLS - requires forward-fill within contract**

- **Syr Proj Deptid Descr**: Department name
  - Text description of Syr Proj Deptid
  - Examples: "Physics", "IVMF", "Burton Blatt Institute (BBI)"
  - **MERGED CELLS - requires forward-fill within contract**

- **SYR Proj Area**: Administrative area/unit code
  - Format: [###] Unit Name (e.g., "[218] Arts & Sciences")
  - First 3 digits correspond to Syr Proj Deptid prefix
  - Represents school/college/major unit
  - **MERGED CELLS - requires forward-fill within contract**

### Sponsor Information
- **Primary Sponsor Type**: Category of funding source
  - Federal Agencies (65.4% of FY25)
  - Not for Profit/Foundation (12.4%)
  - Corporations/Companies (9.9%)
  - New York State (7.8%)
  - Other Governmental/Public Sect (3.9%)
  - State - Other (0.3%)
  - University/College (0.2%)
  - **MERGED CELLS - requires forward-fill within contract**

- **Primary Sponsor**: Specific funding organization
  - 305 unique sponsors in FY25
  - Examples: "Department of Energy - Chicago", "Google, Inc"
  - **MERGED CELLS - requires forward-fill within contract**

### Federal Hierarchy (Federal Sponsors Only)
- **Federal Department**: Top-level federal agency
  - ONLY populated when Primary Sponsor Type = "Federal Agencies"
  - 21 unique departments (HHS, NSF, DoD, DOE, etc.)
  - Must be null for non-federal sponsors
  - **MERGED CELLS - requires forward-fill within contract**

- **Federal Subtier**: Federal sub-agency
  - ONLY for federal sponsors
  - 40 unique values, more specific than department
  - **MERGED CELLS - requires forward-fill within contract**

- **Federal Office**: Specific federal office
  - ONLY for federal sponsors
  - 54 unique offices, most granular level
  - **MERGED CELLS - requires forward-fill within contract**

### Expense Classification
- **Expense Category**: High-level expense type
  - DIRECT COSTS (82.7% of FY25)
  - INDIRECT COSTS (17.3% - F&A/overhead)
  - UNDEFINED ACCOUNT (0.4% - special categories)
  - **MERGED CELLS - requires global forward-fill**

- **Expense SubCategory**: Detailed expense type
  - Under DIRECT COSTS:
    - Salaries (largest - $35.6M in FY25)
    - Fringe Benefits
    - Travel
    - Equipment
    - Subcontracts
    - Other Direct Costs
    - Tuition and Stipends
  - Under INDIRECT COSTS:
    - Indirect Costs (F&A recovery)
  - Under UNDEFINED ACCOUNT:
    - Undefined Account
  - **MERGED CELLS - requires global forward-fill**

### Time Period
- **Expenditure Fiscal Year**: Syracuse fiscal year
  - Single value per file (e.g., 2025.0)
  - Float type, not integer
  - FY runs July 1 - June 30
  - **MERGED CELLS - requires global forward-fill**

- **Expenditure Month Abrevation**: Three-letter month code
  - Values: Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun
  - No forward-fill needed (populated for every row)
  - Fiscal year order: Jul is month 1, Jun is month 12

### Amount
- **Expenditure Amount**: Dollar amount of transaction
  - Can be positive or negative
  - Negative amounts are adjustments/corrections (normal, include in totals)
  - Range: typically -$500K to +$500K per transaction
  - No forward-fill needed (populated for every row)

## Data Quality Considerations

### Forward-Fill Requirements
**Critical**: Must forward-fill WITHIN each contract to prevent data bleeding between CONs:
1. First forward-fill Contract Num globally
2. Remove rows where Contract Num is still null
3. Forward-fill contract-level columns within each Contract Num group
4. Forward-fill global columns (Expense Category, SubCategory, Fiscal Year) across all rows
5. Clean Federal columns for non-federal sponsors (set to null)

### Common Issues
- **Negative amounts**: Normal corrections/adjustments - include in totals
- **Zero amounts**: Placeholder rows - can usually be filtered
- **Undefined accounts**: May indicate cost share or special funding
- **Federal data cleanup**: Must ensure Federal columns are null for non-federal sponsors
- **First 4 rows**: May have nulls even after forward-fill (no header to fill from)

### Hierarchical Structure
Each contract (CON) contains multiple levels:
1. Contract level (one per CON)
2. Expense Category level (2-3 per contract)
3. Expense SubCategory level (varies)
4. Monthly level (up to 12 per subcategory)

Average structure per contract:
- ~20 total rows
- 2-3 expense categories
- 4-6 subcategories
- Multiple months of transactions

### Cross-Reference Keys
- **Contract Num** -> Links to Proposal ID in sponsored-proposals skill
- **Syr Proj Deptid** -> Links to Department ID in su-chart-of-accounts skill
- **PI Name** -> Links to faculty in faculty-by-unit skill (with name variation handling)
- **Primary Sponsor** -> Consistent with sponsor names in sponsored-proposals
