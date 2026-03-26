# Supply Chain & Logistics / Automotive — Sales Cheat Sheet

**Grab this 10 minutes before any supply chain, logistics, or automotive call.**

---

## Signals to Research (5 min)

| Signal | Where to look | What it means |
|--------|--------------|---------------|
| ISO 9001, IATF 16949, or VDA certifications mentioned | Company website (quality page), LinkedIn | Certification culture means they need documented, auditable processes — agents that log everything are a natural fit |
| SAP mentioned in job descriptions | LinkedIn jobs, careers page | SAP integration is non-negotiable for them — lead with "we integrate with SAP" |
| High SKU count or multi-branch operations | Company website, industry context | Order entry complexity is high — more variants = more exceptions = more manual work |
| Supplier quality or delivery complaints | Glassdoor, press, customer reviews | Supply chain exceptions are consuming ops bandwidth — exception management is the beachhead |
| German-speaking market or DACH headquarters | Company website | German compliance culture amplifies certification requirements; also signals potential for German-language document processing |

---

## Default Friction Points

1. **Order entry is manual and error-prone** — Orders arrive via email, fax, EDI, and portal in different formats; each one requires manual keying into SAP/ERP, and errors cascade downstream.
2. **Exception management consumes senior staff** — When an order doesn't match (wrong SKU, price mismatch, quantity discrepancy), experienced staff manually investigate and resolve — pulling them from strategic work.
3. **Certification and compliance documentation** — ISO/IATF 16949/VDA audits require documented processes with full traceability; manual workflows create audit gaps and last-minute scrambles.
4. **Supplier communication is fragmented** — Order confirmations, delivery updates, and quality alerts arrive across email, portals, and phone; no single view of supplier status.

---

## Beachhead Options (propose 3)

| Option | Workflow | Package match | Expected impact |
|--------|---------|--------------|----------------|
| A | Order entry automation — extract from email/fax/portal, validate, enter into SAP | Order Entry | 91% accuracy, 1-5 min per order vs. 4-15 min manual (Fraisa benchmark) |
| B | Order exception management — flag mismatches, suggest resolutions, route to right person | Order Entry + Ticket Classification | Automated exception detection across 20+ edge cases with fuzzy matching (Coolback benchmark) |
| C | Customer service automation with SAP integration + certification-compliant audit trails | Ticket Classification + Email Triage | Full CS automation with ISO/IATF traceability (real customer demand pattern) |

---

## Proof Points (pick 2)

| Customer | What we did | Result |
|----------|------------|--------|
| Fraisa | Order entry agent — extracts order data from variable formats, validates against product catalog, enters into ERP | 91% accuracy, processing time reduced from 4-15 minutes to 1-5 minutes per order |
| Coolback | Order entry agent across 3 client branches with 20+ edge cases — fuzzy matching for product names, unit conversions, special pricing | Automated handling of 20+ exception types with fuzzy matching across 3 branches |
| Volkswagen | DataBot — self-learning agent for development workflows | Self-learning agent that improves over time, integrated into Volkswagen's development processes |

---

## What They've Probably Tried

- **EDI standardization projects** — Work for large trading partners but 40-60% of orders still come via email/fax from smaller suppliers and customers; EDI doesn't solve the long tail.
- **RPA bots for SAP data entry** — Break with every SAP GUI update or transaction code change; maintenance cost often exceeds the labor savings within 12 months.
- **Offshore order processing teams** — Lower cost per order but higher error rates, no process improvement, and certification auditors flag the lack of traceability in outsourced workflows.

---

## Common Objections

| Objection | Response |
|-----------|----------|
| "We need IATF 16949 / ISO 9001 compliance on any new system" | Every agent action is logged with full audit trail — who, what, when, decision rationale. That's better traceability than manual processing. Volkswagen runs our agent in their development workflows; we understand automotive certification requirements. |
| "Our orders are too complex — custom pricing, unit conversions, special terms" | Coolback handles 20+ edge cases including fuzzy product matching, unit conversions, and branch-specific pricing across 3 client branches. Complex order formats are the problem we built for. |
| "We can't risk order errors — they cascade through production" | Fraisa achieves 91% accuracy at launch, and the agent is self-learning — accuracy improves over time. Start with human-in-the-loop: agent processes, human approves. You control the autonomy threshold. |
| "SAP integration takes 6+ months with our IT team" | We integrate at the API/file layer with SAP, not at the ABAP level. 6-8 weeks to production. We've done SAP integrations across multiple customers — it's a known pattern for us. |
| "Our German compliance requirements are stricter than most" | We serve multiple DACH companies — Fraisa (Switzerland), Wünsche (Germany, 8K emails/year in German), Coolback. German compliance culture is familiar territory. |

---

## Expansion Path

Order Entry / Exception Management → Demand Planning Support → Supplier Communication Automation → Quality Documentation → Full Supply Chain Ops Layer

---

## Systems We've Integrated in This Vertical

SAP (ECC, S/4HANA), Oracle SCM, Blue Yonder, Coupa, custom EDI platforms, email/fax intake systems
