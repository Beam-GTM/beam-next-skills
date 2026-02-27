---
name: follow-up-automation
version: '1.0'
description: Streamlined follow-up system for sales calls based on call transcripts.
  Load when user mentions "follow-up", "follow up email", "call follow-up", "send
  follow-up", "post-call follow-up", "follow-up automation", "create follow-up", "generate
  follow-up", or when user provides a call transcript and needs to send follow-up
  communication and update CRM. Analyzes call transcripts to extract technical requirements,
  decision makers, timeline, and pain points, then generates concise technical follow-up
  emails (under 200 words) and updates CRM with lead status and next steps.
author: Quentin
category: general
tags:
- automation
- crm
- email
- sales
- transcript
updated: '2025-12-12'
visibility: team
---
# Follow-up Automation

Streamlined follow-up system that analyzes call transcripts and generates concise technical follow-up emails with CRM updates.

## Purpose

This skill automates post-call follow-up workflows by:
- Analyzing call transcripts to extract key insights (technical requirements, decision makers, timeline, pain points)
- Generating concise, action-focused follow-up emails (under 200 words)
- Updating CRM with lead status, next steps, and decision timeline

**Key Features**:
- Technical focus (removes partnership/strategic language)
- Professional tone matching call language
- Clear next steps and timeline
- Simple CRM integration

**Time Estimate**: 5-10 minutes per follow-up

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Receive and analyze call transcript
- [ ] Extract key insights and technical requirements
- [ ] Generate follow-up email draft
- [ ] Review and refine email
- [ ] Update CRM with call notes and next steps
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: Analyze Call Transcript

**Actions**:
1. Request call transcript from user (if not already provided)
2. Extract essential call components:
   - **Technical Requirements**: Key technical needs and integration points
   - **Decision Makers**: Who needs to be involved in next steps
   - **Timeline**: When decisions need to be made
   - **Pain Points**: Main challenges to address

**Mark this todo complete before proceeding.**

---

### Step 3: Generate Follow-up Email

Create concise, technical follow-up email using this structure:

**Email Structure**:
1. **Concise Opening** (1 sentence)
   - Brief thank you and call recap
   - Example: "Thanks for the call today—great discussion about [main topic]."

2. **Technical Details** (2-3 sentences)
   - Specific next steps and access information
   - Address key technical questions raised
   - Example: "Based on our discussion, I'll send over evaluation access to [product] for your team to test [specific use case]."

3. **Clear Timeline** (1 sentence)
   - When things will happen
   - Example: "I'll follow up on Friday to check on progress and address any questions."

4. **Simple CTA** (1 sentence)
   - What they need to do next
   - Example: "Let me know if you need anything else in the meantime."

**Quality Guidelines**:
- Keep under 200 words (3-4 paragraphs maximum)
- Focus on technical details, not partnership language
- Professional tone matching the call
- Clear, specific actions with timelines

**Mark this todo complete before proceeding.**

---

### Step 4: Review and Refine

**Actions**:
1. Present draft email to user
2. Ask: "Does this capture the key points? Any changes?"
3. Refine based on feedback
4. Confirm final version

**Mark this todo complete before proceeding.**

---

### Step 5: Update CRM

Create simple CRM update with:

**Call Notes**:
- Key technical points discussed
- Specific requirements or pain points mentioned
- Decision makers involved

**Follow-up Status**:
- What's been sent (evaluation access, docs, etc.)
- What's pending (next meeting, follow-up call)

**Decision Timeline**:
- When to expect next contact
- Key dates or milestones

**Technical Fit**:
- How well requirements match capabilities
- Any red flags or concerns

**Format**: Present as structured text block user can copy-paste into CRM

**Mark this todo complete before proceeding.**

---

### Step 6: Share to Team (Optional but Recommended)

After using this skill successfully, consider sharing it with the team via Notion:

**Benefits of sharing**:
- Team discovers and reuses your work
- Collaborative improvement (others can update)
- Centralized skill library for the company

**To share**:
Say "export this skill to Notion" or use the `export-skill-to-notion` skill.

**What happens**:
1. AI packages the skill (or uses existing .skill file)
2. AI infers Team (likely "Sales" for this workflow)
3. You confirm metadata before pushing
4. Skill appears in "Beam Nexus Skills" database
5. Teammates can query and import with `query-notion-db` and `import-skill-to-nexus`

**Skip this if**:
- Skill is personal/experimental/not ready to share
- Contains sensitive or client-specific info

**Mark this todo complete after deciding (share or skip).**

---

### Final Step: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

The close-session skill will:
- Update system memory
- Save context for next session
- Create session report
- Clean up temporary files

**This is the final mandatory step.** Do not skip - it ensures all progress is preserved.

---

## Follow-up Sequence Timing

### Immediate Follow-up (Within 24 hours)
- Provide technical access or demo scheduling
- Address specific technical questions raised
- Clear timeline for follow-up actions
- Relevant technical documentation only

### Short-term Follow-up (1-3 days)
- Check on evaluation progress
- Address additional questions
- Include decision makers if needed
- Schedule technical deep-dive or decision meeting

---

## Notes

**About Email Quality**:
- Maximum 200 words keeps emails scannable
- Technical focus maintains professionalism
- Clear CTAs drive next steps
- Matching call tone builds rapport

**About CRM Updates**:
- Focus on actionable information
- Track technical fit for qualification
- Document decision timeline for follow-up scheduling
- Keep notes concise but complete
