# Buyer Persona: AI/Tech Team Buyer

**Who:** CTO, VP Engineering, Head of AI/ML, Head of Digital, Platform Engineering Lead
**Their world:** They already have AI tools (Claude, OpenAI, Cursor, N8N, custom stacks). They've built prototypes. Their engineers love it. But they can't scale it, govern it, or get the rest of the organization to use it safely. They have a governance problem disguised as a technology problem.

**Key insight from the Bolt call:** These buyers often come to the first call saying "show me the platform" because they think this is a tool evaluation. The real conversation is about governance, orchestration, and scaling beyond the engineering team.

---

## The 7-Beat Arc (AI/Tech Team Variant)

### Beat 1: YOUR WORLD

**What to research:**
- What AI tools they're using (job postings mention Claude, GPT, LangChain, N8N, etc.)
- Size of their engineering/AI team vs. total company
- Whether they have an "AI strategy" or "digital transformation" initiative
- Public signals: blog posts about AI adoption, conference talks, open-source contributions
- Their tech stack (what systems do agents need to interact with?)

**What to say:**
> "Before we show you anything, let me share what we understand about where you are. You've got [X]-person engineering team that's been experimenting with AI — probably Claude, maybe OpenAI, likely some workflow tools like N8N or custom Python scripts. Your engineers have built some impressive things. But you're hitting a wall: the rest of the organization either can't use what you've built, or your security team won't let them. You've got [X] tools doing [Y] things across [Z] teams, and no unified way to govern, audit, or improve any of it."

> "How close is that?"

**What happens next:** They'll correct you, but more importantly, they'll start describing their actual stack, their actual governance gaps, and their actual scaling challenges. This is gold. Let them talk for 10+ minutes.

---

### Beat 2: YOUR FRICTION

**Default friction for AI/tech buyers is fundamentally different from business function buyers:**

| Friction | The real problem | What to say |
|----------|-----------------|-------------|
| **Tool sprawl without governance** | Multiple AI tools across teams, no unified permissions, audit, or control plane | "You've got Claude here, N8N there, custom scripts elsewhere. Each team solved their own problem. But there's no unified view of what agents are doing, on whose behalf, with what permissions." |
| **"We cannot onboard the whole company"** | Security/legal won't approve broad rollout because identity, permissions, and audit trails don't exist | "Your security team is the bottleneck — not because they're wrong, but because the trust infrastructure doesn't exist yet. Agent identity, permissions, audit logs — someone needs to build that layer." |
| **Engineer-dependent scaling** | Only the engineering team can build and modify agents; business teams are locked out | "Your engineers have everything figured out. But the rest of the org hasn't. Every new use case goes through a bottleneck of 3-4 people who know how to build agents." |
| **Prototype-to-production gap** | Demos work, production agents don't — accuracy, edge cases, monitoring are unsolved | "You've proven AI works in POCs. The problem is going from 'cool demo' to 'runs in production at 95%+ accuracy with monitoring, error handling, and continuous improvement.'" |

**Then ask:** "Which of these is the one keeping you up at night?"

---

### Beat 3: THE FAILED PATHS

> "Here's what we see in companies at your stage:"

| Path | What happened | Why it didn't work |
|------|--------------|-------------------|
| **Internal platform team** | "We'll build our own orchestration layer" | Takes 12-18 months. By the time it ships, the AI landscape has shifted. Meanwhile, teams are building ungoverned agents in the wild. |
| **Tool-by-tool governance** | "We'll add permissions to each tool individually" | Creates siloed governance. No cross-tool audit trail. Every new tool means another governance project. |
| **Lock it down and wait** | "Security says no until we have a plan" | Innovation dies. Shadow AI proliferates. Engineers route around restrictions. You end up with MORE ungoverned agents, not fewer. |
| **Consultancy assessment** | "McKinsey will tell us what to do" | You get a 200-page strategy deck. Your engineers ignore it. 6 months later, same problems, minus budget. |

> "The pattern is the same everywhere: the engineering team is 18 months ahead of the governance team. Something has to close that gap — fast."

---

### Beat 4: A BETTER FUTURE

> "Imagine a different architecture. Every agent in your organization — regardless of which LLM it uses, which team built it, which system it touches — runs through a single orchestration layer. That layer handles identity (who is this agent acting on behalf of?), permissions (what is it allowed to do?), audit (what did it actually do?), and continuous improvement (is it getting better?). Your security team isn't blocking adoption — they're enabling it, because the trust infrastructure exists. Your business teams aren't waiting for engineering — they're building agents within governed guardrails. And every agent that runs makes the system smarter."

**The vision for tech buyers is different:**

| Business buyer sees | Tech buyer sees |
|--------------------|----------------|
| "My manual work goes away" | "My AI stack becomes governable and scalable" |
| "95% accuracy" | "Eval-first development with production feedback loops" |
| "Self-learning agents" | "Continuous improvement without re-prompting" |
| "6-8 weeks to production" | "Infrastructure that makes the 100th agent trivial" |

---

### Beat 5: WHY US

**For tech buyers, lead with architecture, not outcomes:**

> "We've been building AI agents since before anyone called them agents. We've been through every failure mode — hallucinations, edge cases, accuracy drift, agents that work in staging and break in production. Instead of solving each problem ad-hoc, we built an operating system. Not because we wanted a platform product, but because we needed it to actually deliver at enterprise scale."

**Three things that resonate with tech buyers:**

**1. Eval-first development**
> "Every agent we build starts with the evaluation dataset — not the prompt. We define what 'good' looks like before we write a line of agent code. That's why 95%+ accuracy at launch, and that's why agents improve over time — because the eval framework is the foundation, not an afterthought."

**2. Orchestration, not just automation**
> "We're not another tool in your stack. We're the layer that makes your stack coherent. Beam orchestrates agents regardless of which LLM powers them, which system they touch, or which team owns them. One governance model. One audit trail. One improvement loop."

**3. Production-grade from day one**
> "The gap between a demo agent and a production agent is enormous. Monitoring, error handling, edge case management, HITL workflows, rollback, permissions — we've built all of that into the platform because we've deployed agents in production at VW, Zurich, KFH, Limehome, MHP Porsche. This isn't theoretical."

**Case study for tech buyers — Volkswagen:**
> "VW's engineering team came to us with a challenge that would have taken them years to build internally. Not because they're not capable — they are — but because building the agent is 20% of the work. The other 80% is eval infrastructure, edge case handling, monitoring, and continuous improvement. We deployed in weeks. The agent today is measurably better than when it launched — no manual re-tuning."

---

### Beat 6: YOUR FIRST AGENT (reframed)

For tech buyers, the beachhead isn't just "which workflow to automate." It's "which use case proves the governance model."

> "Here's what we'd recommend for your first agent. Not because it's the most impressive — because it's the one that proves the architecture. If we can deploy this agent with proper identity management, audit trails, permissions, and continuous improvement — your security team has the evidence they need to greenlight broader rollout."

**Pick a use case that:**
- Touches 2+ systems (proves integration/orchestration)
- Has a clear human-in-the-loop point (proves governance)
- Is visible across teams (proves value beyond engineering)
- Has measurable accuracy requirements (proves eval framework)

---

### Beat 7: THE PATH FORWARD

> "Three steps — but with a governance layer that's different from a typical automation project."

```
Step 1: ARCHITECTURE + DISCOVERY (2 weeks)
  We map your current tool landscape: what's built, who uses it,
  what permissions exist (or don't).
  We co-design the identity and governance model with your security team.
  We select the beachhead use case.

Step 2: BUILD + GOVERN (4-6 weeks)
  We build the first agent on the Beam platform.
  Identity, permissions, audit trail — production-grade from day one.
  Your security team validates the governance model on a real agent.

Step 3: SCALE
  With the governance model proven, you have a template for
  every future agent. Your engineering team builds faster because
  the infrastructure exists. Your business teams self-serve within
  governed guardrails. Every new agent compounds the value.
```

**Bold close (different from business buyer):**
> "We'd like to run a joint architecture session with your engineering lead and your security lead. 90 minutes. We'll map your current stack, identify the governance gaps, and propose the beachhead. Can we do that next week?"

---

## Key Differences from Business Function Playbook

| Dimension | Business Function | AI/Tech Team |
|-----------|------------------|-------------|
| **Language** | Headcount, SLAs, process, budget | Architecture, governance, permissions, APIs |
| **Pain** | Manual work, errors, compliance | Tool sprawl, scaling bottleneck, security blocks |
| **Proof** | Outcome metrics (FTE savings, accuracy) | Architecture proof (governance model, audit trail, eval framework) |
| **Beachhead** | Highest-volume manual workflow | Use case that proves the governance architecture |
| **Close** | "Book discovery with your ops team" | "Joint architecture session with engineering + security" |
| **Competition** | RPA vendors, consultancies | Internal platform team, point-solution governance |
| **Self-learning pitch** | "Agents improve without your team doing anything" | "Eval-first development with production feedback loops — no prompt engineering treadmill" |

---

## Warning Signs This Buyer Is Actually a Business Function Buyer

Sometimes the CTO books the call, but the real problem is a business function pain. Signs:
- They describe a specific workflow ("we spend 20 hours on collections")
- They don't mention their current AI tools
- They ask about pricing per use case, not per platform
- Their team is < 5 engineers

**If this happens:** Pivot to the business function playbook. Don't force the governance narrative on someone who just needs their AR automated.
