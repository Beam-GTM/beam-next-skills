---
name: scope-of-work-creation
version: '1.0'
description: Create professional proposals and scopes of work (SOW) for client projects
  using phased approach with success gates. Load when user mentions "SOW", "scope
  of work", "proposal", "create proposal", "generate SOW", "write scope", "project
  proposal", "statement of work", or when preparing client proposals with phased deliverables,
  pricing, and success criteria. Structures proposals with clear phases, cost breakdowns,
  deliverables, success gates, out-of-scope items, and legal terms.
author: Quentin
category: general
updated: '2025-12-12'
visibility: team
---
# Scope of Work Creation

Generate professional proposals and statements of work for client projects with clear phasing, success gates, and deliverables.

## Purpose

This skill automates the creation of comprehensive SOWs by:
- Structuring proposals with phased approach and success gates
- Defining clear deliverables, timelines, and cost breakdowns
- Establishing out-of-scope boundaries and client requirements
- Including security, support, and legal terms

**Key Features**:
- Phased approach with success gates (validate before advancing)
- Clear cost breakdowns and credit structures
- Deliverables mapped to each phase
- Out-of-scope items to prevent scope creep
- Professional formatting and structure

**Time Estimate**: 15-20 minutes per SOW

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Gather project context and requirements
- [ ] Define phases and success gates
- [ ] Break down deliverables per phase
- [ ] Calculate costs and pricing structure
- [ ] Define out-of-scope items
- [ ] Add support, security, and legal terms
- [ ] Review and finalize SOW
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: Gather Project Context

**Inputs Required**:
1. **Client Information**:
   - Client name
   - Industry and company size
   - Primary use case or problem
   - Technical environment

2. **Project Scope**:
   - Core objectives (what should be achieved?)
   - Success criteria (how to measure success?)
   - Timeline and urgency
   - Budget constraints or expectations

3. **Technical Requirements**:
   - Integrations needed
   - Security/compliance requirements
   - Infrastructure constraints
   - Data requirements

**Deliverable**: Context summary document

**Mark this todo complete before proceeding.**

---

### Step 3: Define Phased Approach

**Structure**: Create 2-3 phases with clear success gates

**Phase Template**:
```
Phase [N]: [Phase Name] ([Success Gate/POC/Production-Ready])

Cost: $[AMOUNT]

Deliverables:
- [Core feature 1]
- [Core feature 2]
- [Infrastructure/setup item]
- [Integration point]
- [X hours of engineering]

Success Gate: [Criteria for advancing to next phase]
```

**Success Gate Examples**:
- "Client is not obligated to advance to Phase 2 unless Phase 1 meets quality standards"
- "POC must demonstrate [specific metric] before production deployment"
- "Client can exit after Phase 1 with working pilot"

**Call Option Template** (if applicable):
```
Call Option for Phase [N]:
The Customer shall have a unilateral option to commence Phase [N] at any time up to and including the last day of Phase [N-1]. The Call Option may only be exercised by written notice via email to [Company] at [EMAIL] from an authorized representative.

Upon valid exercise:
- Phase [N] becomes billable according to payment terms
- Project scope and timeline extended by [X] weeks

If not exercised, Phase [N] shall not commence and no fees shall be due.
```

**Deliverable**: Phased project structure with success gates

**Mark this todo complete before proceeding.**

---

### Step 4: Define Deliverables and Pricing

**For Each Phase**:

1. **List Specific Deliverables**:
   - Technical deliverables (features, integrations, infrastructure)
   - Workspace/access setup
   - Documentation and training
   - Support and maintenance
   - Engineering hours included

2. **Calculate Pricing**:
   - Base cost per phase
   - Engineering hours breakdown
   - License credits (if applicable)
   - Total investment summary

**Pricing Structure Template**:
```
Phase 1: Core [Feature] Pilot
Cost: $[AMOUNT]
Deliverables:
- [Item 1]
- [Item 2]
- [X] hours of AI agent engineering

Phase 2: Production-Ready [Feature]
Cost: $[AMOUNT]
Deliverables:
- [Item 1]
- [Item 2]

Credit: [X]% of Phase 2 cost applied to first-year platform license
```

**Deliverable**: Complete pricing breakdown with deliverables

**Mark this todo complete before proceeding.**

---

### Step 5: Define Out-of-Scope Items

**Purpose**: Prevent scope creep and set clear boundaries

**Categories to Address**:

1. **Additional Use Cases**:
   - "Scope limited to [specific use case]; other [category] automation is excluded"
   - Example: "Additional recruiting use cases - Scope limited to interview scheduling workflows only"

2. **Integrations**:
   - "Only [System X] integration is included; integrations with other [category] are excluded"
   - Example: "Only Thrive integration included; other ATS/HRIS integrations excluded"

3. **Advanced Features**:
   - "[Feature category] - [Basic version] included; [advanced version] excluded"
   - Example: "Basic admin dashboard included; advanced analytics, custom reporting excluded"

4. **Ongoing Support**:
   - "Support limited to [phase/timeframe]; post-[phase] maintenance requires separate agreement"
   - Example: "Support limited to POC phase; post-POC maintenance requires separate agreement"

**Deliverable**: Clear out-of-scope section

**Mark this todo complete before proceeding.**

---

### Step 6: Add Support, Security, and Requirements

**Support Section**:
```
Support:
[Company] will set up a joint communication channel (Slack/Teams) for direct customer support and fast issue resolution.

Client Requirements:
- Client provides API spec in compatible format
- Client supports API access/testing for integrations
- [Company] supports setup of future use cases during project phase
```

**Security Section**:
```
Security Requirements:
[Company] follows [SOC2/ISO 27001] standard for security and data privacy.

Measures include:
- Data Encryption: All sensitive data encrypted during transmission and storage
- Compliance: Agents comply with relevant data protection regulations
- Access Controls: Granular permissions restricting access to authorized personnel only
```

**Main Benefits Section**:
```
Main Benefits of [Solution]:
- Rapid deployment of operational MVP within [X] weeks
- Minimal technical team involvement for integration
- Scalability for future automation needs
```

**Deliverable**: Complete support, security, and benefits sections

**Mark this todo complete before proceeding.**

---

### Step 7: Review and Finalize

**Final Review Checklist**:
- [ ] All phases clearly defined with success gates
- [ ] Deliverables specific and measurable
- [ ] Pricing transparent with breakdown
- [ ] Out-of-scope items comprehensive
- [ ] Support and security requirements included
- [ ] Legal terms (call option) if applicable
- [ ] Professional formatting and structure
- [ ] Client name and use case correctly referenced throughout

**Present to user**:
1. Show complete SOW structure
2. Ask: "Does this capture all requirements? Any changes?"
3. Refine based on feedback
4. Generate final formatted document

**Deliverable**: Final SOW ready for client

**Mark this todo complete before proceeding.**

---

### Step 8: Share to Team (Optional but Recommended)

After using this skill successfully, consider sharing it with the team via Notion.

**To share**: Say "export this skill to Notion" or use the `export-skill-to-notion` skill.

**Skip this if**: Skill is personal/experimental or contains sensitive info.

**Mark this todo complete after deciding (share or skip).**

---

### Final Step: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

**This is the final mandatory step.** Do not skip - it ensures all progress is preserved.

---

## SOW Structure Template

```
### Proposal & Scope of Work
**Proposal**: [Solution description for CLIENT]

#### Context
This proposal introduces [solution type] for [CLIENT NAME] to [primary objective]

#### At A Glance
- Phased Approach with Success Gates - Validate at each step
- Core [Feature] Pilot (Phase 1) - Foundation with quality gate
- Production-Ready [Feature] (Phase 2) - Full production with license credit

[PHASES DETAILED ABOVE]

#### Out of Scope
[OUT-OF-SCOPE ITEMS]

#### Support
[SUPPORT DETAILS]

#### Security Requirements
[SECURITY DETAILS]

#### Main Benefits
[BENEFITS LIST]
```

---

## Notes

**About Phased Approach**:
- Success gates protect client investment
- Each phase delivers standalone value
- Clear exit points after each phase
- Credit structure incentivizes full engagement

**About Pricing**:
- Transparent cost breakdown builds trust
- Engineering hours show value
- License credits reduce friction
- Phasing spreads investment over time

**About Out-of-Scope**:
- Critical for preventing scope creep
- Sets realistic expectations early
- Creates opportunities for future upsells
- Protects project timeline and budget
