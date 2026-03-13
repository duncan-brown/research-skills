# Graduate Student Tuition - Budget Rows 41-42

## Quick Reference

| Row | Description | Regulatory Basis | MTDC Treatment | When to Use |
|-----|-------------|------------------|----------------|-------------|
| 41 | Tuition - Remitted | 2 CFR 200.466(b) | **Excluded** | Standard GRAs doing project work |
| 42 | Tuition - Scholarship | 2 CFR 200.466(a) | **Excluded** | Training grants, fellowships (NRSA, NASA) |

---

## Cell Structure

**Merged cells** (same pattern as Travel):
- Year 1: H:I (write to H)
- Year 2: J:K (write to J)
- Year 3: L:M (write to L)
- Year 4: N:O (write to N)
- Year 5: P:Q (write to P)
- Total: R:S (FORMULA - do not write)

**F41 Dropdown**: NOT useful - outdated values (FY24 rates). Enter tuition amounts directly in year columns.

See: `assets/images/dropdown_tuition_f41.png`

---

## Current Tuition Rate

**FY26 Graduate Tuition:**
- **$2,015 per credit hour**
- **18 credits per academic year** (full-time)
- **$36,270 per year**

**Escalation: 8.16% per year** (NOT 3% like salary)

| Year | Tuition | Calculation |
|------|---------|-------------|
| Y1 | $36,270 | Base rate |
| Y2 | $39,231 | $36,270 × 1.0816 |
| Y3 | $42,432 | $36,270 × 1.0816² |
| Y4 | $45,895 | $36,270 × 1.0816³ |
| Y5 | $49,640 | $36,270 × 1.0816⁴ |

---

## Regulatory Basis: 2 CFR 200.466

### Row 41 - Tuition Remitted (200.466(b))

**"Tuition remission and other forms of compensation paid as, or instead of, wages to students performing necessary work are allowable provided that:"**

1. The individual is conducting activities necessary to the Federal award
2. Tuition remission provided per established written policy of the IHE, consistently provided
3. Student is enrolled in advanced degree program, activities related to degree
4. Tuition or other payments are reasonable compensation for work performed

**Use for:** Standard Graduate Research Assistants (GRAs) working on the project

### Row 42 - Tuition Scholarship (200.466(a))

**"Costs of scholarships, fellowships, and student aid programs at IHEs are allowable only when the purpose of the Federal award is to provide training to participants, and the Federal agency approves the cost."**

**Use for:**
- NIH Training Grants (T32, etc.)
- Individual Fellowships (NIH NRSA F31/F32, NASA fellowships)
- Institutional training programs where training IS the purpose

### Key Distinction

| Factor | Row 41 (Remitted) | Row 42 (Scholarship) |
|--------|-------------------|----------------------|
| Purpose | Work on project | Training/education |
| Student role | GRA doing research | Trainee/fellow |
| Approval | Standard (per policy) | Agency must approve |
| Common awards | NSF, DOE, DOD research | NIH T32, NRSA, training |

---

## College-Specific Remission Policies

**CRITICAL: College determines how much tuition the PI must budget!**

### College of Arts and Sciences (A&S)

| Sponsor Type | F&A Rate | College Remission | PI Budgets |
|--------------|----------|-------------------|------------|
| Federal (full F&A) | 49.5% | **100%** | **$0** |
| Federal (reduced F&A) | <49.5% | Varies | Ask Dean |
| Non-federal | N/A | Use 55% fringe | $0 (in fringe) |

**Special rule:** Up to half tuition automatically authorized for grants at full F&A. Dean's signature NOT required. Note credits needed on IRR Question #3.

### College of Engineering and Computer Science (ECS)

| Sponsor Type | F&A Rate | College Remission | PI Budgets |
|--------------|----------|-------------------|------------|
| Federal | Any | **50%** | **$18,135/year** |
| Non-federal | N/A | 50% or use 55% fringe | Varies |

### All Other Schools/Colleges

**Default assumption: Follow ECS model (50% remission)**

- Confirm with Associate Dean for Research
- Schools include: Maxwell, iSchool, Whitman, Newhouse, FALK, VPA, etc.

### School of Education

| Sponsor Type | College Remission | PI Budgets |
|--------------|-------------------|------------|
| Federal | **0%** | **$36,270/year** |
| Non-federal | 0% or use 55% fringe | Varies |

---

## Information Needed from PI

When a PI mentions graduate students on a sponsored project, ask:

1. **Which college/school is the graduate student in?**
   - A&S: 100% remission (budget $0)
   - ECS: 50% remission (budget $18,135/year)
   - Education: 0% remission (budget $36,270/year)
   - Other: Assume ECS model, confirm with Associate Dean for Research

2. **Is this a training grant or fellowship?**
   - If YES → Use Row 42 (Tuition - Scholarship), requires A&S Dean signature
   - If NO → Use Row 41 (Tuition - Remitted)

**Already known from project setup:**
- Federal vs non-federal (from Sponsor Type)
- Project duration (for multi-year escalation)

---

## Budget Calculations by College

### A&S - Federal Grant (Full F&A)
```
Stipend: $28,750
Fringe (10.8%): $3,105
Tuition (Row 41): $0 (100% remitted)
---
MTDC: $31,855
F&A (49.5%): $15,768
Total: $47,623
```

### ECS - Federal Grant
```
Stipend: $28,750
Fringe (10.8%): $3,105
Tuition (Row 41): $18,135 (50% of $36,270)
---
MTDC: $31,855 (tuition excluded)
F&A (49.5%): $15,768
Total: $65,758
```

### Education - Federal Grant
```
Stipend: $28,750
Fringe (10.8%): $3,105
Tuition (Row 41): $36,270 (100%)
---
MTDC: $31,855 (tuition excluded)
F&A (49.5%): $15,768
Total: $83,893
```

**The college makes a $36,270/year difference!**

---

## Multi-Year Tuition Example (ECS, 3 years)

| Year | Base Tuition | PI's 50% Share | Calculation |
|------|--------------|----------------|-------------|
| Y1 | $36,270 | $18,135 | Base |
| Y2 | $39,231 | $19,616 | $18,135 × 1.0816 |
| Y3 | $42,432 | $21,216 | $18,135 × 1.0816² |
| **Total** | | **$58,967** | |

---

## Dean's Approval Process

### Row 41 (Tuition - Remitted)

**A&S:**
- Up to half auto-authorized at full F&A
- Note credits on IRR Question #3
- Dean's signature NOT required

**All Other Schools:**
- Dean's approval documented on IRR Question #3
- Requires Dean's signature

### Row 42 (Tuition - Scholarship)

**All Schools (including A&S):**
- A&S Dean or designee MUST sign IRR or send email confirmation to OSP
- Required for individual fellowships or institutional training grants

---

## Cost-Sharing Warning

**OSP strongly recommends NOT using tuition for cost-sharing:**
- Actual tuition charged is highly unpredictable
- Unmet cost-sharing must be covered from other sources
- If institutional resources contribute to tuition, sponsor and institution charged equal amounts concurrently

### Budget Justification Language

When college contributes to tuition:
- Describe as "institutional contribution"
- Do NOT include dollar value
- Do NOT identify as "cost-sharing"

---

## Non-Federal Sponsors

**If tuition is not allowable as a direct cost:**
- Cannot use the higher 55% GA fringe rate
- Must use federal fringe rate (10.8%)
- Check sponsor guidelines carefully

**If tuition IS allowable:**
- May charge as direct cost (Row 41), OR
- Use 55% fringe rate (which includes tuition component)
- Don't double-count!

---

## Summary: What to Enter

| Scenario | Row 41 Value | Row 42 Value |
|----------|--------------|--------------|
| A&S, federal, full F&A | $0 | $0 |
| ECS, federal | $18,135 (escalate 8.16%/yr) | $0 |
| Education, federal | $36,270 (escalate 8.16%/yr) | $0 |
| Other school, federal | $18,135 (confirm w/ Assoc Dean) | $0 |
| Training grant/fellowship | $0 | Full tuition (requires approval) |
| Non-federal, tuition allowed | Direct or in 55% fringe | - |
| Non-federal, tuition not allowed | $0, use 10.8% fringe | - |
