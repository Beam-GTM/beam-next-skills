# Demo Runbook — 1-Page Run-of-Show

**For call 2 (demo calls). Never call 1.**

---

## Pre-Demo Checklist (morning of)

- [ ] **Workspace** shows the prospect's company name (not a generic sandbox)
- [ ] **Hero agent** matches a use case from discovery / call 1
- [ ] **One scripted complex task** is ready (SE-flagged, with branching/eval nuance)
- [ ] **Optimize node** is prepared (good vs. bad examples loaded)
- [ ] **Final artifact** is accessible (the business output: email draft, CRM record, ticket update)
- [ ] **Backup plan** if live demo fails: screenshots or recording ready
- [ ] **Beachhead proposal** ready to present after demo (3 options, recommend 1)

**No SE available?** Use fallback: Demo Builder with a short, relevant prompt for their vertical. Narrate over a pre-built skeleton. Focus on orientating + talking value at each section — don't try to run live tasks.

---

## The Flow (15-20 minutes total)

### A. LAND (30 seconds)

Point at workspace switcher → their company name is there.

> "This is your workspace — isolated, governed, scoped to your agents and data."

---

### B. PROOF (5-7 min) — this is where you win or lose

| Step | Show | Say | Time |
|------|------|-----|------|
| **Analytics** | Open hero agent → Analytics view | "Before we go inside — here's proof this agent is operational. [X] completions, [Y]% eval score." | 45s |
| **Tasks** | Task list → select complex task | "Every row is an execution you can audit. Not a chat log — a production record." | 30s |
| **Node detail** | Open 2 nodes inside the task | "This is where decisions happen. Inputs, outputs, tool calls — fully inspectable." | 1 min |
| **Optimize** | Open Optimize on SE-prepared node | "Watch this: good example, bad example, apply. The agent just got better at THIS specific step. Surgical improvement, not re-prompt everything." | 2 min |
| **Final artifact** | Show the business output (email/record/ticket) | "The value isn't the model's monologue — it's this: [updated CRM record / drafted email / resolved ticket]." | 30s |

**Key:** Don't read every chart. Pick 1-2 numbers in Analytics. Move fast. The point is "this is real," not "let me explain every metric."

---

### C. CONTROL (3-5 min)

| Step | Show | Say | Time |
|------|------|-----|------|
| **Flow** | Open Flow (How) → zoom to match the task you showed | "This is the workflow map — branches, tools, human checkpoints. Connected to the task you just saw." | 1 min |
| **HITL** | Show human-in-the-loop on a sensitive step | "Operators approve or reject here. They don't need to edit the graph — just review the work." | 1 min |
| **Model/tool config** | Open node edit on one step | "Step-level control: faster model for simple extraction, stronger model for judgment calls. Not one-size-fits-all." | 30s |

---

### D. COMPOUND (2 min)

| Step | Show | Say | Time |
|------|------|-----|------|
| **Learning** | Open Learning hub | "What you saw in Optimize on one task is where improvement starts. Learning is where patterns accumulate — the system gets smarter across all tasks, not just one." | 1.5 min |

**If "coming soon" shows:** Don't panic. Samsung didn't care. Say: "The continuous improvement infrastructure is here — the visualization is evolving. What matters is: the agent in month 6 is measurably better than the one we launched."

---

### E. ORIGINATE (2 min)

| Step | Show | Say | Time |
|------|------|-----|------|
| **Demo Builder** | Return to home → "How can I help you today?" | "You've seen a deep agent. This is how you bootstrap the next one: natural language → skeleton workflow → tighten with evals." | 1.5 min |

Use a short prompt tied to their world. If risky to run live, narrate over a pre-built skeleton.

---

### F. CLOSE (1-2 min)

> "Integrations: anything API-native connects. Some out of the box, others custom — depends on your stack."

**Pause. Then:**

> "What would you need to see next — deeper on security, a second workflow, or a scoped discovery?"

**Then:** Present the beachhead proposal (3 options, recommend 1). Move to the 3-step path forward.

---

## Demo Rules

1. **15-20 minutes total.** Not 45. Leave time for discussion.
2. **Don't run live tasks** unless you've verified they complete in <30 seconds. Orientate + talk value instead.
3. **Connect every feature to their specific pain** from call 1. "This matters to you because..."
4. **If something breaks:** "Let me show you this differently" → switch to backup (screenshot, recording, or a different task).
5. **The demo is not the close.** The close is the beachhead proposal after the demo.

---

## Persona-Specific Demo Emphasis

| Persona | Spend more time on | Skip or minimize |
|---------|-------------------|-----------------|
| **Business Function** | Proof (analytics, tasks, final artifact) — "this is real, this is measurable" | Control (Flow) — they don't care about the graph |
| **AI/Tech Team** | Control (Flow, HITL, model config) + Compound (Learning) — "this is governable, this improves" | Originate (Demo Builder) — they'll explore later |
| **C-Suite** | Proof (analytics, final artifact) + Compound (Learning) — "real results that compound" | Everything technical — 5-7 min total, max |

---

## The Samsung Formula (What Worked)

1. Delayed the demo until 1 hour into the call
2. Showed platform for 5-7 minutes only
3. Led with Learning Hub and self-learning — biggest impression
4. When they asked about rigid flows: "Flows are directional. Agents are outcome-based." They loved it.
5. Platform was the proof check, not the pitch
