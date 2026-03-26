# Banking & Financial Services — Sales Cheat Sheet

**Grab this 10 minutes before any banking or financial services call.**

---

## Signals to Research (5 min)

| Signal | Where to look | What it means |
|--------|--------------|---------------|
| Recent regulatory fines or consent orders | Press releases, regulatory filings | Compliance pressure is acute — budget unlocked for remediation |
| "Digital transformation" or "operational excellence" in annual report | Investor presentations, annual reports | Leadership has mandated automation — internal sponsor likely exists |
| Hiring for compliance/ops analysts in bulk | LinkedIn jobs page | Manual processes are scaling with headcount — they know it's unsustainable |
| New market expansion or product launch | Press releases, LinkedIn | New geographies = new KYC/KYB requirements = immediate pain |
| Mentions of legacy core banking system | Tech blogs, Glassdoor engineering reviews | Integration is their biggest fear — address it early |

---

## Default Friction Points

1. **KYC/KYB processing bottleneck** — Onboarding a single corporate client can take 2-4 weeks of manual document review, verification, and back-and-forth with the customer.
2. **Regulatory compliance overhead** — Every process change requires compliance sign-off; manual processes mean manual audit trails and constant regulatory risk.
3. **Duplicate payments and reconciliation errors** — Manual matching of payments to invoices across systems creates write-offs and audit findings.
4. **Legacy system lock-in** — Core banking platforms (Temenos, Finastra) are rigid; teams build workarounds in spreadsheets rather than fight IT for integrations.

---

## Beachhead Options (propose 3)

| Option | Workflow | Package match | Expected impact |
|--------|---------|--------------|----------------|
| A | KYC/KYB document extraction + verification against watchlists | KYC/KYB | 40% TAT reduction, 50% error reduction (KFH Bahrain benchmark) |
| B | AR reconciliation across multi-country entities | AR Reconciliation | Automated matching across currencies and systems (Zurich Insurance benchmark) |
| C | AP invoice processing + 3-way matching | Document Extraction + AR Collections | 94%+ extraction accuracy, automated exception flagging (BID-Coburg benchmark) |

---

## Proof Points (pick 2)

| Customer | What we did | Result |
|----------|------------|--------|
| KFH Bahrain | AI agent for KYC/KYB document processing — extraction, verification, duplicate detection | 40% reduction in turnaround time, 50% reduction in errors, 90% reduction in duplicate payments |
| BID-Coburg | AR document extraction and classification agent for collections processing | 94.4% extraction accuracy, 88.6% classification accuracy, projected savings of EUR 5.2M/year |

---

## What They've Probably Tried

- **RPA bots for data entry** — Brittle screen-scraping that breaks with every UI update; works for structured workflows but can't handle document variability in KYC/KYB.
- **OCR + rules engine** — Captures text but can't interpret context; still requires human review for anything beyond perfectly formatted documents.
- **Offshore operations teams** — Cheaper labor but same error rates, plus timezone delays and data sovereignty concerns that regulators increasingly flag.

---

## Common Objections

| Objection | Response |
|-----------|----------|
| "Our regulator won't accept AI-driven decisions" | The agent doesn't make decisions — it processes documents, extracts data, and flags exceptions for human review. Your compliance team still approves. KFH Bahrain operates under Central Bank of Bahrain oversight and achieved 40% faster turnaround with this model. |
| "We can't send customer data to an external AI" | Beam AI deploys within your infrastructure. Data never leaves your environment. We're built for regulated industries — SOX-compliant implementations are standard (Smartly runs AR through us with SOX compliance). |
| "Integration with our core banking system is a 12-month project" | We integrate at the workflow layer, not the core banking layer. API or file-based integration. 6-8 weeks to production, not 9-12 months. |
| "We need to go through vendor assessment and security review" | Understood — we support that. We can provide SOC 2 documentation and do a scoped POC on a non-production workflow to build evidence for your security team while the review runs in parallel. |

---

## Expansion Path

KYC/KYB Document Processing → AP Automation → Compliance Reporting → AR Reconciliation → Full Financial Ops Layer

---

## Systems We've Integrated in This Vertical

Core banking platforms, Temenos, Finastra, SAP, NetSuite, Bloomberg, Zendesk (for customer-facing ops), custom portals
