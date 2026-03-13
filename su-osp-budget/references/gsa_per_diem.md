# GSA Per Diem Rates Reference

## Overview

Federal grants require travel costs to comply with GSA per diem rates. Per diem covers:
- **Lodging**: Maximum nightly hotel rate
- **M&IE**: Meals and Incidental Expenses (daily allowance)

## Files in Skill Assets

- `FY2026_PerDiemMasterRatesFile.xlsx` - Current FY rates (Oct 1, 2025 - Sep 30, 2026)
- `FY2025_PerDiemMasterRatesFile.xlsx` - Previous FY rates
- `FY2025PerDiemRatesHighlights.docx` - Explanation of per diem system
- `FY_2025_MIE_Breakdown.docx` - M&IE breakdown by tier

## Per Diem File Structure

The Excel files have these columns:
- Column A: ID
- Column B: STATE (2-letter code)
- Column C: DESTINATION (city name)
- Column D: COUNTY/LOCATION DEFINED
- Column E: SEASON BEGIN
- Column F: SEASON END
- Column G: Lodging Rate
- Column H: M&IE Rate

**Row 3** contains the Standard CONUS rate for non-listed locations:
- Lodging: $110/night
- M&IE: $68/day

## Looking Up Rates

```python
from openpyxl import load_workbook

def lookup_per_diem(city, state, fiscal_year=2026):
    """Look up GSA per diem rates for a city."""
    wb = load_workbook(f'assets/FY{fiscal_year}_PerDiemMasterRatesFile.xlsx')
    sheet = wb.active
    
    results = []
    for row in range(4, 600):
        row_state = sheet.cell(row=row, column=2).value
        row_city = sheet.cell(row=row, column=3).value
        
        if row_state == state and row_city and city.lower() in str(row_city).lower():
            results.append({
                'city': row_city,
                'season_begin': sheet.cell(row=row, column=5).value,
                'season_end': sheet.cell(row=row, column=6).value,
                'lodging': sheet.cell(row=row, column=7).value,
                'mie': sheet.cell(row=row, column=8).value
            })
    
    # Return standard CONUS if not found
    if not results:
        return [{
            'city': 'Standard CONUS',
            'lodging': sheet.cell(row=3, column=7).value,
            'mie': sheet.cell(row=3, column=8).value
        }]
    
    return results
```

## M&IE Breakdown by Tier

First and last travel days receive **75%** of the full M&IE rate.

| M&IE Total | Breakfast | Lunch | Dinner | Incidentals | First/Last Day (75%) |
|------------|-----------|-------|--------|-------------|----------------------|
| $68 | $16 | $19 | $28 | $5 | $51.00 |
| $74 | $18 | $20 | $31 | $5 | $55.50 |
| $80 | $20 | $22 | $33 | $5 | $60.00 |
| $86 | $22 | $23 | $36 | $5 | $64.50 |
| $92 | $23 | $26 | $38 | $5 | $69.00 |

## Calculating M&IE for a Trip

```python
def calculate_mie(daily_rate, total_days):
    """
    Calculate M&IE for a trip.
    First and last days are at 75% rate.
    """
    MIE_BREAKDOWN = {
        68: 51.00,
        74: 55.50,
        80: 60.00,
        86: 64.50,
        92: 69.00
    }
    
    first_last_rate = MIE_BREAKDOWN.get(daily_rate, daily_rate * 0.75)
    
    if total_days == 1:
        return first_last_rate
    elif total_days == 2:
        return first_last_rate * 2
    else:
        full_days = total_days - 2
        return (first_last_rate * 2) + (daily_rate * full_days)
```

## Example: 4-Day Trip to Denver, CO

```python
# Denver FY2026: Lodging $215 (peak) / $165 (off-peak), M&IE $92

trip_days = 4
mie_rate = 92
first_last_day = 69  # 75% of $92

mie_total = (2 * first_last_day) + (2 * mie_rate)
# = $69 + $92 + $92 + $69 = $322
```

## Lodging Validation

```python
def validate_lodging(nightly_cost, city, state, trip_dates=None):
    """Check if hotel cost is within GSA lodging allowance."""
    rates = lookup_per_diem(city, state)
    
    # Find applicable rate (consider seasonal variations)
    max_lodging = max(r['lodging'] for r in rates)
    
    if nightly_cost <= max_lodging:
        return True, f"Within GSA rate (${max_lodging}/night)"
    else:
        return False, f"Exceeds GSA rate (${max_lodging}/night) by ${nightly_cost - max_lodging:.2f}"
```

## Common Cities Quick Reference (FY2026)

| City | Lodging | M&IE | Notes |
|------|---------|------|-------|
| Standard CONUS | $110 | $68 | Non-listed locations |
| Denver, CO | $165-215 | $92 | Seasonal variation |
| New York, NY | $282-358 | $92 | Seasonal variation |
| San Francisco, CA | $289-343 | $86 | Seasonal variation |
| Washington, DC | $233-281 | $86 | Seasonal variation |
| Boston, MA | $232-337 | $86 | Seasonal variation |

## Notes

1. **Conference Hotels**: May exceed GSA rate if documented as official conference hotel
2. **Actual Expense**: Some agencies allow actual expense reimbursement with approval
3. **Foreign Travel**: Different rules apply - use State Department rates
4. **Meals Provided**: Deduct from M&IE if meals included in registration or provided by host
