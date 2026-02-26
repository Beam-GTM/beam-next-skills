# Checklist Pattern Reference

This document describes the proven checklist format used for node processing documentation. Follow this pattern to ensure consistency and usability.

## Overview

The checklist format has been validated with clients and provides step-by-step guidance for non-technical staff to execute complex AI extraction logic manually.

## Structure

Every checklist follows this structure:

```markdown
# 📋 PROCESSING CHECKLIST: Node X ([Name])

## 🎯 **Checklist Application**

[1-2 sentences explaining purpose and how to use]

---

## 📝 **STEP 1: [First Major Step]**

### **[Subsection Name]**

- [ ]  [Checklist item]
- [ ]  [Checklist item with details:]
    - Sub-detail 1
    - Sub-detail 2

**IF [CONDITION]:**

- ✓ **variable = "value"**
- ✓ **STOP HERE** - Continue to Step 2

**Examples:**

- ✓ "[Example that matches]" → **value**
- ✗ "[Example that doesn't match]" → **different value**

---

## [Additional Steps...]

---

## 🔍 **STEP X: Validation & Common Errors**

### **Critical Checkpoints:**

### **[Category 1]:**

- [ ]  [Validation point]
- [ ]  [Validation point]

### **Special Cases:**

- [ ]  **"[Edge case description]:"**
    - Current logic: [explanation] → **result**
    - Question: [validation question if uncertain]

---

## 📋 **STEP X+1: Quick Check for Common Errors**

### **TOP X Errors - Check Again:**

- [ ]  **ERROR 1:** [Description of common mistake]
    - ✓ Correct: **[How to do it right]**!
- [ ]  **ERROR 2:** [Description]
    - ✓ Correct: **[How to do it right]**!

---

## ✅ **FINAL CONFIRMATION**

### **Before completion, verify:**

- [ ]  [Final check 1]
- [ ]  [Final check 2]

### **Final Extraction:**

**variable1 = ________** (possible values)

**variable2 = ________** (possible values)

**Justification:**

- Keyword found: _____________________________________
- Logic applied: _____________________________________

---

## 📞 **When Uncertain**

**If unclear which option applies:**

- [ ]  [Troubleshooting step 1]
- [ ]  [Troubleshooting step 2]
- [ ]  Discuss with team colleagues

**Documentation for Review:**

- [Category 1]: __________
- [Category 2]: __________
- Question: ___________________________________________
```

## Key Elements

### 1. Emoji Headers

Use consistent emojis for section types:

- 🎯 Application/Purpose
- 📝 Data Entry/Steps
- 🔀 Routing Decisions
- 📇 Contact/People Info
- 👤 Person-specific Data
- 📄 Documents/Metadata
- 🏦 Banking/Financial
- 💰 Amounts/Money
- 📅 Dates/Scheduling
- ✍️ Signatures
- 🔍 Validation
- 📋 Quick Check/Summary
- ✅ Final Confirmation
- 📞 Help/Support
- 🚨 Critical Warnings

### 2. Checkbox Format

```markdown
- [ ]  Item description
- [ ]  Item with sub-details:
    - Sub-detail 1
    - Sub-detail 2
```

**Note:** Use two spaces after checkbox for proper formatting: `- [ ]  Text`

### 3. Decision Points

For branching logic, use numbered subsections (S1, S2, S3 or B1, B2, B3):

```markdown
### **S1: Option A → result_value**

- [ ]  **Check:** Does condition A apply?
    - Indicator 1
    - Indicator 2

**IF YES:**

- ✓ **variable = "result_value"**
- ✓ **STOP HERE** - Continue to Step X

**Examples:**

- ✓ "Example matching condition A" → **result_value**
- ✓ "Another example" → **result_value**

---

### **S2: Option B → different_value**

[Same structure...]
```

### 4. Critical Warnings

Use blockquotes with warning emoji for critical rules:

```markdown
> **⚠️ IMPORTANT:** This rule is critical because...

> **🚨 CRITICAL:** Bank data ONLY from "Authorization" section (bottom)! NOT from header!
```

### 5. Examples Format

Show both correct and incorrect examples:

```markdown
**Examples:**

- ✓ "Correct example" → **expected_output**
- ✓ "Another correct" → **expected_output**
- ✗ "Wrong approach" → This is incorrect because...
```

For before/after transformations:

```markdown
**Format Transformation:**

- Input: `684,22 EUR` or `1.234,56 EUR`
- Transformation: Remove dot (thousands), comma → period (decimal), remove EUR
- Output: `"684.22"` or `"1234.56"`
```

### 6. Fill-in Blanks

Provide blank fields for users to fill:

```markdown
**variable = ________** (type: possible_value1 / possible_value2 / null)

**Justification:**

- Keyword found: _____________________________________
- Logic applied: _____________________________________
- Source: _____________________________________
```

### 7. Common Errors Section

Always include a "TOP X Errors" section highlighting most frequent mistakes:

```markdown
### **TOP 5 Errors - Check Again:**

- [ ]  **ERROR 1:** [Specific mistake description]
    - ✓ Correct: **[Exact correct approach]**!
- [ ]  **ERROR 2:** [Another common error]
    - ✓ Correct: **[How to do it correctly]**!
```

## Tone and Language

- **Imperative form:** "Extract", "Check", "Verify" (not "You should extract")
- **Direct and clear:** Avoid ambiguity
- **Action-oriented:** Every item should be actionable
- **Structured:** Use consistent formatting throughout
- **English:** All content in English, even when describing German documents

## Validation Example

Here's a complete mini-example:

```markdown
# 📋 PROCESSING CHECKLIST: Node 1a (Bank Letter Processor)

## 🎯 **Checklist Application**

Work through this checklist systematically from top to bottom. Node 1a processes ONLY bank letters about standing order status.

---

## 📝 **STEP 1: Document Validation**

### **Document Check**

- [ ]  Bank letter available (PDF)
- [ ]  Document is readable
- [ ]  Sender is a bank (letterhead visible)

**⚠️ IMPORTANT: Bank letters only!**

- [ ]  Sender = Bank (NOT debtor, NOT BID)
- [ ]  Topic = Standing order status
- [ ]  Official bank letterhead present

**If NOT a bank letter:**

- ❌ This node should NOT run
- ⚠️ Node 0 may have routed incorrectly

---

## 🔍 **STEP 2: Extract Standing Order Status (bIsBankersOrderStatus)**

> **Main Task:** Determine if the bank accepted or rejected the standing order!

### **Status Check**

- [ ]  **Check:** Does the bank letter contain standing order status information?

### **S1: Standing Order ACCEPTED → true**

- [ ]  **Keyword Search:** Does the letter contain one of these keywords?
    - "standing order acknowledged"
    - "standing order created"
    - "standing order established"

**IF YES:**

- ✓ **bIsBankersOrderStatus = true**
- ✓ **STOP HERE** - Continue to Step 3

**Examples:**

- ✓ "The standing order was established" → **true**
- ✓ "We confirm that the standing order was acknowledged" → **true**

---

### **S2: Standing Order REJECTED → false**

- [ ]  **Keyword Search:** Does the letter contain one of these keywords?
    - "standing order rejected"
    - "rejection of standing order"

**IF YES:**

- ✓ **bIsBankersOrderStatus = false**
- ✓ **STOP HERE** - Continue to Step 3

**Examples:**

- ✓ "The standing order was rejected" → **false**

---

### **S3: No Status / Unclear → null**

- [ ]  **Check:** Letter mentions standing order but NO clear status?
    - Interim message ("We received your request")
    - Request for documents ("Please send additional documents")
    - General notice (no recognizable status)

**IF YES:**

- ✓ **bIsBankersOrderStatus = null**
- ✓ **STOP HERE** - Continue to Step 3

---

## 📋 **STEP 3: Quick Check for Common Errors**

### **TOP 3 Errors - Check Again:**

- [ ]  **ERROR 1:** Debtor letter instead of bank letter
    - ✓ Correct: **Only bank letters with bank letterhead**!
- [ ]  **ERROR 2:** General payment instead of standing order
    - ✓ Correct: **Only standing order status**, not regular transfers!
- [ ]  **ERROR 3:** No clear keywords but status guessed
    - ✓ Correct: **No keyword → null**, don't guess!

---

## ✅ **FINAL CONFIRMATION**

### **Before completion, verify:**

- [ ]  Document is bank letter (bank sender)?
- [ ]  Status correctly extracted (true/false/null)?
- [ ]  Keywords clearly identified (not guessed)?

### **Final Extraction:**

**bIsBankersOrderStatus = ________** (true / false / null)

**Justification:**

- Keyword found: _____________________________________
- Status: _____________________________________

---

## 📞 **When Uncertain**

**If unclear which status applies:**

- [ ]  Check keywords again: "acknowledged", "created", "established" → true
- [ ]  Check keywords again: "rejected" → false
- [ ]  No keyword or unclear → null
- [ ]  Discuss with team colleagues
```

## Customization Guidelines

For each node:

1. **Adjust step count:** Simple nodes (2-3 steps), complex nodes (7-9 steps)
2. **Scale error list:** TOP 3 for simple nodes, TOP 5-7 for complex nodes
3. **Add domain-specific emojis:** Banking 🏦, legal ⚖️, etc.
4. **Include relevant warnings:** Highlight the most critical disambiguation rules
5. **Provide realistic examples:** Use actual data patterns from the domain

## Common Patterns

### For Routing Nodes

```markdown
## 🔀 **STEP X: Routing Decision (CRITICAL!)**

> **IMPORTANT:** The routing decision determines which specialized processor gets the document!

### **R1: Category A → "Folder A"**

[Structure as shown above]

### **R2: Category B → "Folder B"**

[Structure as shown above]
```

### For Amount Extraction

```markdown
## 💰 **STEP X: Extract Amounts (3-TIER HIERARCHY!)**

> **IMPORTANT:** 3 different amounts: Total > First Payment >= Subsequent Payments

### **A1: Total Amount (nClaimAmount) - LARGEST amount**

- [ ]  Wording found: "total claim of EUR ________"
- [ ]  Amount extracted: ________ EUR
- [ ]  **Format transformation:**
    - Input: `684,22 EUR` or `1.234,56 EUR`
    - Transformation: Remove dot (thousands), comma → period (decimal), remove EUR
    - Output: `"684.22"` or `"1234.56"`
- [ ]  **nClaimAmount = "________"** (string, 2 decimal places)
```

### For Date Extraction

```markdown
## 📅 **STEP X: Extract Date**

- [ ]  Date found after "starting ________" or "total on ________"
- [ ]  **Format transformation:**
    - Input: `01.07.2024` (German DD.MM.YYYY)
    - Output: `"2024-07-01"` (ISO 8601 YYYY-MM-DD)
- [ ]  **dDateFirstInstalment = "________"** (ISO 8601)
```
