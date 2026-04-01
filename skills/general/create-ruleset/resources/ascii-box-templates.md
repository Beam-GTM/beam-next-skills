# Presentation Templates

ASCII box diagram templates for the Step-by-Step Presentation Protocol. Use these exact formats when presenting proposals to the user. Emojis provide semantic color-coding for quick scanning.

---

## Agent Task (Step 1)

```
┌─────────────────────────────────────────────────────────────┐
│                   🤖 [AGENT NAME]                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📥 Receives:  [input description]                          │
│                                                             │
│  ⚙️  Does:      [what the agent does]                       │
│                                                             │
│  📤 Produces:  [output description]                         │
│                                                             │
│  📊 Status:    [production/dev/prototype]                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Input Entity (Step 2)

One box per input entity. For multi-entity agents, show one box per entity.

```
┌─────────────────────────────────────────────────────────────┐
│              📄 INPUT ENTITY: [NAME]                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📁 Format:    [formats with distributions]                 │
│  📐 Layout:    [layouts with distributions]                 │
│                                                             │
│  📋 Content:   [key fields listed]                          │
│                                                             │
│  🏭 Industries: [relevant industries]                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Output Entity (Step 3)

```
┌─────────────────────────────────────────────────────────────┐
│              📤 OUTPUT: [NAME]                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📁 Format:    [output format]                              │
│                                                             │
│  📋 Fields:                                                 │
│     • [field_1]: [type] — [description]                     │
│     • [field_2]: [type] — [description]                     │
│     • [field_3]: [type] — [description]                     │
│                                                             │
│  📏 Constraints: [any bounds, ranges, enums]                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Test Scenarios & Sizing (Step 4)

Present ALL three purpose options first, then state recommendation. After user picks, show scenario cards.

### Purpose Selection

```
┌──────────────┬──────────────────────────────────────┬─────────┐
│  Purpose     │ When to use                          │ Samples │
├──────────────┼──────────────────────────────────────┼─────────┤
│ 🟢 flow_check│ Prototyping, testing prompt changes   │   N     │
│ 🟡 score     │ Measure accuracy across scenarios     │   N     │
│ 🔴 battle_test│ Pre-launch, every edge case          │   N     │
└──────────────┴──────────────────────────────────────┴─────────┘
💡 My recommendation: [purpose] — [why]
```

### Scenario Card (one per scenario)

```
┌─────────────────────────────────────────────────────────────┐
│  [✅/🟡/❌/💥] [SCENARIO NAME]              [N] samples     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  What:   [1-3 sentences — what the agent receives]          │
│                                                             │
│  Why it's hard: [1-3 sentences — the specific challenge]    │
│                                                             │
│  Varies:                                                    │
│    [dimension]: [option X%], [option Y%], [option Z%]       │
│    [dimension]: [option X%], [option Y%]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Summary Composition Table

```
┌──────────────────┬──────────┬───────────────────────────────┐
│  Scenario        │ Samples  │ Coverage                      │
├──────────────────┼──────────┼───────────────────────────────┤
│ ✅ [name]        │  N (XX%) │ [what it tests]               │
│ 🟡 [name]        │  N (XX%) │ [what it tests]               │
│ ❌ [name]        │  N (XX%) │ [what it tests]               │
│ 💥 [name]        │  N (XX%) │ [what it tests]               │
├──────────────────┼──────────┼───────────────────────────────┤
│ 📊 TOTAL         │  N       │                               │
└──────────────────┴──────────┴───────────────────────────────┘
```

---

## Anti-Patterns (DO NOT)

1. **No redundant labels.** If the box title includes a value (e.g., `🧠 COMPLEXITY: MEDIUM`), do NOT repeat it inside the box (e.g., `🏷️ T-shirt size: MEDIUM`). State it once only.
2. **No empty footers.** If there are zero hypotheses, omit the `🔶 Hypotheses` section entirely. Same for `Sources` if nothing is cited.
3. **No inline citations.** Never put `📎 source:` lines under individual fields. Use footnote superscripts (¹ ² ³) with a collected `Sources` footer.
4. **No filler rows.** Every row in a box should carry information. Remove blank spacer lines between single-line fields (e.g., `End user` and `Status` can sit adjacent).
