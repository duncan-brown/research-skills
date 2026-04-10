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

## License

This project is licensed under the Apache License, Version 2.0. See [LICENSE](su-osp-budget/LICENSE) for details.
