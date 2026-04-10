# Proposal ID System - CORRECTED v1.2

## Critical Correction (v1.2)

**Multi-row CONs in Proposal Details = Multiple funding requests over time**

NOT budget splits, NOT multiple projects under one contract.

---

## CON Structure in Proposal Details

### One CON, Multiple Funding Requests

When a CON has multiple rows in Proposal Details, each row represents:
- A separate funding request submitted at different times
- Independent submission (may or may not have been funded)
- Own Submitted Date and Proposed Amount

**Example - CON04525 (HEOP):**
6 funding requests submitted 2021-2024:
- June 2021: $1,526,000 requested
- Feb 2022: $393,086 requested
- May 2022: $1,943,841 requested
- Dec 2022: $268,237 requested
- Apr 2023: $2,235,865 requested
- Mar 2024: $95,688 requested

**These are NOT summed** - each is an independent request.

### Merged Cells in Proposals

Only 3 columns have merged cells:
1. **Proposal ID** (CON##### or 3####) - Same for all requests under one CON
2. **Proposal Title** - Original proposal title
3. **Proposal Status** - Overall status (Funded/Not Funded/Pending)

**NOT merged**:
- Primary Project ID (only on first row)
- Submitted Date (each row has own date)
- Proposed Amount (each request has own amount)

---

## CON Structure in Award Details  

### One CON, Multiple Award Actions

Multiple rows = base award + supplements:
- Row 1: Base award (Award Label = "Anticipated Amount")
- Row 2+: Supplements (Award Label = "Supplement Amount" or blank)

**DO sum these** to get total anticipated award.

### Merged Cells in Awards

Only 2 columns have merged cells:
1. **Contract Num** - Same for base + all supplements
2. **Award Title** - Award title

**NOT merged**:
- Award Label (describes each row)
- Amounts (each supplement separate)
- Dates (each can differ)

---

## Primary Project ID (NEW Column 3 in Proposals)

**What it is:**
- CON-level identifier (not submission-specific)
- Shows the main/primary Project ID for this CON
- Renamed from "Project ID" for clarity

**Limitations:**
- Only populated for funded awards (44.7%)
- Only on first row of multi-row CONs
- Proposal data has NO project-level detail
- Cannot determine which submissions map to which Project IDs

**For project-level analysis**: Use Award Details (has Project ID with semicolons)

---

## Submitted Date (NEW Column 5 in Proposals)

**What it is:**
- Date when this specific funding request was submitted
- 100% populated
- Format: M/D/YYYY

**Use for:**
- Fiscal year assignment (actual submission date!)
- Tracking resubmissions over time
- Time-to-award analysis

**Multi-row CONs:**
- Each row has own Submitted Date
- Shows chronological history of requests

---

## CON vs InfoEd System

Unchanged from v1.0:
- CON##### = PeopleSoft (post-April 12, 2025 + all awarded)
- 3#### = InfoEd Inst # (pre-April 12, 2025 unfunded only)

---

## Key Insight

**Proposal Details** = Historical submission record
**Award Details** = Current authoritative award data

For funded awards, these serve DIFFERENT purposes:
- Proposals: When and how much was requested
- Awards: What was actually awarded and current status
