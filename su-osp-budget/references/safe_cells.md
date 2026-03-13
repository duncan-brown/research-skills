# OSP Budget Template - Safe Data Entry Cells

This document defines the ONLY cells that may be written to when populating the OSP Budget Template. All other cells contain formulas or protected content and must NOT be modified.

## Critical Rules

1. **NEVER write to gray cells** - these contain formulas
2. **NEVER write to columns M, N, O** in personnel sections (except M53-M72 for Other Personnel salary)
3. **Use EXACT dropdown values** - XLOOKUP requires exact matches
4. **Set I43 (Grad Fringe) BEFORE entering graduate assistants**

## Personnel Yr 1 Sheet

### Project Information (Row 5)

| Cell | Field | Type | Valid Values |
|------|-------|------|--------------|
| I5 | Start Date | Date/Text | e.g., "7/1/26" |
| K5 | Project Duration | Integer | 1, 2, 3, 4, 5 |
| O5 | Sponsor Type | Dropdown | "Federal - NIH", "Federal - Other", "Fnd/Prof Soc" |

### Senior Personnel - Primary (Rows 7-14)

For each row 7-14:

| Column | Field | Type | Notes |
|--------|-------|------|-------|
| B | Prefix | Text | Optional (Dr, Prof, etc.) |
| C | First Name | Text | Required for row 7 |
| D | Middle | Text | Optional |
| E | Last Name | Text | Required for row 7 |
| F | Suffix | Text | Optional |
| G | Project Role | Dropdown | "PI", "Co-PI", "Co-Investigator", "Senior/Key Personnel" |
| H | Designation | Dropdown | See Designation Values below |
| I | Base Salary | Number | Annual salary; enter capped amount if NIH cap applies |
| J | Cal Months | Number | For 12-month appointments (0-12) |
| K | Acad Months | Number | For 8.5-month appointments (0-8.5) |
| L | Sum Months | Number | Summer months (0-3.5) |
| P | Justification | Text | Free text; required if NIH cap applied |

**DO NOT WRITE TO: M, N, O (formula columns)**

### Senior Personnel - Additional (Rows 20-34)

Same structure as rows 7-14, for rows 20-34.

### Graduate Fringe Type (Row 43)

| Cell | Field | Type | Valid Values |
|------|-------|------|--------------|
| I43 | Grad Fringe | Dropdown | "Federal - NIH", "Federal - Other", "Fnd/Prof Soc" |

**CRITICAL: Must be set BEFORE entering Graduate Assistants or fringe will show #N/A**

### Other Personnel Detail (Rows 53-72)

For each row 53-72:

| Column | Field | Type | Notes |
|--------|-------|------|-------|
| B | Prefix | Text | Optional |
| C | First Name | Text | Required if row used |
| D | Middle | Text | Optional |
| E | Last Name | Text | Required if row used |
| F | Suffix | Text | Optional |
| G | Project Role | Dropdown | See Other Personnel Roles below |
| J | Cal Months | Number | For 12-month positions (postdocs, staff) |
| K | Acad Months | Number | For academic year positions |
| L | Sum Months | Number | Summer months |
| M | Requested Salary | Number | **USER ENTERS directly** (unlike Senior Personnel) |
| P | Justification | Text | Free text |

**DO NOT WRITE TO: N, O (formula columns)**

## Personnel Yr 2-5 Sheets

These sheets auto-populate from Year 1 with 3% escalation. Generally do NOT write to these unless:
- Salary changes differ from 3% escalation
- Effort changes in out years
- Personnel added/removed in out years

Safe cells follow same pattern as Personnel Yr 1.

### Out-Year Modification Rules

When modifying out-year personnel, you OVERWRITE formulas with values:

**To REMOVE a person (zero out effort):**
- Senior Personnel: Set J, K, L to 0 (salary formula will calculate to 0)
- Other Personnel: Set J, K, L AND M to 0 (M is manual entry, not formula)

**To MODIFY effort/FTE:**
- Change the relevant month columns (J, K, L) 
- For Other Personnel, also update M (Requested Salary)
- Calculate salary with appropriate escalation (Year 1 × 1.03^(year-1))

**To ADD a new person:**
- Write to C (First Name), E (Last Name)
- Write to G (Project Role - must match dropdown exactly)
- Write to appropriate month columns (J, K, L)
- For Other Personnel, write to M (Requested Salary)

**Important:** When adding in Year N but not Year N-1:
- Year N+1 formulas will reference Year N values (cascades forward)
- If person is temporary (e.g., undergrad for one year), zero out in subsequent years

### Out-Year Safe Cells

For Personnel Yr 2, 3, 4, 5:

**Senior Personnel (Rows 7-14, 20-34):**
- Can overwrite: J, K, L (months) - these override formulas
- Can overwrite: I (base salary) if different from escalated value
- DO NOT write to: M, N, O (these are calculated)

**Other Personnel Detail (Rows 53-72):**
- Can overwrite: J, K, L, M (months and salary)
- Can write: C, E, G for new personnel
- DO NOT write to: N, O (these are calculated)

## Non-personnel Sheet

### Complete Row Map — DATA ENTRY vs FORMULA

| Rows | Section | Type | Notes |
|------|---------|------|-------|
| 7-13 | Equipment | DATA ENTRY ✓ | Up to 7 equipment items |
| **14** | **Equipment subtotal** | **FORMULA ✗** | DO NOT WRITE |
| 15-18 | (Reserved) | — | |
| **19** | **Domestic Travel** | **DATA ENTRY ✓** | Write here! |
| **20** | **Foreign Travel** | **DATA ENTRY ✓** | Write here! |
| **21** | **Total Travel** | **FORMULA ✗** | DO NOT WRITE - contains =SUM() |
| 22 | (Reserved) | — | Do not use |
| 23-24 | Headers | — | |
| 25-28 | Participant Support | DATA ENTRY ✓ | Stipends, Travel, Subsistence, Other |
| **29** | **Participant Total** | **FORMULA ✗** | DO NOT WRITE |
| 30-33 | Headers/Reserved | — | |
| 34-37 | Direct Costs | DATA ENTRY ✓ | Materials, Pubs, Consultant, Purchased Svcs |
| **38** | **Subawards** | **FORMULA ✗** | Auto-calc from rows 70-88 |
| 39-43 | Direct Costs | DATA ENTRY ✓ | Rental, Alterations, Tuition, Human Subjects |
| 44-47 | Other (Custom) | DATA ENTRY ✓ | User-defined categories |
| **48** | **ODC subtotal** | **FORMULA ✗** | DO NOT WRITE |
| 49-51 | Reserved | — | |
| **52** | **Total Direct Costs** | **FORMULA ✗** | DO NOT WRITE |
| 53-56 | Reserved | — | |
| 57-61 | F&A Settings | **PARTIAL** | **Columns B and C ONLY** for Type/Rate dropdowns |
| 62-65 | Reserved | — | Do not use |
| **66** | **F&A subtotal** | **FORMULA ✗** | DO NOT WRITE |
| 67-69 | Reserved | — | |
| 70-88 (even) | Subaward Detail | DATA ENTRY ✓ | 10 subaward slots |
| 71-87 (odd) | Subaward Totals | FORMULA ✗ | DO NOT WRITE |
| 89 | Reserved | — | |
| **90** | **Subaward Grand Total** | **FORMULA ✗** | DO NOT WRITE |

### ⚠️ FORMULA ROWS - DO NOT WRITE ⚠️

The following rows contain formulas and must NEVER be written to:

| Row | Purpose | Contains |
|-----|---------|----------|
| 14 | Equipment subtotal | Formula summing rows 7-13 |
| 21 | **Total Travel Cost** | `=SUM(H19:I20)` formula - sums domestic + foreign |
| 29 | Total Participant Support | Formula summing rows 25-28 |
| 38 | Subawards Total | Formula from subaward detail (rows 70-88) |
| 48 | Other Direct Costs subtotal | Formula row |
| 52 | Total Direct Costs | Formula row |
| 57 | F&A Year 1 row | **EXCEPTION: Columns B and C are DATA ENTRY** |
| 66 | F&A subtotal | Formula row |
| 90 | Subaward grand total | Formula summing all subawards |

**CRITICAL DISTINCTIONS:**
- **Row 19**: Domestic Travel - DATA ENTRY ✓
- **Row 20**: Foreign Travel - DATA ENTRY ✓  
- **Row 21**: Total Travel - FORMULA ✗ (DO NOT WRITE!)
- **Row 57**: F&A Settings - **Columns B and C ONLY** are DATA ENTRY ✓

### Equipment (Rows 7-14)

| Column | Field | Years |
|--------|-------|-------|
| B-G | Equipment Description | Text (merged cells) |
| H | Year 1 Amount | Number |
| I | Year 1 Amount (overflow) | Number |
| J | Year 2 Amount | Number |
| K | Year 2 Amount (overflow) | Number |
| L-Q | Years 3-5 | Same pattern |

**Equipment Rules:**

1. **Threshold**: Total cost must be ≥$5,000 (items below this are Supplies, Row 34)
2. **Total cost** is what matters - fabricated equipment can be spread across years
3. **Include ALL costs** to make equipment functional:
   - Purchase price
   - Shipping/freight
   - Installation
   - Renovation required for installation
4. **Must be essential** for successful performance of the project
5. **F&A treatment**: Equipment is EXCLUDED from MTDC base (no F&A charged)

### Travel (Rows 19-20) — DATA ENTRY ROWS

**⚠️ CRITICAL: Write to rows 19-20 ONLY. Row 21 is a FORMULA row!**

| Row | Description | Columns | Type |
|-----|-------------|---------|------|
| 19 | Domestic Travel | H (Yr1), J (Yr2), L (Yr3), N (Yr4), P (Yr5), T (Justification) | DATA ENTRY ✓ |
| 20 | Foreign Travel | H (Yr1), J (Yr2), L (Yr3), N (Yr4), P (Yr5), T (Justification) | DATA ENTRY ✓ |
| 21 | Total Travel Cost | Formula: =SUM(rows 19-20) | FORMULA - DO NOT WRITE ✗ |
| 22 | (Reserved) | Empty | DO NOT USE ✗ |

### Participant/Trainee Support (Rows 25-28) — DATA ENTRY ROWS

**⚠️ Row 29 is a FORMULA row (total) - do not write to it!**

| Row | Description | Columns | Type |
|-----|-------------|---------|------|
| 25 | Stipends | H, J, L, N, P, T (Justification) | DATA ENTRY ✓ |
| 26 | Travel | H, J, L, N, P, T (Justification) | DATA ENTRY ✓ |
| 27 | Subsistence | H, J, L, N, P, T (Justification) | DATA ENTRY ✓ |
| 28 | Other | H, J, L, N, P, T (Justification) | DATA ENTRY ✓ |
| D29 | Number of Participants | Number | DATA ENTRY ✓ |
| 29 | Total Participant Support | Formula | FORMULA - DO NOT WRITE ✗ |

### Other Direct Costs (Rows 34-47)

| Row | Description | Columns |
|-----|-------------|---------|
| 34 | Materials and Supplies | H, J, L, N, P |
| 35 | Publication Costs | H, J, L, N, P |

**Materials and Supplies Notes (Row 34):**
- Items under $5,000 (≥$5,000 = Equipment)
- **Computers**: Generally NOT allowable if for general use. Must be specifically for the project (e.g., workstation for postdoc doing computational work). General-purpose PI computers used for teaching/service are NOT allowable.
- Encourage semi-detailed justifications for budget justification text

**Publication Costs Notes (Row 35):**
- Open access fees (APCs), page charges allowable per 2 CFR 200.461
- Can charge during closeout even if paper published after award ends

| 36 | Consultant Services | H, J, L, N, P |
| 37 | Purchased Services | H, J, L, N, P |
| 38 | Subawards | AUTO-CALCULATED from rows 70-88 |
| 39 | Rental/Lease | H, J, L, N, P |
| 40 | Alterations | H, J, L, N, P |

**Consultant Services Notes (Row 36):**
- Individual with specialized expertise providing advisory services
- Requires OSP Consulting Agreement
- Document: service description, days of service, daily rate, travel
- Per 2 CFR 200.459 - must be "reasonable in relation to services rendered"
- NSF: No rate limit (since FY06). Other agencies: varies (see consultant_contractor_rental.md)
- Included in MTDC (F&A applies)

**Purchased Services Notes (Row 37):**
- Routine goods/services from vendors (NOT programmatic work)
- Follows Procurement process (NOT OSP)
- Examples: core facilities, equipment repair, analytical testing, printing
- Micro-purchase ≤$10K: no competitive quotes required
- Simplified acquisition $10K-$250K: quotes from adequate sources
- Included in MTDC (F&A applies)

**Rental/Lease Notes (Row 39):**
- Per 2 CFR 200.465 - rates must be reasonable (comparable, market conditions)
- Arm's-length lease: reasonable rental payments allowable
- Less-than-arm's-length lease: limited to depreciation/maintenance/taxes/insurance
- Example: Burton Blatt Institute rents space for SE-ADA Center (HHS grant)
- Home office space is UNALLOWABLE
- Included in MTDC (F&A applies)

**Alterations Notes (Row 40):**
- **REQUIRES Vice President for Research approval**
- PIs should NOT budget for alterations without prior VPR discussion
- If PI asks to add Alterations, direct them to contact: **vpr@syr.edu**

| 41 | Tuition - Remitted | H, J, L, N, P |
| 42 | Tuition - Scholarship | H, J, L, N, P |

**Tuition Notes (Rows 41-42):**
- **Merged cells**: H:I, J:K, L:M, N:O, P:Q (write to first cell of each pair)
- **F41 dropdown is NOT useful** - outdated values (FY24), enter tuition directly
- **Excluded from MTDC** (no F&A)
- **Escalate 8.16% per year** (NOT 3% like salary)
- Current rate: $36,270/year ($2,015/credit × 18 credits)

**Row 41 (Tuition - Remitted)** - per 2 CFR 200.466(b):
- Standard GRAs doing project work
- College remission varies:
  - A&S: 100% remission → budget $0
  - ECS: 50% remission → budget $18,135
  - Education: 0% remission → budget $36,270
  - Other schools: Assume ECS model (confirm with Associate Dean for Research)

**Row 42 (Tuition - Scholarship)** - per 2 CFR 200.466(a):
- Training grants (T32), fellowships (NRSA, NASA)
- Purpose of award IS training
- Requires A&S Dean signature (all schools)

| 43 | Human Subject | H, J, L, N, P |

**Human Subject Notes (Row 43):**
- Payments to **research subjects** (NOT participants in workshops/training)
- Per 2 CFR 200.456 - payments for time and inconvenience
- **OSA escrows funds until IRB approval** - no expenditures before IRB approved
- **Included in MTDC** (F&A applies) - different from Participant Support
- IRB must approve incentive amounts (to avoid undue influence)
- Tax reporting:
  - US persons: W-9 required, 1099-MISC if ≥$600/calendar year
  - Non-resident aliens: W-8BEN required, **30% withholding** (unless treaty exception)
- Account: 561104 (Sponsored Subjects)
- See `references/human_subjects.md` for full documentation

### Other Direct Costs - Generic (Rows 44-47)

| Row | Columns | Content |
|-----|---------|---------|
| 44 | B | Description (user-defined) |
| 44 | H, J, L, N, P | Years 1-5 amounts |
| 45 | B | Description (user-defined) |
| 45 | H, J, L, N, P | Years 1-5 amounts |
| 46 | B | Description (user-defined) |
| 46 | H, J, L, N, P | Years 1-5 amounts |
| 47 | B | Description (user-defined) |
| 47 | H, J, L, N, P | Years 1-5 amounts |

**Purpose:** Catch-all rows for allowable direct costs that don't fit predefined categories.

**F&A Treatment:** Generally included in MTDC unless the cost type is specifically excluded.

**Common Uses:**
- Software licenses (if not equipment)
- Conference registration fees (if not part of travel)
- Service contracts
- Communication costs (if unusual)
- Other specialized costs

**Note:** Use descriptive text in Column B so reviewers understand the cost.

### F&A Rate (Rows 57-61)

**Structure:**

| Row | Year | F&A Type (Column B) | F&A Rate (Column C) |
|-----|------|---------------------|---------------------|
| 57 | 1 | Dropdown | Dropdown |
| 58 | 2 | Dropdown | Dropdown |
| 59 | 3 | Dropdown | Dropdown |
| 60 | 4 | Dropdown | Dropdown |
| 61 | 5 | Dropdown | Dropdown |

**CRITICAL: F&A Rate Must Be Same Across All Years**

While the template allows setting different F&A rates for each year, this should **ALMOST NEVER** happen.

- **Default behavior:** Set B57 and C57, all other years should match
- **If user wants different rates year-to-year:** Requires VPR approval (vpr@syr.edu)
- **If University's negotiated rate changes:** Since SU uses "actual rates in place at time will be charged" language, it's OK to budget the same rate throughout

**F&A Type Values (Column B):**
```
"MTDC-Fed"      - Federal sponsors using MTDC
"MTDC-NonFed"   - Non-federal or sponsor-capped rates
"TDC"           - Total Direct Costs (rare)
"SWFB"          - Salaries, Wages, Fringe Benefits only (rare)
```

**F&A Rate Values (Column C):**
```
"Research - On Campus - 49.50%"      - Most federal research
"Instruction - On Campus - 34.00%"   - Training/instruction grants
"Other - On Campus - 35.00%"         - Other sponsored activities
"Research - Off Campus - 26.00%"     - >50% off-campus
"Instruction - Off Campus - 26.00%"
"Other - Off Campus - 26.00%"
```

**Sponsor-Capped Rates:**
If sponsor caps F&A below negotiated rate:
1. Set B57 to "MTDC-NonFed"
2. Enter numeric rate in C57 (Excel will warn "This is not one of the Approved Rates" - click Yes)

See `assets/images/fa_rate_rows_57_61.png` and `assets/images/fa_rate_warning_dialog.png`

### Subawards (Rows 70-88, even rows only)

**Structure:** 10 subaward slots on even rows (70, 72, 74, 76, 78, 80, 82, 84, 86, 88)

| Row | Subaward # | Column B | Columns H-Q | Column T |
|-----|------------|----------|-------------|----------|
| 70 | 1 | Institution name | Direct/Indirect by year | Justification |
| 72 | 2 | Institution name | Direct/Indirect by year | Justification |
| 74 | 3 | Institution name | Direct/Indirect by year | Justification |
| 76 | 4 | Institution name | Direct/Indirect by year | Justification |
| 78 | 5 | Institution name | Direct/Indirect by year | Justification |
| 80 | 6 | Institution name | Direct/Indirect by year | Justification |
| 82 | 7 | Institution name | Direct/Indirect by year | Justification |
| 84 | 8 | Institution name | Direct/Indirect by year | Justification |
| 86 | 9 | Institution name | Direct/Indirect by year | Justification |
| 88 | 10 | Institution name | Direct/Indirect by year | Justification |

**Column detail for each row:**

| Column | Content | Write? |
|--------|---------|--------|
| B-F | Institution name (merged) | Write to B |
| G | Spacer | No |
| H | Year 1 Direct | Yes |
| I | Year 1 Indirect | Yes |
| J | Year 2 Direct | Yes |
| K | Year 2 Indirect | Yes |
| L | Year 3 Direct | Yes |
| M | Year 3 Indirect | Yes |
| N | Year 4 Direct | Yes |
| O | Year 4 Indirect | Yes |
| P | Year 5 Direct | Yes |
| Q | Year 5 Indirect | Yes |
| R | Total Direct | **FORMULA - do not write** |
| S | Total Indirect | **FORMULA - do not write** |
| T | Justification | Yes |

**Row 90:** Totals (FORMULA - do not write)

**Row 38:** Auto-populated from subaward detail (FORMULA - do not write)

**F&A / MTDC Rule:**
- First $25,000 of each subaward: Included in MTDC (F&A applies)
- Amount above $25,000: Excluded from MTDC (no F&A)
- Template calculates this automatically - just enter full Direct and Indirect amounts

**What to enter:**
- Collaborators provide their own budgets with their institutional rates
- Enter their Direct and Indirect costs as provided
- Don't recalculate using SU's rates

See `references/subawards.md` for full documentation

## Dropdown Value Reference

### Designation (Senior Personnel - Column H)

```
"Tenure/Track Faculty - Acad/Sum"
"Tenure/Track Faculty - Calendar"
"Non-Tenure Track Faculty - Full Time"
"Non-Tenure Track Faculty - Hourly"
"Senior Research Associate (Staff)"
"Qualified Staff Non-Ph.D."
```

### Project Role - Senior (Column G, Rows 7-34)

```
"PI"
"Co-PI"
"Co-Investigator"
"Senior/Key Personnel"
```

### Project Role - Other Personnel (Column G, Rows 53-72)

```
"Postdoctoral Associates"
"Research Associate - Full Time"
"Research Associate - Hourly"
"Other Professional Staff"
"Graduate Assistants"
"Hourly Students (Grad/Undergrad)"
"Secretarial/Clerical"
"Other (Temp, wages)"
"Extra Service & Overload"
"Adjunct Faculty"
```

### Sponsor Type / Grad Fringe (O5 / I43)

```
"Federal - NIH"
"Federal - Other"
"Fnd/Prof Soc"
```

### F&A Type (B57)

```
"MTDC-Fed"
"MTDC-NonFed"
"TDC"
"SWFB"
```

### F&A Rate (C57)

```
"Research - On Campus - 49.50%"
"Instruction - On Campus - 34.00%"
"Other - On Campus - 35.00%"
"Research - Off Campus - 26.00%"
"Instruction - Off Campus - 26.00%"
"Other - Off Campus - 26.00%"
```

## Verification Checklist

Before saving a populated workbook, verify:

1. [ ] All dropdown values are EXACT matches (case-sensitive)
2. [ ] I43 (Grad Fringe) is set if any Graduate Assistants entered
3. [ ] O5 (Sponsor Type) matches I43 (Grad Fringe)
4. [ ] No formula cells (gray cells) were modified
5. [ ] Row 7 has PI entered (required)
6. [ ] For NIH: salary caps applied and justification text added
7. [ ] For NSF: senior personnel total ≤ 2 months

## Account Code Mapping

For reference, these are the account codes that map to each role (used in SAMTool):

| Role | OSA Code | Account |
|------|----------|---------|
| Tenure/Track Faculty - Acad/Sum | PROFAY/PROFSM | 500011/530011 |
| Tenure/Track Faculty - Calendar | PROFCAL | 511005 |
| Non-Tenure Track Faculty - Full Time | SRFULL | 500013 |
| Non-Tenure Track Faculty - Hourly | SRHLY | 520010 |
| Senior Research Associate (Staff) | SRRA | 513005 |
| Qualified Staff Non-Ph.D. | SRCAL | 512002 |
| Postdoctoral Associates | OTPDR | 513001 |
| Research Associate - Full Time | RAFULL | 513002 |
| Research Associate - Hourly | RAHRLY | 544074 |
| Other Professional Staff | OTFUL | 513021 |
| Graduate Assistants | GRADST | 503259 |
| Hourly Students | OTUGR | 549976 |
| Secretarial/Clerical | CLERK | N/A |
| Other (Temp, wages) | OTTMP | 543021 |
| Extra Service & Overload | OTESO | 549979 |
| Adjunct Faculty | OTADJ | 500214 |
