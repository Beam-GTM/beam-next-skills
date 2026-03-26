# Finance Operations & Insurance — Sales Cheat Sheet

**Grab this 10 minutes before any finance, insurance, or shared services call.**

---

## Signals to Research (5 min)

| Signal | Where to look | What it means |
|--------|--------------|---------------|
| "Month-end close" pain mentioned anywhere | Glassdoor, LinkedIn posts from finance team | Close process is manual and painful — direct beachhead fit for AP/AR automation |
| Large factory/entity count or multi-country operations | Company website, annual report | Multi-entity consolidation = spreadsheet hell. Different currencies, systems, regulations per country |
| Hiring for AP/AR clerks, claims adjusters, or financial analysts | LinkedIn jobs page | Throwing headcount at manual processes — budget exists and pain is real |
| Travel-heavy workforce or field operations | Company website, industry context | Expense report volume is high — validation is a bottleneck |
| High combined ratio (>95%) for insurers | Investor presentations, earnings calls | Margin pressure forcing ops efficiency — cost reduction has executive attention |
| ERP or core platform migration mentioned | Job posts, press releases | Mid-migration means workarounds everywhere; they need quick wins outside the migration timeline |
| Recent M&A activity | Press releases | Acquired entities mean duplicate systems and reconciliation nightmares |

---

## Default Friction Points

1. **Invoice processing bottleneck** — AP teams manually key invoices, match to POs, and chase approvals; a single invoice touches 4-5 people before payment.
2. **Multi-entity reconciliation chaos** — Matching invoices, premiums, payments, or commissions across countries and legal entities is a manual spreadsheet exercise that closes late every month.
3. **Expense report validation is tedious and error-prone** — Checking receipts against policy rules is mind-numbing work that nobody wants to do, so violations slip through.
4. **FP&A / reporting consolidation across entities** — Pulling actuals from multiple ERPs/systems into a single view requires manual extraction, transformation, and validation every reporting cycle.
5. **Claims processing backlog** (insurance-specific) — High-volume, document-heavy claims create backlogs that drive customer complaints and regulatory scrutiny.

---

## Beachhead Options (propose 3)

### For general finance / shared services:

| Option | Workflow | Package match | Expected impact |
|--------|---------|--------------|----------------|
| A | AP invoice extraction + 3-way matching + exception routing | Document Extraction + AR Collections | 94.4% extraction accuracy, automated matching (BID-Coburg benchmark) |
| B | Expense report validation against policy rules | Expense Validation | 6-15 seconds per report, replaces 5.5 FTEs (MHP Porsche benchmark) |
| C | FP&A data consolidation across multi-entity operations | FP&A Consolidation | Target 90%+ accuracy (Americana Foods: 10K+ employees, 19 factories) |

### For insurance-specific:

| Option | Workflow | Package match | Expected impact |
|--------|---------|--------------|----------------|
| A | AR / invoice reconciliation across multi-country entities | AR Reconciliation | Automated cross-entity matching and exception flagging (Zurich Insurance benchmark) |
| B | Claims document extraction + classification | Document Extraction | 94%+ extraction accuracy, faster first-touch on claims |
| C | Broker/agent email triage and routing | Email Triage | Route and prioritize thousands of broker emails/month (Linde: 90% on 6K emails/month) |

---

## Proof Points (pick 2-3)

| Customer | Industry | What we did | Result |
|----------|----------|------------|--------|
| MHP Porsche | Automotive/Consulting | Expense validation agent — 46 policy rules across 4 categories | **6-15 seconds per report**, replaces 5.5 FTEs |
| BID-Coburg | Debt Collection | AR document extraction and classification | 94.4% extraction, 88.6% classification, projected **€5.2M/year savings** |
| Zurich Insurance | Insurance | Multi-country AR reconciliation agent | Automated reconciliation across multiple countries and legal entities |
| Americana Foods | FMCG | FP&A consolidation for 10K+ employees, 19 factories | Target ≥90% accuracy on automated consolidation |
| Smartly | Martech | AR automation with NetSuite + Zendesk | **SOX-compliant** AR processing |
| KFH Bahrain | Banking | AP automation | **40% TAT reduction**, 50% error reduction, **90% duplicate payment reduction** |

---

## What They've Probably Tried

- **ERP "automation" modules** (SAP workflows, NetSuite SuiteFlow, Guidewire Smart) — Built for happy-path transactions; exceptions still manual, customization expensive and slow.
- **OCR + manual review** — Captures text but can't interpret line items, match to POs, or handle format variations; still requires a human for every document.
- **RPA for data movement** — Works until a field changes or a new entity is added; maintenance costs often exceed savings within 18 months.
- **Outsourced AP/AR/claims processing** (Genpact, WNS) — Reduces cost per transaction but introduces delays, quality issues, and zero process improvement.
- **Consulting-led process redesign** — 6-month engagement that produces a roadmap but no running software.

---

## Common Objections

| Objection | Response |
|-----------|----------|
| "We're implementing SAP S/4HANA — we'll solve this in migration" | S/4HANA migrations take 18-24 months minimum. Our agents deploy in 6-8 weeks and work with both current and future ERP. MHP Porsche is a Porsche company running our expense agent — SAP is their world, and they still needed workflow-layer automation. |
| "We're mid-migration on our core insurance platform" | That's exactly why a workflow-layer agent makes sense — it sits above the core platform, works during and after migration. Zurich Insurance runs reconciliation across multiple legacy and modern systems simultaneously. |
| "Our invoices/documents come in too many formats" | That's the problem we solve. BID-Coburg: 94.4% extraction across variable formats. Sunday Natural: 12 document types, 46 fields, 95% confidence. Format variability is our sweet spot. |
| "We need SOX / Solvency II / IFRS 17 audit trails" | Smartly runs AR through Beam with full SOX compliance. Every agent action is logged — who, what, when, why. Better audit trail than manual processes where decisions live in someone's head. |
| "Our CFO won't trust AI with financial data" | Start with validation: agent flags exceptions, humans approve. MHP Porsche validates against 46 rules at 6-15 seconds/report. CFO sees accuracy metrics in week one and decides autonomy level. |
| "Our IT team won't approve another vendor" | We deploy as a workflow layer — API integration, no infrastructure footprint. 6-8 weeks to production vs. the 12-month platform projects IT evaluates. |

---

## Expansion Path

**General finance:** AP Automation → Expense Management → Financial Close Acceleration → FP&A Consolidation → Full Finance Ops Layer

**Insurance:** AR Reconciliation → Claims Document Processing → Policy Administration Support → Underwriting Data Extraction → Full Insurance Ops Layer

---

## Systems We've Integrated in This Vertical

SAP (S/4HANA, ECC), NetSuite, Sage, QuickBooks, Stripe, Guidewire, Duck Creek, Salesforce, Zendesk, custom ERP and policy admin systems, multi-currency platforms
