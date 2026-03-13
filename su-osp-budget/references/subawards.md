# Subawards / Subcontracts (Row 38 + Rows 70-88)

## Overview

Subawards are entered in the detail section (Rows 70-88) and automatically populate Row 38 in Other Direct Costs. The template calculates F&A correctly, applying it only to the first $25,000 of each subaward per 2 CFR 200.

**Key principle:** F&A is only charged on the first $25,000 of each subaward. Amounts above $25K are excluded from MTDC.

---

## SU Process

1. **PI works with collaborators** at subcontracting institutions
2. **Collaborators develop their own budgets** according to:
   - Flow-through requirements from the prime award to SU
   - Their own institutional rates (F&A, fringe)
   - Sponsor guidelines
3. **Collaborators provide budgets to SU PI** showing:
   - Direct costs by year
   - Indirect costs by year (using their negotiated F&A rate)
4. **PI enters Direct and Indirect** for each subawardee in Rows 70-88
5. **Row 38 auto-populates** with totals
6. **F&A calculation** automatically handles the $25K MTDC rule

---

## Cell Structure (Rows 70-88)

### Available Rows

| Row | Subaward # | Excel Row |
|-----|------------|-----------|
| 70 | 1 | First subawardee |
| 72 | 2 | Second subawardee |
| 74 | 3 | Third subawardee |
| 76 | 4 | Fourth subawardee |
| 78 | 5 | Fifth subawardee |
| 80 | 6 | Sixth subawardee |
| 82 | 7 | Seventh subawardee |
| 84 | 8 | Eighth subawardee |
| 86 | 9 | Ninth subawardee |
| 88 | 10 | Tenth subawardee |

**Note:** Only even rows are used (70, 72, 74...). Odd rows (71, 73, 75...) are not data entry rows.

### Column Structure

| Column(s) | Content | Write To |
|-----------|---------|----------|
| B-F | Institution name (merged) | B |
| G | Spacer | - |
| H | Year 1 Direct | H |
| I | Year 1 Indirect | I |
| J | Year 2 Direct | J |
| K | Year 2 Indirect | K |
| L | Year 3 Direct | L |
| M | Year 3 Indirect | M |
| N | Year 4 Direct | N |
| O | Year 4 Indirect | O |
| P | Year 5 Direct | P |
| Q | Year 5 Indirect | Q |
| R | Total Direct | FORMULA - do not write |
| S | Total Indirect | FORMULA - do not write |
| T | Justification | T |

### Row 90: Totals

Row 90 contains formulas that sum all subaward entries. Do not write to this row.

---

## F&A / MTDC Treatment

### The $25,000 Rule

**Syracuse University Context:** Syracuse follows our federally negotiated rate agreement (DHHS, dated June 4, 2024), which uses the $25,000 threshold per OMB regulations in effect at the time of negotiation. We will continue using $25,000 until our NICRA is renegotiated or we receive further guidance from OMB. This has been accepted by federal sponsors including NSF.

Per Syracuse University's current indirect cost rate agreement:

> "MTDC excludes... the portion of each subaward in excess of $25,000."

**This means:**
- First $25,000 of each subaward: **Included in MTDC** (F&A applies)
- Amount above $25,000: **Excluded from MTDC** (no F&A)

### How the Template Handles This

The template automatically:
1. Sums Direct + Indirect for each subaward by year
2. Calculates total per subaward across all years
3. Includes first $25K in MTDC base
4. Excludes remainder from MTDC base

**You don't need to split this manually** - just enter the full Direct and Indirect amounts.

### Example Calculation

**Subaward to Caltech: $150,000 total ($120,000 Direct + $30,000 Indirect)**

| Component | Amount | In MTDC? |
|-----------|--------|----------|
| First $25,000 | $25,000 | Yes |
| Remaining $125,000 | $125,000 | No |

SU's F&A (49.5%) applies only to $25,000 = $12,375 in F&A

---

## What Collaborators Should Provide

Ask collaborators for:

1. **Budget by year** showing:
   - Direct costs (personnel, supplies, travel, etc.)
   - Indirect costs (using their F&A rate)

2. **Budget justification** explaining:
   - Personnel (name, role, effort, salary)
   - Other costs

3. **Required documents for proposal:**
   - Subrecipient Commitment Form OR signed letter of intent
   - Statement of Work (PI, period, tasks, milestones)
   - Biosketches, Current & Pending (if required by sponsor)

### Sample Collaborator Budget Format

```
Institution: California Institute of Technology
Period: 7/1/2026 - 6/30/2029 (3 years)

                    Year 1      Year 2      Year 3      Total
Personnel           $45,000     $46,350     $47,741     $139,091
Fringe (25%)        $11,250     $11,588     $11,935     $34,773
Travel              $3,000      $3,000      $3,000      $9,000
Supplies            $5,000      $5,000      $5,000      $15,000
-----------------------------------------------------------------
Total Direct        $64,250     $65,938     $67,676     $197,864
Indirect (54%)      $34,695     $35,607     $36,545     $106,847
-----------------------------------------------------------------
TOTAL               $98,945     $101,545    $104,221    $304,711
```

### What PI Enters in Template

From the example above:

| Row 70 | Column | Value |
|--------|--------|-------|
| Institution | B | California Institute of Technology |
| Y1 Direct | H | 64250 |
| Y1 Indirect | I | 34695 |
| Y2 Direct | J | 65938 |
| Y2 Indirect | K | 35607 |
| Y3 Direct | L | 67676 |
| Y3 Indirect | M | 36545 |

---

## Multiple Subawards

If a project has multiple subawardees, each gets their own row:

| Row | Institution | Y1 Direct | Y1 Indirect | ... |
|-----|-------------|-----------|-------------|-----|
| 70 | Caltech | 64,250 | 34,695 | ... |
| 72 | MIT | 50,000 | 27,000 | ... |
| 74 | U of Michigan | 35,000 | 17,500 | ... |

**Each subaward gets its own $25K MTDC inclusion.** So with 3 subawards:
- Up to $75,000 total could be in MTDC (3 × $25K)

---

## Budget Justification

For each subaward, the justification (Column T or separate document) should include:

1. **Subawardee institution and PI**
2. **Role/contribution** to the project
3. **Summary of costs** (can reference attached detailed budget)
4. **Why subaward** (vs. consultant or contractor)

**Example:**
"Subaward to California Institute of Technology (Dr. Jane Smith, PI): $304,711 total costs over 3 years. Caltech will perform gravitational wave data analysis and develop signal processing algorithms. Dr. Smith is a leading expert in matched filtering techniques. See attached Caltech budget and statement of work."

---

## Subrecipient vs. Contractor Reminder

Subawards are for **subrecipients** who:
- Carry out substantive programmatic work
- Have programmatic decision-making responsibility
- Are measured against project objectives
- Are subject to Federal compliance requirements

If the entity is providing routine goods/services → use **Purchased Services (Row 37)** instead.

See `references/consultant_contractor_rental.md` for the full decision tree.

---

## Common Issues

### 1. Collaborator Uses Different F&A Rate

**This is expected.** Each institution has its own negotiated F&A rate. Enter their numbers as provided.

### 2. Collaborator's Budget Doesn't Match SU's Years

If subaward period differs from SU's, align costs to SU's budget years. May need to prorate.

### 3. Subaward Starts in Year 2

Enter $0 for Year 1, then actual amounts starting in Year 2.

### 4. More Than 10 Subawards

The template supports 10 subawards maximum. If you have more, contact OSP - this is unusual and may require special handling.

### 5. Foreign Subaward

Additional requirements may apply:
- Export control review
- Foreign entity documentation
- Some sponsors restrict foreign subawards (check NOFO)

---

## Quick Entry Reference

**To add a subaward:**

1. Find next available even row (70, 72, 74...)
2. Write institution name to column B
3. Write Direct costs to H, J, L, N, P (for years used)
4. Write Indirect costs to I, K, M, O, Q (for years used)
5. Optionally add justification to column T

**Do NOT write to:**
- Columns R, S (Total formulas)
- Row 90 (Sum formulas)
- Row 38 (Auto-populated from detail)

---

## Verification

After entering subawards:
1. Check Row 38 shows correct total
2. Verify F&A calculation in Rows 57-61 area reflects $25K rule
3. Cross-check totals against collaborator budgets
