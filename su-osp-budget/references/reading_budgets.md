# Reading OSP Budget Workbooks

This document describes how to correctly parse a completed OSP Budget Template workbook to extract all user-entered data.

## ⚠️ CRITICAL: Data Entry vs Formula Rows

### Non-personnel Sheet Row Map

| Rows | Section | Type | Notes |
|------|---------|------|-------|
| 7-13 | Equipment | DATA ENTRY ✓ | Up to 7 equipment items |
| **14** | **Equipment subtotal** | **FORMULA ✗** | DO NOT WRITE |
| **19** | **Domestic Travel** | **DATA ENTRY ✓** | Write/read here! |
| **20** | **Foreign Travel** | **DATA ENTRY ✓** | Write/read here! |
| **21** | **Total Travel** | **FORMULA ✗** | DO NOT WRITE - contains =SUM() |
| 22 | (Reserved) | — | Do not use |
| 25-28 | Participant Support | DATA ENTRY ✓ | Stipends, Travel, Subsistence, Other |
| **29** | **Participant Total** | **FORMULA ✗** | DO NOT WRITE |
| 34-37 | Direct Costs | DATA ENTRY ✓ | Materials, Pubs, Consultant, Purchased Svcs |
| **38** | **Subawards** | **FORMULA ✗** | Auto-calc from rows 70-88 |
| 39-43 | Direct Costs | DATA ENTRY ✓ | Rental, Alterations, Tuition, Human Subjects |
| 44-47 | Other (Custom) | DATA ENTRY ✓ | User-defined categories |
| **48** | **ODC subtotal** | **FORMULA ✗** | DO NOT WRITE |
| **52** | **Total Direct Costs** | **FORMULA ✗** | DO NOT WRITE |
| 57-61 | F&A Settings | **PARTIAL** | **Columns B and C ONLY** for Type/Rate |
| **66** | **F&A subtotal** | **FORMULA ✗** | DO NOT WRITE |
| 70, 72, 74, 76, 78, 80, 82, 84, 86, 88 | Subaward Detail | DATA ENTRY ✓ | Even rows only! |
| 71, 73, 75, 77, 79, 81, 83, 85, 87 | Subaward row totals | FORMULA ✗ | DO NOT WRITE |
| **90** | **Subaward Grand Total** | **FORMULA ✗** | DO NOT WRITE |

## Critical Lessons Learned

### 1. Personnel Name Columns
- **First Name**: Column C
- **Middle Name**: Column D (often empty)
- **Last Name**: Column E (NOT Column D!)

### 2. Travel Rows (Non-personnel Sheet)
- **Row 19**: Domestic Travel Costs - DATA ENTRY ROW
- **Row 20**: Foreign Travel Costs - DATA ENTRY ROW  
- **Row 21**: Total Travel Cost - FORMULA ROW (do not write here!)
- **Row 22**: EMPTY (do not confuse with foreign travel)

### 3. Year Columns
All sheets use the same column structure for year data:

| Year | Columns (Personnel) | Columns (Non-personnel costs) |
|------|--------------------|-----------------------------|
| Year 1 | H, I | H (or H:I for subawards) |
| Year 2 | J, K | J (or J:K for subawards) |
| Year 3 | L, M | L (or L:M for subawards) |
| Year 4 | N, O | N (or N:O for subawards) |
| Year 5 | P, Q | P (or P:Q for subawards) |

**Note**: Column T is always Justification for Non-personnel items.

### 4. Out-Year Personnel Changes
The most complex aspect of reading budgets is detecting out-year changes. Compare each Personnel Yr sheet:

**For each person row (7-14, 20-34 for Senior; 53-72 for Other):**
1. Compare Year N values to Year 1 values
2. If effort months (J, K, L) differ → effort change
3. If salary (M for Other) differs from escalated Y1 → salary change
4. If all months are 0 → person removed
5. If row has data in Year N but not Year 1 → person added

### 5. Multi-Year Equipment
Equipment (rows 7-14) can have costs in multiple years. Always check columns H, J, L, N, P for each row.

### 6. Personnel Changes with end_year
When a person is added with an end_year, they need an **explicit removal** record for subsequent years. The system does not automatically zero out cells when end_year expires.

## Cell Reference Guide

### Personnel Yr 1

#### Project Info (Row 5)
| Cell | Contents |
|------|----------|
| I5 | Start Date (e.g., "7/1/26") |
| K5 | Duration (years: 1-5) |
| O5 | Sponsor Type dropdown |

#### Senior Personnel (Rows 7-14, 20-34)
| Column | Contents |
|--------|----------|
| B | Prefix (Dr., etc.) |
| C | First Name |
| D | Middle Name |
| E | Last Name |
| F | Suffix |
| G | Role (dropdown) |
| H | Designation (dropdown) |
| I | Base Salary |
| J | Calendar Months |
| K | Academic Months |
| L | Summer Months |
| P | Justification |

#### Graduate Fringe Type (Row 43)
| Cell | Contents |
|------|----------|
| I43 | Sponsor Type (determines fringe rate) |

#### Other Personnel (Rows 53-72)
| Column | Contents |
|--------|----------|
| B | Prefix |
| C | First Name |
| D | Middle Name |
| E | Last Name |
| F | Suffix |
| G | Role (dropdown) |
| J | Calendar Months |
| K | Academic Months |
| L | Summer Months |
| M | Requested Salary |
| P | Justification |

### Non-personnel Sheet

#### Equipment (Rows 7-14)
| Column | Contents |
|--------|----------|
| B | Description |
| C-G | (part of merged description area) |
| H | Year 1 Cost |
| J | Year 2 Cost |
| L | Year 3 Cost |
| N | Year 4 Cost |
| P | Year 5 Cost |
| T | Justification |

#### Travel (Rows 19-20)
| Row | Type | Columns |
|-----|------|---------|
| 19 | Domestic | H/J/L/N/P for Y1-5, T for justification |
| 20 | Foreign | H/J/L/N/P for Y1-5, T for justification |
| 21 | Total | FORMULA - do not read/write |

#### Participant Support (Rows 25-28)
| Row | Type |
|-----|------|
| 25 | Stipends |
| 26 | Travel |
| 27 | Subsistence |
| 28 | Other |

Columns: H/J/L/N/P for Y1-5, T for justification

#### Other Direct Costs (Rows 34-47)
| Row | Type |
|-----|------|
| 34 | Materials and Supplies |
| 35 | Publication Costs |
| 36 | Consultant Services |
| 37 | Purchased Services |
| 38 | Subawards (auto-calculated from rows 70-88) |
| 39 | Rental/Lease |
| 40 | Alterations |
| 41 | Tuition - Remitted |
| 42 | Tuition - Scholarship |
| 43 | Human Subjects |
| 44-47 | Other (describe in column B) |

#### F&A Settings (Rows 57-61)
| Row | Year | Columns |
|-----|------|---------|
| 57 | Year 1 | B=Type, C=Rate |
| 58 | Year 2 | B=Type (or =B57), C=Rate |
| 59 | Year 3 | B=Type (or =B57), C=Rate |
| 60 | Year 4 | B=Type (or =B57), C=Rate |
| 61 | Year 5 | B=Type (or =B57), C=Rate |

#### Subaward Detail (Rows 70-88, even rows only)
| Column | Contents |
|--------|----------|
| B | Institution Name |
| H | Year 1 Direct Costs |
| I | Year 1 Indirect Costs |
| J | Year 2 Direct |
| K | Year 2 Indirect |
| L | Year 3 Direct |
| M | Year 3 Indirect |
| N | Year 4 Direct |
| O | Year 4 Indirect |
| P | Year 5 Direct |
| Q | Year 5 Indirect |
| T | Justification |

## Python Code for Reading Budgets

```python
from openpyxl import load_workbook

def read_osp_budget(filepath):
    """Read a completed OSP Budget Template and extract all user-entered data."""
    wb = load_workbook(filepath, data_only=False)
    
    budget = {
        'project_info': {},
        'senior_personnel': [],
        'other_personnel': [],
        'equipment': [],
        'travel': {'domestic': {}, 'foreign': {}},
        'participant_support': {},
        'other_direct_costs': {},
        'fa_settings': [],
        'subawards': [],
        'personnel_changes': []  # Out-year changes
    }
    
    # Read Personnel Yr 1
    p1 = wb['Personnel Yr 1']
    
    # Project Info
    budget['project_info'] = {
        'start_date': p1['I5'].value,
        'duration': p1['K5'].value,
        'sponsor_type': p1['O5'].value,
        'grad_fringe_type': p1['I43'].value
    }
    
    # Senior Personnel (rows 7-14, 20-34)
    for row in list(range(7, 15)) + list(range(20, 35)):
        first = p1[f'C{row}'].value
        last = p1[f'E{row}'].value  # Column E, not D!
        if first or last:
            budget['senior_personnel'].append({
                'row': row,
                'prefix': p1[f'B{row}'].value,
                'first_name': first,
                'middle': p1[f'D{row}'].value,
                'last_name': last,
                'suffix': p1[f'F{row}'].value,
                'role': p1[f'G{row}'].value,
                'designation': p1[f'H{row}'].value,
                'base_salary': p1[f'I{row}'].value,
                'cal_months': p1[f'J{row}'].value,
                'acad_months': p1[f'K{row}'].value,
                'sum_months': p1[f'L{row}'].value,
                'justification': p1[f'P{row}'].value
            })
    
    # Other Personnel (rows 53-72)
    for row in range(53, 73):
        first = p1[f'C{row}'].value
        last = p1[f'E{row}'].value  # Column E!
        if first or last:
            budget['other_personnel'].append({
                'row': row,
                'prefix': p1[f'B{row}'].value,
                'first_name': first,
                'middle': p1[f'D{row}'].value,
                'last_name': last,
                'suffix': p1[f'F{row}'].value,
                'role': p1[f'G{row}'].value,
                'cal_months': p1[f'J{row}'].value,
                'acad_months': p1[f'K{row}'].value,
                'sum_months': p1[f'L{row}'].value,
                'salary': p1[f'M{row}'].value,
                'justification': p1[f'P{row}'].value
            })
    
    # Non-personnel
    np = wb['Non-personnel']
    
    # Equipment (rows 7-14)
    for row in range(7, 15):
        desc = np[f'B{row}'].value
        y1 = np[f'H{row}'].value
        y2 = np[f'J{row}'].value
        y3 = np[f'L{row}'].value
        y4 = np[f'N{row}'].value
        y5 = np[f'P{row}'].value
        if desc or y1 or y2 or y3 or y4 or y5:
            budget['equipment'].append({
                'row': row,
                'description': desc,
                'y1': y1, 'y2': y2, 'y3': y3, 'y4': y4, 'y5': y5,
                'justification': np[f'T{row}'].value
            })
    
    # Travel - ROWS 19-20, not 21-22!
    budget['travel']['domestic'] = {
        'y1': np['H19'].value, 'y2': np['J19'].value, 'y3': np['L19'].value,
        'y4': np['N19'].value, 'y5': np['P19'].value,
        'justification': np['T19'].value
    }
    budget['travel']['foreign'] = {
        'y1': np['H20'].value, 'y2': np['J20'].value, 'y3': np['L20'].value,
        'y4': np['N20'].value, 'y5': np['P20'].value,
        'justification': np['T20'].value
    }
    
    # F&A (rows 57-61)
    for row in range(57, 62):
        fa_type = np[f'B{row}'].value
        fa_rate = np[f'C{row}'].value
        # Skip formula references
        if fa_type and not str(fa_type).startswith('='):
            budget['fa_settings'].append({
                'year': row - 56,
                'type': fa_type,
                'rate': fa_rate
            })
    
    # Detect out-year changes by comparing Personnel Yr 2, Yr 3, etc.
    for year in range(2, 6):
        sheet_name = f'Personnel Yr {year}'
        if sheet_name not in wb.sheetnames:
            continue
        py = wb[sheet_name]
        
        # Compare each person row to Year 1
        for person in budget['senior_personnel'] + budget['other_personnel']:
            row = person['row']
            section = 'senior' if row < 50 else 'other'
            
            # Get year N values
            val_j = py[f'J{row}'].value
            val_k = py[f'K{row}'].value
            val_l = py[f'L{row}'].value
            val_m = py[f'M{row}'].value if section == 'other' else None
            
            # Skip formula cells
            if val_j is not None and str(val_j).startswith('='):
                continue
            
            # Check for removal (all zeros)
            if val_j == 0 and val_k == 0 and val_l == 0:
                if val_m is None or val_m == 0:
                    budget['personnel_changes'].append({
                        'year': year,
                        'row': row,
                        'section': section,
                        'type': 'remove',
                        'person': f"{person['first_name']} {person['last_name']}"
                    })
                    continue
            
            # Check for modifications (values differ from expected escalation)
            # ... additional logic needed for salary comparison
    
    wb.close()
    return budget
```

## Common Parsing Errors to Avoid

1. **Wrong column for last name**: Use Column E, not Column D
2. **Wrong rows for travel**: Use rows 19-20, not 21-22
3. **Missing multi-year equipment costs**: Check all year columns, not just Year 1
4. **Ignoring out-year sheets**: Personnel Yr 2/3/4/5 contain critical changes
5. **Not handling explicit zeros**: A value of 0 is different from a formula
6. **Assuming formulas propagate removals**: When someone is added with end_year, you need explicit removal records
