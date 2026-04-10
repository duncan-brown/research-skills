# Research Skills for Claude

Custom [Claude skills](https://support.anthropic.com/en/articles/11147175-what-are-skills) for research administration at Syracuse University. These skills extend Claude's capabilities with institutional knowledge, policy data, and automated workflows for sponsored research, budget development, and proposal preparation.

## Skills

### su-osp-budget (v3.1)

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

## Installation

Download the `.skill` file from the [`dist/`](dist/) directory and add it to your Claude project:

1. Go to your Claude project settings
2. Under "Skills", click "Add skill"
3. Upload the `.skill` file

## License

This project is licensed under the Apache License, Version 2.0. See [LICENSE](su-osp-budget/LICENSE) for details.
