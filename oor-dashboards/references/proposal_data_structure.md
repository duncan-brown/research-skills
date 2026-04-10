# Sponsored Proposals Details - Column Analysis

## Data Overview
- **Total Records**: 3,664 proposals
- **Data Date**: November 23, 2025 (20251123)
- **Source**: Sponsored Proposals at Syracuse University dashboard

---

## Column Definitions & Analysis

### 1. **Proposal ID** (object) **[MERGED CELLS - REQUIRES FORWARD FILL]**
- **Critical**: This column contains merged cells; must forward-fill to get complete data
- **Format**: Two types
  - **CON#####** (PeopleSoft): 1,788 unique CONs containing 1,817 proposals
  - **3####** (InfoEd Inst #): 1,847 legacy proposals (5-digit, starts with 3)
- **Non-null after forward fill**: 3,664 (100%)

**Understanding CON vs Inst #:**
- **Post-April 12, 2025**: All proposals get a CON in PeopleSoft (regardless of award status)
- **Pre-April 12, 2025**: 
  - Awarded proposals -> CON in PeopleSoft
  - Not awarded proposals -> Inst # from InfoEd (legacy system)
  
**CON Structure:**
- One CON can contain multiple related proposals (e.g., amendments, phases, sub-projects)
- Each proposal has unique title, amount, and dates
- Multiple proposals under one CON typically share one Project ID
- 1,773 CONs have 1 proposal; 15 CONs have 2-10 proposals (max: 10)

**Examples:**
- Single-proposal CON: CON06743 (one proposal, one Project ID)
- Multi-proposal CON: CON04855 (10 proposals, one Project ID 5716)

**Data Loading Note:** Must forward-fill Proposal ID column like merged cell handling in faculty-by-unit

### 2. **Proposal Title** (object)
- **Example**: "Environmental Storytelling CNY: Land, Water, and the Right to Belong"
- **Non-null**: 3,663 (99.97%)
- **Notes**: Full descriptive title of the research proposal

### 3. **Proposal Status** (object)
- **Non-null**: 3,663 (99.97%)
- **Values**: 
  - Not Funded: 1,754 (47.9%)
  - Funded: 1,336 (36.5%)
  - Pending: 573 (15.6%)

### 4. **Award Project Start Date** (object)
- **Non-null**: 3,664 (100%)
- **Format**: "M/D/YYYY 12:00:00 AM" (e.g., "6/1/2026 12:00:00 AM")
- **For Pending proposals**: Proposed/anticipated start date (subject to change upon award)
- **For Funded proposals**: Actual start of expenditure period (when OSA allows charges against Project ID)
- **For Not Funded proposals**: Originally proposed start date
- **Fiscal Year Assignment**: This date is used to assign proposals to fiscal years (FY = July 1 - June 30)
  - [!] **Known Ambiguity**: The Tableau dashboard may use proposal submission date (not in this export) for FY assignment, so calculated FY totals from this data may not exactly match the dashboard. Clarification requested from DataInsights team (November 23, 2025).

### 5. **Award Project End Date** (object)
- **Non-null**: 3,664 (100%)
- **Format**: "M/D/YYYY 12:00:00 AM" (e.g., "5/31/2028 12:00:00 AM")
- **For Pending proposals**: Proposed/anticipated end date (subject to change upon award)
- **For Funded proposals**: Actual end of expenditure period (when OSA stops allowing charges against Project ID)
- **For Not Funded proposals**: Originally proposed end date
- **Notes**: For multi-project CONs, different Project IDs can have different start and end dates

### 6. **Instrument Type** (object)
- **Non-null**: 3,341 (91.2%)
- **Values**: 11 unique types
  - Grant: 1,419 (42.5%)
  - (blank): 924 (27.6%)
  - Subgrant (Prime = Grant): 429 (12.8%)
  - Contract: 277 (8.3%)
  - Inst Type - Grant: 102 (3.1%)
  - Subcontract (Prime = Contract): 98 (2.9%)
  - Inst Type - Contract: 32 (1.0%)
  - Cooperative Agreement: 30 (0.9%)
  - Inst Type - Subgrant: 23 (0.7%)
  - Inst Type - Subcontract: 6 (0.2%)
- **Notes**: Legal mechanism for funding; frequently blank

### 7. **Program Type** (object)
- **Non-null**: 3,662 (99.95%)
- **Values**: 10 unique types
  - Research - Basic: 2,386 (65.2%)
  - Other: 520 (14.2%)
  - Research: 410 (11.2%)
  - Instruction/Training: 217 (5.9%)
  - Research - Applied: 76 (2.1%)
  - Training: 25 (0.7%)
  - Research - Development: 10 (0.3%)
  - Research - Testing: 8 (0.2%)
  - (blank): 7 (0.2%)
  - Appropriation: Instruction/Training: 3 (0.1%)

### 8. **Project ID** (float64)
- **Example**: 7883.0, 7882.0, 7881.0
- **Non-null**: 1,675 (45.7%)
- **Unique**: 1,651 Project IDs
- **Notes**: Chart of Accounts Project ID for financial tracking (post-award)
  - Only present for **Funded** proposals that became active sponsored projects
  - Links to su-chart-of-accounts Project data
  - Multiple proposals under one CON typically share the same Project ID
  - NOT the same as Proposal ID; this is the financial tracking number
  - Format: 4-5 digit integer (not the CON number)

### 9. **PI Administrative Unit** (object)
- **Non-null**: 3,659 (99.9%)
- **Values**: 24 unique units
  - Engineering: 1,039 (28.4%)
  - Arts & Sciences: 1,000 (27.3%)
  - Maxwell: 474 (13.0%)
  - Falk: 306 (8.4%)
  - Veteran&Military Affairs: 177 (4.8%)
  - Information Studies: 129 (3.5%)
  - Education: 103 (2.8%)
  - Law: 72 (2.0%)
  - Office of Research: 70 (1.9%)
  - Newhouse: 54 (1.5%)
- **Notes**: School/college level; maps to faculty-by-unit UNIT field

### 10. **PI Deptid** (float64)
- **Example**: 21812.0, 21331.0, 22012.0
- **Non-null**: 3,659 (99.9%)
- **Unique**: 125 departments
- **Top departments**:
  - 21406: 305 proposals (Mechanical & Aerospace Eng)
  - 21404: 279 proposals (Electrical Eng & Computer Sci)
  - 21825: 261 proposals (Biology)
- **Notes**: Maps to Chart of Accounts DEPTID; can be looked up via su-chart-of-accounts skill

### 11. **PI Department (if any)** (object)
- **Example**: "Writing Program", "Ctr on Disability & Inclusion", "Center For Policy Research"
- **Non-null**: 3,659 (99.9%)
- **Notes**: Human-readable department name; may differ from Chart of Accounts department names

### 12. **PI Name** (object)
- **Example**: "Jones, Maria L", "Chen, Wei", "Williams, James"
- **Non-null**: 3,659 (99.9%)
- **Format**: "Last Name, First Name Middle Initial"
- **Notes**: Principal Investigator name; can be cross-referenced with faculty-by-unit data

### 13. **Primary Sponsor** (object)
- **Non-null**: 3,664 (100%)
- **Examples**: "National Geographic Society", "Spencer Foundation", "National Science Foundation"
- **Notes**: The ultimate source of funding; for subcontracts/subgrants, this is the prime sponsor

### 14. **Primary Sponsor Type** (object)
- **Non-null**: 3,664 (100%)
- **Values**: 9 types
  - Federal Agencies: 2,273 (62.0%)
  - Not for Profit/Foundation: 812 (22.2%)
  - Corporations/Companies: 227 (6.2%)
  - New York State: 178 (4.9%)
  - Foreign: 69 (1.9%)
  - Other Governmental/Public Sect: 57 (1.6%)
  - University/College: 37 (1.0%)
  - State - Other: 10 (0.3%)
  - European Organisation: 1 (<0.1%)

### 15. **Sponsor Name** (object)
- **Non-null**: 3,664 (100%)
- **Examples**: "National Geographic Society", "Cornell University", "Spencer Foundation"
- **Notes**: The direct contracting sponsor; for subcontracts/subgrants, this is the institution that contracts with SU (different from Primary Sponsor)

### 16. **Sponsor Type** (object)
- **Non-null**: 3,664 (100%)
- **Values**: 9 types (same categories as Primary Sponsor Type, different distribution)
  - Federal Agencies: 1,574 (43.0%)
  - Not for Profit/Foundation: 852 (23.3%)
  - University/College: 647 (17.7%) - *Higher than Primary Sponsor due to subcontracts*
  - Corporations/Companies: 325 (8.9%)
  - New York State: 136 (3.7%)
  - Foreign: 66 (1.8%)
  - Other Governmental/Public Sect: 59 (1.6%)
  - State - Other: 4 (0.1%)
  - European Organisation: 1 (<0.1%)

### 17. **Federal Department** (object)
- **Non-null**: 2,254 (61.5%)
- **Values**: 26 federal departments
  - National Science Foundation: 922 (40.9%)
  - Department Of Health And Human Services: 634 (28.1%)
  - Dept Of Defense: 212 (9.4%)
  - Department Of Energy: 111 (4.9%)
  - National Aeronautics And Space Administration: 64 (2.8%)
  - Department Of Agriculture: 58 (2.6%)
  - Environmental Protection Agency: 39 (1.7%)
  - The Institute Of Museum And Library Services: 36 (1.6%)
  - Department Of Education: 35 (1.6%)
  - National Endowment For The Humanities: 31 (1.4%)
- **Notes**: Only populated for federal proposals

### 18. **Federal Subtier** (object)
- **Non-null**: 2,254 (61.5%)
- **Examples**: "National Science Foundation", "National Institutes Of Health"
- **Notes**: Sub-agency level; only populated for federal proposals

### 19. **Federal Office** (object)
- **Non-null**: 2,254 (61.5%)
- **Examples**: "National Science Foundation", "National Institutes Of Health"
- **Notes**: Program office level; only populated for federal proposals

### 20. **Proposed Amount** (int64)
- **Non-null**: 3,664 (100%)
- **Format**: Integer (whole dollars)
- **Statistics**:
  - Mean: $545,715
  - Median: $183,501
  - Min: $0 (2 proposals)
  - Max: $36,766,360
  - 25th percentile: $42,627
  - 75th percentile: $504,118

**Interpretation by Proposal Status**:
- **Pending**: Amount requested from sponsor
- **Not Funded**: Amount that was requested (historical)
- **Funded**: Actual award amount for each Project ID

**Multi-Project CONs**:
- Each row shows amount for that specific Project ID
- **Total award to SU** = sum of all rows with same Proposal ID
- Example: CON04855 has 10 rows totaling $1,183,038

**Subcontracts/Subgrants**:
- Amount shown is **SU's portion only** (not the prime award total)
- Example: $34K subaward from UW-Madison on an HHS prime award

**Special Cases**:
- Supplements shown as separate rows (e.g., base + supplement)
- Two $0 amounts for pending proposals (likely TBD or in-kind only)

---

## Key Relationships & Notes

### Proposal ID System (Critical!)
**Two-Tiered System based on April 12, 2025 migration:**
- **InfoEd (pre-April 12, 2025)**: Legacy proposals not awarded keep Inst # (5-digit, starts with 3)
- **PeopleSoft (post-April 12, 2025)**: All proposals get CON regardless of status

**CON = Contract in PeopleSoft:**
- Tracks both pre-award (proposals) and post-award (contracts)
- One CON can contain multiple related proposals with different titles/amounts/dates
- All proposals in a CON typically share one Project ID (if awarded)
- 15 CONs (0.8%) contain 2-10 proposals; most (99.2%) contain 1 proposal

**Project ID = Financial Tracking:**
- Only appears after a proposal is awarded and becomes a sponsored project
- Links to Chart of Accounts for expense tracking
- Can be looked up in su-chart-of-accounts skill

### Sponsor vs Primary Sponsor
- **Primary Sponsor**: Ultimate funding source (e.g., NSF)
- **Sponsor Name**: Direct contracting entity (e.g., Cornell if SU is subcontractor)
- When Sponsor != Primary Sponsor -> This is a subcontract or subgrant

### Project ID Population
- Only ~46% of proposals have Project IDs
- Project IDs appear only for **Funded** proposals that became active sponsored projects
- Not Funded and Pending proposals generally lack Project IDs

### Federal Sponsor Fields
- Federal Department, Subtier, and Office only populated when Primary Sponsor Type = "Federal Agencies"
- These fields are blank for non-federal sponsors

### Date Format
- Dates stored as strings in "M/D/YYYY 12:00:00 AM" format
- Need to parse to datetime for date operations

### Department ID Mapping
- PI Deptid maps to Chart of Accounts Department IDs
- Can use su-chart-of-accounts skill for lookups
- PI Department names may not exactly match Chart of Accounts descriptions

### Faculty Mapping
- PI Name format: "Last Name, First Name Middle Initial"
- Can cross-reference with faculty-by-unit data using EMPLID
- Note: Not all PIs may be in faculty-by-unit (could be staff, administrators, or adjuncts)
