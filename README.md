# Research Skills for Claude

Custom [Claude skills](https://support.anthropic.com/en/articles/11147175-what-are-skills) for research administration at Syracuse University. These skills extend Claude's capabilities with institutional knowledge, policy data, and automated workflows for sponsored research, budget development, and proposal preparation.

## Installation

Download the `.skill` file from the [`dist/`](dist/) directory and add it to your Claude project:

1. Go to your Claude project settings
2. Under "Skills", click "Add skill"
3. Upload the `.skill` file

## su-osp-budget (v3.1)

[su-osp-budget.skill](https://github.com/duncan-brown/research-skills/tree/cc22e918bf41daa344d20275dc4518512afd9738/dist/su-osp-budget/v3.1)

Populates the Syracuse University OSP Budget Template for sponsored research proposals. Translates natural-language budget requests into correctly formatted Excel workbooks with proper fringe rates, F&A calculations, salary escalation, and policy compliance.

**Key capabilities:**

- Personnel budgeting (senior/key, postdocs, graduate assistants, staff) with automatic fringe rate lookup
- Non-personnel costs (equipment, travel, participant support, subawards, tuition, consultants)
- F&A rate calculation using SU's federally negotiated rates (DHHS agreement)
- Multi-year budgets with 3% salary escalation and out-year personnel changes
- NIH salary cap enforcement, NSF two-month rule warnings
- College-specific tuition remission policies
- DOE Genesis Mission (DE-FOA-0003612) Phase I support: generates both the SU OSP Budget workbook and the SF424 R&R Budget form from a single set of Python-computed values

**Requires:** Claude Opus 4.5+, xlsx skill


### Getting Started

Once the skill is installed in your Claude project, you can ask Claude to build a budget in plain English. Claude will ask clarifying questions as needed, look up the correct fringe and F&A rates, and generate a populated OSP Budget Template as a downloadable Excel file.

Open an Opus 4.5 or higher chat and tell Claude:

> Load the su-osp-budget skill to help me develop a budget for my proposal.

Then you can interact with Claude using prompts like the examples below.

**Example prompts:**

> I need a 3-year NSF budget starting 9/1/26. I'm the PI with a base salary of $135,000 and I want to buy out one course per year plus 1 month of summer salary. I also need one grad student for the full project and $5,000/year in travel.

> Build me a budget for an NIH R01. Start date 4/1/27, 5 years. PI salary $150,000 (calendar year appointment, 3 months effort). One postdoc at $62,400 full time. Two grad students in A&S. Equipment: one GPU server at $25,000 in year 1. Subaward to University of Rochester, their budget is $50,000 direct / $15,000 indirect per year.

> Help me build a DOE Genesis Phase I proposal budget. I'm applying to the quantum information science focus area. My base salary is $120,000 and I want 1 course buyout plus 0.5 summer months. I need one postdoc for 6 months and $15,000 in cloud computing for AI model training.

**Tips:**

- Claude will verify your budget against sponsor-specific rules (NIH salary cap, NSF two-month limit, etc.) and flag any issues.
- Always tell Claude which college your grad students are in — tuition remission policies differ by college and significantly affect the budget.
- You can modify budgets iteratively: "Add a second grad student starting in year 2" or "Remove the foreign travel."
- If you are unsure about a rate or policy, just ask — the skill includes all current SU fringe rates, F&A rates, and relevant federal sponsor policies.
- For DOE Genesis proposals, Claude will generate both the SU OSP Budget workbook and the SF424 R&R Budget form.

## oor-dashboards (v1.1)

[oor-dashboards.skill](dist/oor-dashboards/v1.1)

Analyzes Syracuse University Office of Research data from three DataInsights dashboards. Handles Tableau Excel exports with merged cells, forward-fill logic, and cross-referencing across proposals, awards, and expenditures. Does not include General Ledger (GL) transaction parsing.

**Data sources:**

- [Sponsored Proposals](https://datainsights.syr.edu/#/site/data/views/SponsoredProposalsatSyracuseUniversity/Details) — all proposals (Pending, Not Funded, Funded) from FY2014 onwards
- [Anticipated & Supplement Amounts](https://datainsights.syr.edu/#/site/data/views/OfficeofResearchAnticipatedandSupplementAmounts/Details) — funded awards with supplement tracking
- [Detailed Sponsored Expenditures](https://datainsights.syr.edu/#/site/data/views/OfficeofResearchDetailedExpenditures/Details) — expenditures by fiscal year

**Key capabilities:**

- Proposal tracking by status, PI, department, sponsor, and fiscal year
- Award analysis with base + supplement calculations and active/completed filtering
- Expenditure analysis with direct/indirect cost breakdowns and burn rate calculations
- Cross-referencing with faculty-by-unit and Chart of Accounts data
- Subcontract identification (Primary Sponsor vs Sponsor Name)
- Federal spending analysis by department and office
- Monthly expenditure trends and cumulative spending visualization

**Requires:** xlsx skill

### Getting Started

Once the skill is installed in your Claude project, upload Excel exports from the DataInsights dashboards and ask Claude to analyze them.

**Data file naming convention:** `YYYYMMDD_Proposal_Details.xlsx`, `YYYYMMDD_Award_Details.xlsx`, `YYYYMMDD_Expenditure_Details_FYXX.xlsx`

**Example prompts:**

> Load the oor-dashboards skill. I've uploaded Proposal_Details and Award_Details files. Show me a summary of funded proposals by school/college for the current fiscal year.

> What are the top 10 PIs by total active award funding? Include the number of awards and the annual rate for each.

> Show me the monthly expenditure trend for FY25. What is the effective F&A rate and how does spending break down by expense category?

> Which Engineering faculty have pending proposals? What is the total pending amount and who are the sponsors?

> Compare proposed amounts to actual award amounts for funded proposals. How many awards were negotiated down?

> Identify all awards with supplements. Who has the largest total award including supplements?

**Tips:**

- Always upload Proposal Details and Award Details files from the same date for accurate cross-referencing.
- For funded award analysis, the skill uses Award Details as the authoritative source (PeopleSoft live data).
- Expenditure data must be downloaded per fiscal year from the Details tab.
- The skill handles Tableau's merged-cell Excel exports automatically — no manual cleanup needed.

## License

This project is licensed under the Apache License, Version 2.0. See [LICENSE](su-osp-budget/LICENSE) for details.
