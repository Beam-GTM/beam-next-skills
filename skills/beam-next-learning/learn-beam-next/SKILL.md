---
name: learn-beam-next
type: skill
version: '1.1'
description: 'Master Beam Next philosophy and best practices. Load when user mentions:
  learn beam next, beam next tutorial, system mastery, beam next best practices, how
  beam next works, beam next philosophy, beam next design, understand beam next, beam
  next deep dive. 15-18 min.'
category: learning
updated: '2026-03-23'
visibility: public
onboarding: true
priority: medium
---
## 🎯 AI Proactive Triggering (ONBOARDING SKILL)

**This is an ONBOARDING skill with MEDIUM PRIORITY (suggest after core onboarding complete).**

### When to Proactively Suggest (AI MUST check user-config.yaml)

Check `learning_tracker.completed.learn_beam_next` in user-config.yaml. If `false`:

**PROACTIVELY SUGGEST when user:**
1. Has completed OTHER onboarding skills (setup-goals, learn-projects, learn-skills)
   but hasn't done learn-beam-next yet - suggest as "graduation" step
2. Asks philosophical questions ("why does Beam Next work this way?", "what's the design behind...")
3. Encounters AI patterns (false progress, incomplete reads, over-engineering)
4. Makes common mistakes (creating projects instead of skills, skipping close-session)
5. Expresses interest in mastering the system or best practices
6. After using Beam Next for 3+ sessions without completing this skill

**Suggestion Pattern (after other onboarding):**
```
💡 You've learned the core concepts! Ready for system mastery? 'learn beam next'
(15 min) covers the philosophy, design principles, common pitfalls, and
expert collaboration techniques.

This is the "graduation" skill - after this, you'll understand Beam Next deeply.
```

**Suggestion Pattern (encountering issues):**
```
💡 I notice you're running into [AI pattern / common mistake]. The 'learn beam next'
skill covers exactly how to handle this. Want to take 15 minutes to learn
the system deeply? It'll prevent these issues in the future.
```

**DO NOT suggest if:**
- `learning_tracker.completed.learn_beam_next: true`
- User hasn't completed core onboarding yet (suggest core skills first)
- User is new and just getting started (too advanced for first sessions)

---

# Learn Beam Next

Master Beam Next through understanding its philosophy, design principles, and practical patterns.

## Purpose

Help users understand WHY Beam Next works the way it does, avoid common mistakes, and collaborate effectively with AI.

**Time Estimate**: 15-18 minutes

---

## Part A: The Living Knowledge Organism (3 min)

### Display:
```
━━━ CORE PHILOSOPHY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALL FILES IN THIS SYSTEM ARE EXECUTABLE — NOT DOCUMENTATION!

Every .md file, .yaml config, and planning document is designed
to be READ, LOADED, and EXECUTED by AI in conversation.

This is not a static knowledge base. It's a living, breathing
organism that guides you through work, adapts to your context,
and evolves with every interaction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ask**: "Does that click? Every markdown file is essentially code for the AI."

---

## Part B: The 7 Problems Beam Next Solves (4 min)

### Display one at a time, confirm understanding:

```
━━━ THE 7 PROBLEMS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. AI AMNESIA
   Problem: AI forgets everything every session
   Solution: Memory files auto-load every session (goals.md, etc.)

2. FILE CHAOS
   Problem: AI generates files randomly everywhere
   Solution: 5-folder system with clear boundaries

3. INCONSISTENT RESULTS
   Problem: AI improvises differently every time
   Solution: Skills = saved workflows with exact steps

4. REPEATED WORK
   Problem: Build same workflow multiple times
   Solution: Create skill once, reuse forever

5. CONTEXT OVERLOAD
   Problem: Loading everything slows responses
   Solution: Progressive loading (metadata first, content on-demand)

6. HARD TO LEARN
   Problem: Steep learning curve, overwhelming complexity
   Solution: Optional onboarding skills, smart defaults

7. IMMEDIATE EXECUTION
   Problem: AI builds before understanding requirements
   Solution: Planning mode → separate execution session

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ask**: "Which of these problems have you experienced? That's why Beam Next exists."

---

## Part C: The 7 Design Principles (4 min)

### Display:
```
━━━ 7 DESIGN PRINCIPLES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. INSTRUCTION-DRIVEN
   Python script returns COMPLETE instructions.
   AI follows exactly. Zero interpretation.

2. YAML-DRIVEN AUTO-DETECTION
   Everything has metadata describing when to load it.
   AI matches your message → context loads automatically.

3. SKILL-FIRST EXECUTION
   Skills have priority over projects.
   User skills have priority over system skills.

4. PROGRESSIVE DISCLOSURE
   Load minimum at start (metadata only).
   More context just-in-time when needed.

5. STATE IN DATA FILES
   System state tracked in YAML and checkboxes.
   No hidden logic. Transparent. Inspectable.

6. CONTEXT PRESERVATION
   Nothing is lost between sessions.
   close-session saves everything automatically.

7. CONCRETE BEFORE ABSTRACT
   Experience first, explanation after.
   Value delivery before feature teaching.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ask**: "Any principle you want me to explain further?"

---

## Part D: System Pitfalls (2 min)

### Pitfall #1: Projects Instead of Skills

```
WRONG:
📁 weekly-report-week-1/
📁 weekly-report-week-2/
📁 weekly-report-week-3/

RIGHT:
📁 weekly-report/  # ONE skill, used weekly

If creating "name-1", "name-2"... STOP! That's a skill.
```

### Pitfall #2: Skipping Close-Session

```
Without "done" / "close session":
❌ Progress not saved
❌ Learnings not captured
❌ Next session loses context

Always say "done" when finished.
```

### Pitfall #3: Over-Organizing

```
WRONG (day 1): 20 nested empty folders
RIGHT (day 1): 3-5 essential folders

Add folders WHEN needed, not before.
```

---

## Part E: AI Collaboration Patterns (2 min)

### Pattern #1: False Progress

```
AI: "Done! Files created."
(But they don't exist)

Detection:
🔍 "Show me the files"
🔍 "Read that back"
```

### Pattern #2: Incomplete Reads

```
AI reads 100 of 500 lines, misses critical info.

Detection:
🔍 "Did you read the ENTIRE file?"
🔍 "What's at the end?"
```

### Pattern #3: Over-Engineering

```
You want simple, AI builds framework.

Detection:
🔍 "Can this be simpler?"
🔍 "What's the minimum needed?"
```

---

## Part F: Expert Techniques (2 min)

### "Yes, And..." Collaboration

```
You: "Create sales proposal template"
AI: "I'll create it. I notice you target enterprise
     clients - should I add ROI calculator?"
```

Evaluate additions, don't auto-accept/reject.

### Intelligent Friction

```
You: "Create 10 projects for Q1"
AI: "Before 10 projects: Which unblocks others?
     Should some be skills? Start with 2-3?"
```

Good friction prevents wasted effort.

### The Planning Pattern

```
Session 1 (Planning - 20-30 min):
- Create project structure
- Fill overview.md, plan.md, steps.md
- NO IMPLEMENTATION

Session 2 (Execution):
- Load planning files (crystal-clear requirements)
- Execute end-to-end
- Minimal intervention needed
```

Planning optimized for thinking. Execution optimized for doing.

---

## Part G: Mastery Check (2 min)

Quick quiz:
1. Creating "expense-report-jan", "expense-report-feb"... Fix?
2. AI says "Done! All files created." Response?
3. What's the #1 design principle of Beam Next?

Answers:
1. ONE "expense-report" skill
2. "Show me the files"
3. Instruction-driven (Python script controls, AI follows)

---

## Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       learn_beam_next: true  # ADD THIS LINE
   ```

2. **Display completion**:
   ```
   ✅ Learn Beam Next Complete!

   You now understand:
   • The Living Knowledge Organism philosophy
   • 7 problems Beam Next solves
   • 7 design principles (instruction-driven, skill-first, etc.)
   • 3 system pitfalls to avoid
   • 3 AI patterns to detect
   • Expert collaboration techniques

   You're ready to use Beam Next at full power.

   Next steps:
   • 'create project' - Start a new project
   • 'create skill' - Capture a workflow
   • Just work - Beam Next guides you
   ```

3. **Prompt close-session**:
   ```
   💡 When you're done working, say "done" to save progress.
   ```

---

## Success Criteria

- [ ] User understands the Living Knowledge Organism philosophy
- [ ] User knows the 7 problems Beam Next solves
- [ ] User can name key design principles
- [ ] User knows 3 system pitfalls and how to avoid them
- [ ] User can detect 3 AI behavior patterns
- [ ] User understands expert collaboration patterns
- [ ] User passed mastery check quiz
- [ ] `learning_tracker.completed.learn_beam_next: true` in user-config.yaml
