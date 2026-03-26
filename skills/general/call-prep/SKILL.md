---
name: call-prep
description: "Sales call prep wizard. Researches a prospect, identifies buyer persona and vertical, generates a complete battle plan. Load when user mentions 'prep', 'call prep', 'prep for [company]', 'meeting prep', 'sales prep', 'prepare for [name]', 'demo prep', or any upcoming sales/demo call preparation."
---

# Prep — Sales Call Wizard

**Input:** Name + Company + LinkedIn URL
**Output:** A filled-in battle plan (markdown + optional HTML deck ready to present)

---

## Call Types Supported

| Call type | Trigger | What it produces |
|-----------|---------|-----------------|
| **First call** (default) | "prep for [name] at [company]" | Full battle plan: assumptions, friction, beachhead, proof, close |
| **Demo** (call 2) | "demo prep for [company]" | Demo run-of-show customized to their beachhead + persona |
| **Follow-up / Proposal** | "proposal prep for [company]" | Beachhead proposal with pricing framework, timeline, next steps |
| **Partner call** | "partner prep for [name] at [partner]" | Joint opportunity framing, complementary capabilities, RACI |
| **Expansion** (existing customer) | "expansion prep for [company]" | Agent #2-3 proposals based on what's deployed, expansion path |

---

## The Wizard

### Step 1: GATHER (30 seconds)

Ask the user for:
- **Company name**
- **Attendee(s)** — name + title, or LinkedIn URL(s). Can be multiple people.
- **Call type** (first call / demo / follow-up / partner / expansion) — default: first call
- **Any context** (prior calls, referral source, post-call debriefs, what you already know)

If the user already provided these in their message, skip asking and proceed.

**Multiple attendees:** If more than one person, profile each separately and map room dynamics:
- Who's the real decision maker?
- Who needs convincing vs. who's already bought in?
- Who will ask the hard questions?
- How do the attendees relate to each other?

**Prior context:** Check if there are existing debriefs, project files, or transcripts for this prospect in the workspace. If this is call 2+, load what was learned on call 1 (confirmed friction, what resonated, what fell flat, agreed next steps).

### Step 2: RESEARCH (auto — web search)

**Company research** (use WebSearch):
- What they do, revenue, employee count, competitive position
- Strategic priorities (annual reports, press, earnings)
- Operational model (what's manual, outsourced, tech stack)
- Job postings — look for ops/data entry roles (signals manual processes)
- Any "transformation" or "AI" or "digitization" mentions
- BPO/outsourcing relationships
- Recent M&A, restructuring, or platform migrations

**Attendee research** (use WebSearch + LinkedIn URL if provided):
- Career arc, education, previous roles
- What they're trying to prove in their current role
- How to speak their language (technical vs. strategic vs. financial)
- Decision role (decision maker / influencer / evaluator / champion / blocker)

**Save research notes internally.** Don't dump raw research on the user.

### Step 3: CLASSIFY (auto)

Based on research, determine:

**Buyer persona** — use these signals:

| Signal | Persona |
|--------|---------|
| Describes a specific workflow problem | Business Function |
| Mentions AI tools they're using (Claude, N8N, etc.) | AI/Tech Team |
| Talks about transformation, competitive advantage | C-Suite |
| Title has "Operations" / "Finance" / "HR" | Business Function |
| Title has "AI" / "Digital" / "Engineering" / "CTO" | AI/Tech Team |
| Title has "CEO" / "COO" / "CDO" / "Managing Director" | C-Suite |

→ Load the matched persona playbook from `knowledge/playbook-[type].md`

**Vertical** — match to one of:

| Vertical | File |
|----------|------|
| HR & Recruitment | `knowledge/vertical-hr.md` |
| Banking & Financial Services | `knowledge/vertical-banking.md` |
| Customer Service / CX | `knowledge/vertical-cx.md` |
| Finance Ops & Insurance | `knowledge/vertical-finance.md` |
| Supply Chain / Automotive | `knowledge/vertical-supply-chain.md` |
| Other | Use packages.md qualifying matrix |

→ Load the matched vertical cheat sheet

**Package match** — use the qualifying matrix from `knowledge/packages.md`:
1. What arrives? (email, ticket, document, system event)
2. What happens to it? (classify/route, extract/enter, monitor/chase, evaluate/decide)
3. What function? (operations, finance, HR)

### Step 4: GENERATE

Read the matched persona playbook and vertical cheat sheet. Also read:
- `knowledge/competitive-positioning.md`
- `knowledge/self-learning-story.md`
- `knowledge/packages.md`

Fill in the output template from `templates/output-quick-reference.md` with:

1. **Their world** — from company research (3 bullets)
2. **Their pressures** — from research + vertical cheat sheet signals
3. **Friction hypothesis** — pull from cheat sheet "Default Friction Points," customize with research
4. **Beachhead options** — pull from cheat sheet "Beachhead Options," customize for their specific situation
5. **Proof points** — pull from cheat sheet "Proof Points," pick 2 most relevant
6. **Attendee profile** — from attendee research
7. **Bold close** — propose based on persona (business: "discovery with your ops team" / tech: "architecture session with engineering + security" / c-suite: "30 min alignment + 30 min with function lead")
8. **Objections** — pull from cheat sheet "Common Objections," pick 3-4 most likely for this specific prospect
9. **Call sequence** — from the template (same for all)
10. **Self-learning story** — from `knowledge/self-learning-story.md`

**Recommend one beachhead option.** Don't leave it open.

### Step 5: PRESENT

Output the filled-in battle plan to the user. Then ask:

> "Here's your prep. Three things to check:
> 1. Does the persona feel right? (Business Function / AI-Tech / C-Suite)
> 2. Any of the friction points off-base?
> 3. Want me to go deeper on anything — full attendee profiles, objection handling, or confidential strategy?"

### Step 6: DEEP DIVE (optional, if user asks)

If the user wants more depth, produce the full prep document following the original sales-call-prep workflow:
- Extended attendee profiles with room dynamics
- Full conversation flow with time blocks and role assignments
- Extended objection handling (10+ objections)
- Confidential strategy section
- Key numbers table
- The "one line that wins the call"
- Post-call action checklist

Read the original skill's appendices and Mo Method principles from the old skill file at `../sales-call-prep/SKILL.md` for the deep dive format.

### Step 7: GENERATE DECK (optional but recommended)

If the user wants a presentable deck, generate a filled-in HTML assumptions deck:

1. Read the template from `../../../03-projects/52-customer-focused-framework/04-outputs/assumptions-slide-template.html`
2. Replace all placeholder text with the research from Step 4:
   - Slide 1: Company name + date
   - Slide 2 (Your World): Their world bullets + pressures
   - Slide 3 (Your Friction): 3 friction hypotheses
   - Slide 4 (Failed Paths): Customize based on what they've tried (from vertical cheat sheet)
   - Slide 5 (Better Future): Customize the before/after for their specific function
   - Slide 6 (Why Beam): 2-3 proof points from the prep
   - Slide 7 (Your First Agent): 3 beachhead options with recommended highlighted
   - Slide 8 (Path Forward): Standard 3-step path
   - Slide 9 (Close): Contact info
3. Save as `04-workspace/[company]-deck.html` or the user's preferred location

**This is the single deliverable for the call.** The AE opens this HTML file in a browser and screen-shares. The Quick Reference markdown is for their own notes; the deck is what the prospect sees.

Offer this after presenting the battle plan:
> "Want me to generate the assumptions deck too? You can open it in your browser and screen-share."

### Step 8: PDF (optional, if user asks)

Generate a branded PDF using `scripts/generate_call_prep_pdf.py`.

---

## Follow-Up / Proposal Prep (call 3)

If the call type is follow-up or proposal:

1. Load any existing debrief or notes from prior calls
2. Generate a focused prep that includes:
   - **What was confirmed on call 1/2** — friction, beachhead preference, what resonated
   - **The beachhead proposal** — the one agent they chose, detailed scope
   - **Timeline** — Discovery (1-2 weeks) → Build (4-6 weeks) → Operate
   - **Investment framing** — not a price quote, but how to frame the conversation about cost
   - **Expansion vision** — agent #2 and #3 to plant the seed
   - **Bold close** — "We'd like to kick off discovery next week. Who from your team should be in the room?"

---

## Partner Call Prep

If the call type is partner:

1. Research the partner company (capabilities, markets, existing clients)
2. Generate a prep focused on:
   - **Joint opportunity** — where do your capabilities + theirs create something neither can do alone?
   - **RACI proposal** — who does what in a joint engagement
   - **Reference stories** — any joint customers or analogous partnerships
   - **Commercials framing** — how the economics work
   - **Bold close** — specific joint prospect to pursue together

---

## Expansion Prep (existing customer)

If the call type is expansion:

1. Load what's deployed for this customer (check project files, debriefs, transcripts)
2. Generate a prep focused on:
   - **What's working** — metrics from current agent(s)
   - **Natural next agents** — based on the expansion path from the vertical cheat sheet
   - **3 expansion options** — propose specific agent #2, #3, #4
   - **The compounding story** — "every agent makes the next one faster"
   - **Bold close** — "Let's scope agent #2. Same timeline: 6-8 weeks."

---

## Vertical Not in the List?

If the prospect doesn't match one of the 5 verticals, build a custom cheat sheet on the fly:

1. Use the qualifying matrix from `knowledge/packages.md`:
   - What arrives? → What happens? → What function?
2. Match to the closest package(s)
3. Pull proof points from the most analogous customers
4. Generate friction hypotheses from the company research (job postings, press, operational signals)
5. Note in the output: "No standard vertical match — custom research applied"

---

## Post-Call

After the call, remind the user to fill out the post-call debrief: `templates/post-call-debrief.md`

Trigger phrases: "debrief [company]" or "post-call [company]"

When triggered, present the debrief template and help fill it in based on what the user shares about the call.

---

## Demo Prep (for call 2)

If the user says "demo prep for [company]" or this is a follow-up/demo call:

1. Load `templates/demo-runbook.md`
2. Customize the demo flow for this specific prospect:
   - Which hero agent to show (based on their beachhead from call 1)
   - Which proof points to highlight during Optimize
   - Persona-specific emphasis (business → proof, tech → control, c-suite → compound)
3. Generate the demo run-of-show

---

## Knowledge Base

All knowledge files in `knowledge/` are the skill's internal reference. They are loaded during Step 3-4 as needed. The AE never reads these directly — the wizard reads them and produces the output.

| File | Contains |
|------|---------|
| `playbook-business.md` | 7-beat arc for business function buyers |
| `playbook-tech.md` | 7-beat arc for AI/tech team buyers |
| `playbook-csuite.md` | 7-beat arc for C-suite buyers |
| `vertical-hr.md` | HR & Recruitment cheat sheet |
| `vertical-banking.md` | Banking & Financial Services cheat sheet |
| `vertical-cx.md` | Customer Service / CX cheat sheet |
| `vertical-finance.md` | Finance Ops & Insurance cheat sheet |
| `vertical-supply-chain.md` | Supply Chain / Automotive cheat sheet |
| `packages.md` | Repeatable packages catalog + qualifying matrix |
| `competitive-positioning.md` | How to handle competitor mentions + key numbers |
| `self-learning-story.md` | The 15-sec and 60-sec self-learning pitch |
