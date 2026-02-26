---
name: abstract
version: '1.0'
description: Zoom out and contextualize overwhelming concepts. Load when user says
  'zoom out', 'abstract', 'I'm lost', 'I'm overwhelmed', 'bigger picture', or expresses
  confusion about where a concept fits. Identifies paradigms, shows hierarchies, teaches
  with analogies, and connects to user's goals.
category: general
updated: '2026-01-09'
visibility: public
---
# Abstract

Help users zoom out when overwhelmed by new concepts - identify paradigms, show the bigger picture, and teach in context.

## Purpose

When learning new concepts, it's easy to get lost in details without understanding where they fit. This skill:
- Identifies which paradigm/framework the concept belongs to
- Shows a visual map of how pieces connect
- Teaches using analogies tailored to the user's background
- Connects everything to the user's actual goals and work

**Time Estimate**: 3-5 minutes per concept

---

## Workflow

### Step 1: Load User Context

**Always start by reading the user's goals:**

```
Read: 01-memory/goals.md
```

Extract:
- Current role and work context
- Short-term goals (what they're trying to master)
- Long-term vision (where this learning leads)
- Work style preferences

This ensures explanations are tailored, not generic.

---

### Step 2: Identify the Concept

Ask or infer what the user is overwhelmed by.

**If unclear, ask:**
> "What concept or topic is feeling overwhelming right now?"

**If they've already stated it**, proceed directly.

**Capture:**
- The specific concept/term
- What triggered the confusion (if mentioned)
- How deep they've gone (beginner vs. stuck in details)

---

### Step 3: Map the Paradigm

Identify which framework or mental model this concept belongs to.

**Common paradigms in FDE/Agent work:**

| Domain | Paradigms |
|--------|-----------|
| AI Agents | Agentic loops, Tool use, Memory patterns, Evaluation |
| APIs/Integrations | REST vs GraphQL, Auth patterns, Webhooks vs Polling |
| Debugging | Observability stack, Trace analysis, Root cause patterns |
| Architecture | Distributed systems, Event-driven, Request-response |
| Data | ETL pipelines, Streaming vs Batch, Schema design |

**For broader topics**, identify the relevant field and its core frameworks.

Load [references/paradigm-maps.md](references/paradigm-maps.md) for detailed hierarchies.

---

### Step 4: Show the Map

Present a visual hierarchy showing where the concept sits.

**Format (simple concept):**
```
PARADIGM: [Name]
│
├── Core Concept A
│   ├── Sub-concept
│   └── Sub-concept ← YOU ARE HERE
│
├── Core Concept B
│   └── Related idea
│
└── Core Concept C
```

**Format (complex concept):**
Provide narrative tour first, then visual map:

> "You're looking at [X]. X is part of the [Y] paradigm, which is how we think about [purpose].
>
> At the highest level, [Y] breaks into [A, B, C]. You're currently in [A], specifically looking at [X].
>
> Here's the map:"
>
> [Visual hierarchy]

**Always show:**
- Where they are (mark with "← YOU ARE HERE")
- What's adjacent (sibling concepts)
- What's above (parent category)
- What's below (if relevant)

---

### Step 5: Connect to User Context

Bridge the concept to their specific situation.

**Reference their goals:**
- "Given you're mastering the AI agent lifecycle, [concept] matters because..."
- "For your startup vision in payments/debt collection, this connects to..."
- "In your FDE role at Beam, you'll encounter this when..."

**Make it concrete:**
- Name specific scenarios they'll face
- Reference tools/platforms they use (Beam, Langfuse, etc.)
- Tie to their success metrics if relevant

---

### Step 6: Teach with Analogies

Explain using relatable comparisons.

**Good analogy patterns:**

| Pattern | Example |
|---------|---------|
| Physical world | "An API is like a waiter - takes your order, talks to kitchen, brings food back" |
| Their domain | "Langfuse traces are like flight recorders - capture everything for post-mortem" |
| Everyday experience | "Rate limiting is like a bouncer - only lets so many people in per hour" |
| Building blocks | "Webhooks are push notifications for servers" |

**Load** [references/analogy-patterns.md](references/analogy-patterns.md) for more patterns.

**Guidelines:**
- Use analogies from their background (FDE, agents, startups)
- Acknowledge where analogies break down
- Layer analogies for complex concepts (simple → nuanced)

---

### Step 7: Provide Actionable Clarity

End with clear next steps.

**Format:**
```
NOW YOU KNOW:
- [Key insight 1]
- [Key insight 2]

FOCUS ON:
- [What matters most right now]
- [What to ignore for now]

NEXT STEP:
- [Concrete action they can take]
```

**Anti-overwhelm principle:** Tell them what to NOT worry about yet. Scope reduction is clarity.

---

## Output Adaptation

**Simple concept** (can explain in 2 min):
- Visual hierarchy
- One strong analogy
- Brief context connection
- Quick "focus on" guidance

**Complex concept** (needs 5+ min):
- Narrative tour first ("Let me walk you through...")
- Multiple layered analogies
- Detailed visual map
- Explicit "ignore for now" list
- Concrete next step

---

## Example

**User:** "I'm overwhelmed by all these agent memory patterns - RAG, vector stores, conversation history, episodic memory..."

**Response:**

> Let me zoom out on this for you.
>
> **The Paradigm:** Agent Memory
>
> Memory in AI agents answers one question: *"How does the agent access information it doesn't have in its weights?"*
>
> ```
> AGENT MEMORY
> │
> ├── Short-term (within conversation)
> │   └── Conversation history ← simplest, always there
> │
> ├── Long-term (across conversations)
> │   ├── Vector stores / RAG ← YOU ARE HERE
> │   ├── Episodic memory (past experiences)
> │   └── Semantic memory (facts/knowledge)
> │
> └── Working memory (active context)
>     └── What's loaded right now
> ```
>
> **Analogy:** Think of it like human memory:
> - *Conversation history* = what you said 5 minutes ago (short-term)
> - *RAG/Vector stores* = your bookshelf - you look things up when needed
> - *Episodic memory* = remembering "last time this client asked X, we did Y"
>
> **For your Beam work:** Most agents you'll build use RAG (vector stores) for knowledge retrieval. Episodic memory is advanced - only needed when agents must learn from past interactions.
>
> **Focus on:**
> - RAG fundamentals (chunking, embeddings, retrieval)
> - Ignore episodic memory until you've shipped 3+ RAG agents
>
> **Next step:** Build one agent with simple RAG, observe where retrieval fails, then iterate.

---

## Resources

### references/
- **paradigm-maps.md** - Hierarchies for common FDE domains
- **analogy-patterns.md** - Templates for creating good analogies

### scripts/
*None required - this is a reasoning/teaching skill*

### assets/
*None required*
