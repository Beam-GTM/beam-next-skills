---
name: evaluate-solutions-case-study
version: '1.0'
description: Load when user says 'evaluate case study', 'review candidate submission',
  'analyze case study', 'candidate strengths and weaknesses', 'assess candidate work',
  or 'evaluate solutions engineer candidate'. Systematically evaluate Solutions AI
  Engineer candidate case study submissions by analyzing extraction prompt quality,
  project plan depth, and presentation/communication.
author: Sven Djokic
category: general
tags:
- beam-ai
platform: Beam AI
updated: '2025-12-10'
visibility: team
---
# Evaluate Solutions Case Study

Systematically identify strengths and weaknesses in Solutions AI Engineer candidate case study submissions.

## Purpose

Evaluate candidate submissions for the Solutions AI Engineer role by analyzing three key components: extraction prompt quality, project plan depth, and presentation effectiveness. Produces a structured strengths/weaknesses analysis to support consistent hiring decisions.

**Time Estimate**: 15-25 minutes per candidate

---

## Required Context (Load Before Evaluating)

Before evaluating any candidate submission, load these reference materials to understand what the candidate was asked to do:

1. **Case Study Requirements**: `case-study-materials/case-study-requirements.md`
   - Full task instructions given to candidates
   - Expected deliverables for each task

2. **Test Dataset**: `case-study-materials/case-study-dataset/Mid Level AI Solution Engineer Case Study/`
   - **Expected outputs**: `Test Dataset...csv` - Contains emails and expected extraction results
   - **Source PDFs** (10 order documents candidates must extract from):
     - `BauerTech-GmbH.pdf`
     - `Hofbauer-Eng-GmBH.pdf`
     - `Mller-Industrial-GmBH.pdf`
     - `NORSE-tech-GmBH.PDF`
     - `NT-Precision-GmBH.pdf`
     - `Schneider-Metallbau-GmbH.pdf`
     - `Steinbach-GmBH.pdf`
     - `Technovac-GmBH.pdf`
     - `Weber-Tools-GmbH.pdf`
     - `ZMT-Precision-GmBH.pdf`
   - Varying complexity (1-10 products per order)

3. **Full Brief (optional)**: `case-study-materials/Solutions-Case-Study.pdf`
   - Complete PDF sent to candidates

### Required Extraction Fields (11 total)

The candidate's prompt must extract these fields from German B2B order documents:

**Buyer (3 fields):**
- `buyer_company_name`
- `buyer_person_name`
- `buyer_email_address`

**Order (5 fields):**
- `order_number`
- `order_date` (German format: DD.MM.YYYY)
- `delivery_address_street`
- `delivery_address_postal_code`
- `delivery_address_city`

**Product (3 fields, repeated per line item):**
- `product_position`
- `product_article_code`
- `product_quantity`

**Note**: Orders contain 1-10 products each. A complete prompt must handle multiple products per order.

---

## Scoring Rubric

### Score Scale (1-5)

| Score | Meaning |
|-------|---------|
| **5** | Exceptional - Exceeds expectations, demonstrates mastery |
| **4** | Strong - Fully meets expectations, minor improvements possible |
| **3** | Acceptable - Meets basic expectations, some gaps |
| **2** | Weak - Below expectations, significant gaps |
| **1** | Poor - Does not meet expectations, major issues |

### Categories (4 total, 25 points each)

**1. Prompt Engineering** (from Task 1)
| Criterion | What to Score |
|-----------|---------------|
| Field Coverage | Does the prompt address all 11 required fields? Handles multi-product orders? |
| Structure & Clarity | Clear sections, logical organization, unambiguous instructions |
| Output Format Specification | Defines exact output structure, handles edge cases (empty fields, special characters) |
| Example Quality | Provides input/output examples, demonstrates expected behavior |
| Prompt Engineering Best Practices | System/user role separation, appropriate constraints, robust to variation |

**2. Solution Design** (from Task 1 thinking + Task 2)
| Criterion | What to Score |
|-----------|---------------|
| Architecture Understanding | Grasps how LLM extraction fits into larger automation pipeline |
| Error Handling & HITL | Plans for failures, confidence thresholds, human review points |
| Scalability Thinking | Considers volume growth, new document formats, maintenance |
| UAT & Validation Approach | How to test accuracy, acceptance criteria, feedback loops |
| Technical Realism | Feasible approach, aware of LLM limitations, no magic thinking |

**3. Project Management** (from Task 2)
| Criterion | What to Score |
|-----------|---------------|
| Phase Structure | Clear milestones, logical sequencing, dependencies identified |
| Timeline Realism | Reasonable estimates, accounts for iteration and review cycles |
| Risk Identification | Anticipates what could go wrong, has mitigation strategies |
| Stakeholder Touchpoints | Built-in client communication, approval gates, expectation management |
| Resource & Scope Clarity | Clear on what's needed, explicit assumptions and trade-offs |

**4. Communication & Sales** (from Task 3)
| Criterion | What to Score |
|-----------|---------------|
| Narrative Flow | Problem → Solution → Value story, logical progression |
| Technical Translation | Explains complex concepts in client-friendly language |
| Value Proposition | Clear ROI, business benefits articulated, not just features |
| Visual Clarity | Clean slides, appropriate use of diagrams/graphics, not cluttered |
| Call to Action | Clear next steps, creates urgency or engagement path |

### Emoji Indicators

**Category Score (out of 25):**
- 😢 Below 10
- 😟 10-15
- 🙂 16-20
- 🤩 21-25

**Overall Score (out of 100):**
- 😢 Below 40
- 😟 40-69
- 🙂 70-85
- 🤩 86-100

---

## Workflow

### Step 1: Receive Candidate Submission

**Actions**:
1. Receive candidate's case study files from user
2. Identify which components are included:
   - Task 1: Extraction prompt
   - Task 2: Project plan
   - Task 3: Presentation slides
3. Confirm files received and ready to evaluate

---

### Step 2: Score Prompt Engineering (Task 1)

Evaluate the extraction prompt using the **Prompt Engineering** criteria from the Scoring Rubric.

**Actions**:
1. Score each of the 5 criteria (1-5)
2. Note specific references in the candidate's prompt for each score
3. Calculate category total (out of 25)

---

### Step 3: Score Solution Design & Project Management (Task 2)

Evaluate the project plan using both **Solution Design** and **Project Management** criteria from the Scoring Rubric.

**Actions**:
1. Score each of the 5 Solution Design criteria (1-5)
2. Score each of the 5 Project Management criteria (1-5)
3. Note specific references in the candidate's plan for each score
4. Calculate both category totals (out of 25 each)

---

### Step 4: Score Communication & Sales (Task 3)

Evaluate the presentation using the **Communication & Sales** criteria from the Scoring Rubric.

**Actions**:
1. Score each of the 5 criteria (1-5)
2. Note specific references in the candidate's slides for each score
3. Calculate category total (out of 25)

---

### Step 5: Generate Evaluation Report

Compile all scores into the final evaluation report using this format:

**Report Template**:

```markdown
# Candidate Evaluation: [Name/ID]
**Date**: [Evaluation date]
**Evaluator**: [Your name]

---

## 1. Prompt Engineering [EMOJI] [XX/25]

| Criterion | Score | Reference |
|-----------|-------|-----------|
| Field Coverage | X/5 | [Specific reference in candidate's prompt] |
| Structure & Clarity | X/5 | [Specific reference] |
| Output Format Specification | X/5 | [Specific reference] |
| Example Quality | X/5 | [Specific reference] |
| Prompt Engineering Best Practices | X/5 | [Specific reference] |

---

## 2. Solution Design [EMOJI] [XX/25]

| Criterion | Score | Reference |
|-----------|-------|-----------|
| Architecture Understanding | X/5 | [Specific reference in candidate's plan] |
| Error Handling & HITL | X/5 | [Specific reference] |
| Scalability Thinking | X/5 | [Specific reference] |
| UAT & Validation Approach | X/5 | [Specific reference] |
| Technical Realism | X/5 | [Specific reference] |

---

## 3. Project Management [EMOJI] [XX/25]

| Criterion | Score | Reference |
|-----------|-------|-----------|
| Phase Structure | X/5 | [Specific reference in candidate's plan] |
| Timeline Realism | X/5 | [Specific reference] |
| Risk Identification | X/5 | [Specific reference] |
| Stakeholder Touchpoints | X/5 | [Specific reference] |
| Resource & Scope Clarity | X/5 | [Specific reference] |

---

## 4. Communication & Sales [EMOJI] [XX/25]

| Criterion | Score | Reference |
|-----------|-------|-----------|
| Narrative Flow | X/5 | [Specific reference in candidate's slides] |
| Technical Translation | X/5 | [Specific reference] |
| Value Proposition | X/5 | [Specific reference] |
| Visual Clarity | X/5 | [Specific reference] |
| Call to Action | X/5 | [Specific reference] |

---

## Overall Score: [EMOJI] [XX/100]

| Category | Score |
|----------|-------|
| Prompt Engineering | XX/25 |
| Solution Design | XX/25 |
| Project Management | XX/25 |
| Communication & Sales | XX/25 |
| **Total** | **XX/100** |
```

**Emoji Reference**:
- Category (out of 25): 😢 <10 | 😟 10-15 | 🙂 16-20 | 🤩 21-25
- Overall (out of 100): 😢 <40 | 😟 40-69 | 🙂 70-85 | 🤩 86-100

---

## Evaluation Philosophy

- Focus on patterns, not perfection—look for evidence of thinking
- All categories weighted equally (25 points each)
- Reference specific submission material for each score to ensure accountability
- Evaluate against role requirements, not arbitrary standards
