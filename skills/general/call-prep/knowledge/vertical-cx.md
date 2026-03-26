# Customer Service / CX — Sales Cheat Sheet

**Grab this 10 minutes before any CX or customer support call.**

---

## Signals to Research (5 min)

| Signal | Where to look | What it means |
|--------|--------------|---------------|
| Hiring for Tier 1 support agents in bulk | LinkedIn jobs page | Volume is outpacing headcount — automation is inevitable |
| Multi-language support mentioned | Job posts, company website (language options) | Complexity multiplier — every language doubles the staffing problem |
| "Response time" or "CSAT" mentioned in company values | Website, Glassdoor | CX metrics are a leadership priority — they'll measure ROI on response time improvement |
| Using Zendesk/Freshdesk/Intercom (visible in job posts or footer) | Job descriptions, website chat widget | Known integration surface — we've done this before |
| Rapid scaling (new markets, product launches) | Press releases, LinkedIn | Ticket volume is about to spike and current team won't scale |

---

## Default Friction Points

1. **Tier 1 ticket volume overwhelms agents** — 60-70% of tickets are repetitive (password resets, order status, billing questions) but still require human handling, burying agents in low-value work.
2. **Inconsistent response quality** — Different agents give different answers to the same question; new hires take months to ramp, and QA can only sample a fraction of tickets.
3. **Multi-language complexity** — Supporting Arabic+English, German+English, or 30+ country variants requires specialized agents who are expensive and hard to find.
4. **Email triage and routing waste** — Support inboxes receive thousands of emails daily; manually reading, classifying, and routing each one burns hours before anyone starts solving the actual problem.

---

## Beachhead Options (propose 3)

| Option | Workflow | Package match | Expected impact |
|--------|---------|--------------|----------------|
| A | Ticket auto-classification + agent-drafted responses (human-approved) | Ticket Classification | Route to correct queue instantly, draft responses for agent review (Limehome: 11K units; 1NCE: 8 queues, 30+ countries) |
| B | Email triage — classify, filter spam, route to correct team | Email Triage | 90% spam recall, automated routing (Linde: 6K emails/month; Wünsche: 8K emails/year in German) |
| C | Multi-language ticket resolution (Arabic+English or German+English) | Ticket Classification | Handle multi-language tickets without specialized language hires (T2: 9-scenario, Arabic+English) |

---

## Proof Points (pick 2)

| Customer | What we did | Result |
|----------|------------|--------|
| Limehome | Ticket classification agent for 11K-unit hotel operation — routes invoices, booking issues, complaints to correct teams automatically | Automated classification across invoice, booking, and complaint categories |
| FINN | Ticket classification for car subscription support — auto-classifies and routes via Zendesk integration | Automated Zendesk ticket routing for subscription lifecycle issues |
| 1NCE | Support ticket classification across 8 queues serving 30+ countries | Automated multi-queue, multi-country ticket routing |
| Linde | Email triage agent processing 6K emails/month — classifies, filters spam, routes to correct teams | 90% spam recall, automated routing of legitimate emails |

---

## What They've Probably Tried

- **Chatbots (rule-based or early GenAI)** — Handle 10-15% of queries at best; customers learn to type "speak to agent" immediately, and the bot becomes an annoying extra step.
- **Zendesk/Freshdesk built-in automation** — Trigger-based routing works for simple keyword matching but misses intent; tickets still land in the wrong queue 20-30% of the time.
- **Offshore support teams** — Cheaper per-agent cost but lower CSAT, language quality issues, and high turnover means constant retraining. Scales cost linearly with volume.

---

## Common Objections

| Objection | Response |
|-----------|----------|
| "We tried a chatbot and customers hated it" | Chatbots try to replace agents. Our agent works behind the scenes — it classifies, drafts, and routes. Your human agents still respond; they just do it 3x faster with a pre-drafted answer. Customers never interact with the AI directly unless you choose that. |
| "Our tickets are too complex for AI" | T2 runs 9 different scenario types in Arabic and English through our agent. 1NCE classifies across 8 queues and 30+ countries. Complex is our default — we're not doing keyword matching. |
| "We need to keep our Zendesk/Freshdesk setup" | We integrate with your existing stack, not replace it. FINN runs through Zendesk. We add an intelligence layer on top of what you already have. |
| "How do you handle edge cases and escalations?" | The agent classifies confidence on every ticket. Low-confidence tickets get routed to a senior agent automatically. You set the threshold — start conservative, loosen as the agent learns. Self-learning means accuracy improves over time. |

---

## Expansion Path

Ticket Classification + Email Triage → Escalation Routing → Proactive Outreach (certificate renewals, expiration alerts) → Full CX Automation Layer

---

## Systems We've Integrated in This Vertical

Zendesk, Dixa, Freshdesk, Intercom, Salesforce Service Cloud, custom email systems, multi-language NLP pipelines
