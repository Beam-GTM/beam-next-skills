---
name: calculate-beam-agent-pricing
version: '1.0'
description: Design node architecture and calculate comprehensive pricing for Beam
  AI agents based on requirements. Load when user says 'calculate agent pricing',
  'price this agent', 'design agent architecture', 'estimate agent cost', 'node breakdown
  for agent', or needs detailed cost analysis for a Beam agent project. Generates
  complete node-by-node breakdown with credit consumption, monthly economics, optimization
  strategies, and client pricing models.
author: Safi Haider
category: general
tags:
- beam-ai
platform: Beam AI
updated: '2026-02-03'
visibility: team
---
# Calculate Beam Agent Pricing

## Purpose

Generate comprehensive node architecture and pricing analysis for Beam AI agents, including:
- Detailed node-by-node breakdown
- Credit consumption calculations
- Multiple pricing scenarios (POC, optimized, premium)
- Cost optimization strategies
- Client pricing recommendations
- Professional markdown output for proposals

## When to Use

- **New agent projects**: Need to estimate costs before building
- **Client proposals**: Calculate pricing for enterprise clients
- **Architecture planning**: Design optimal node flow
- **Cost optimization**: Analyze existing agents for savings
- **Budget planning**: Forecast monthly operational costs

## Prerequisites

- Agent requirements/scope documented
- Expected monthly volume known
- Integration requirements identified
- Quality/performance targets defined

---

## Workflow

### PHASE 1: Requirements Gathering

#### Step 1: Collect Agent Requirements

Ask the user to provide (or help them define):

**Basic Information:**
- Agent name/purpose
- Primary use case (email personalization, data extraction, lead qualification, etc.)
- Target users/audience
- Expected monthly volume (executions per month)

**Technical Requirements:**
- Input sources (webhooks, APIs, manual triggers)
- Data retrieval needs (CRM, enrichment APIs, databases)
- Processing complexity (simple classification vs deep analysis)
- Output destinations (CRM, email, Slack, database)
- Integration requirements (Zoho, Salesforce, HubSpot, etc.)

**Quality Requirements:**
- Need for validation/quality checks?
- Fallback strategy required?
- Analytics/logging needs?
- Performance requirements (speed, accuracy)

**Example Questions:**
```
What does this agent do? (1-2 sentence description)
How many times will it run per month?
What data sources does it need to access?
What's the main output/action it performs?
Do you need quality validation before final output?
Are there optional features we could cut to reduce costs?
```

---

### PHASE 2: Node Architecture Design

#### Step 2: Design Node Flow

Based on requirements, design the node architecture using this framework:

**SECTION 1: TRIGGER & CONTEXT RETRIEVAL**
- Trigger node (webhook, scheduled, manual) - **0 credits** if webhook/chat
- Integration nodes for data retrieval - **1 credit each**
- Consider: How many data sources? What context is needed?

**SECTION 2: ANALYSIS & PROCESSING**
- LLM nodes for classification/analysis - **1-5 credits** depending on model
- Logic nodes for routing/branching - **0 credits**
- Consider: Complexity of analysis? Model requirements (Basic vs Standard)?

**SECTION 3: GENERATION/ACTION**
- LLM nodes for content generation - **1-5 credits**
- Logic nodes for formatting - **0 credits**
- Consider: Output complexity? Multiple variations needed?

**SECTION 4: QUALITY VALIDATION** (optional but recommended)
- LLM node for quality check - **3-5 credits**
- Conditional logic for gating - **0 credits**
- Fallback handler - **0 credits**
- Consider: Risk of poor output? Need for guardrails?

**SECTION 5: DELIVERY & LOGGING**
- Integration nodes for writing data - **1 credit each**
- Analytics/logging - **1 credit**
- Consider: How many systems to update? Tracking needs?

**Node Design Principles:**
- Each integration API call = 1 credit
- Each LLM call = 1 (Basic), 3 (Standard), or 5 (Advanced) credits
- Logic/transformation nodes = 0 credits
- Triggers: webhook/chat = 0, scheduled/integration = 1 credit
- Attachments: 3 minimum (configurable, cost-based on tokens)

---

#### Step 3: Document Each Node

For each node, specify:
- **Node number & name**: Sequential numbering
- **Type**: Trigger, Integration, LLM, Logic, Conditional
- **Purpose**: What does this node do?
- **Model** (if LLM): GPT-4o-mini (1), Claude Sonnet (3), Claude Opus (5)
- **Input**: What data does it receive?
- **Output**: What data does it produce?
- **API Call** (if integration): Endpoint and method
- **Prompt** (if LLM): Full prompt template
- **Logic** (if logic node): Business rules
- **Credits**: Credit consumption

**Template:**
```markdown
#### Node X: [Name]
- **Type**: [Trigger/Integration/LLM/Logic]
- **Purpose**: [Clear description]
- **Model**: [If LLM - specify model and why]
- **Input**: [Data received]
- **Prompt**: [If LLM - full prompt]
- **Output**: [Data produced]
- **Credits**: **X**
```

---

#### Step 4: Calculate Credit Consumption

Create a consumption breakdown table:

| Section | Nodes | Credits | Details |
|---------|-------|---------|---------|
| Trigger & Context | X-Y | N | [Breakdown] |
| Analysis | X-Y | N | [Breakdown] |
| Generation | X-Y | N | [Breakdown] |
| Validation | X-Y | N | [Breakdown] |
| Delivery | X-Y | N | [Breakdown] |
| **TOTAL** | X nodes | **N credits** | Per execution |

**Model Usage Breakdown:**

| Model Type | Usage per Execution | Credits per Usage | Total Credits | % of Total |
|------------|---------------------|-------------------|---------------|------------|
| LLM - Basic | X calls | 1 | X | X% |
| LLM - Standard | X calls | 3 | X | X% |
| LLM - Advanced | X calls | 5 | X | X% |
| Integration Nodes | X calls | 1 | X | X% |
| Logic/Triggers | X nodes | 0 | 0 | 0% |
| **TOTAL** | **X nodes** | - | **X** | **100%** |

---

### PHASE 3: Pricing Calculations

#### Step 5: Calculate Monthly Economics

**Formula:**
```
Total Monthly Credits = Credits per Execution × Monthly Volume
```

**Cost Calculation:**
- **Base Cost**: Total Credits × $0.02 (base credit value)
- **Your Cost @ 4.0x**: Total Credits × $0.08 (default Enterprise markup)
- **Your Cost @ 2.5x**: Total Credits × $0.05 (negotiated markup)
- **Your Cost @ 2.0x**: Total Credits × $0.04 (volume discount)

**Create Pricing Tables:**

##### Full Architecture

| Volume | Total Credits | Cost @ 4.0x | Cost @ 2.5x | Client Price | Margin @ 4.0x |
|--------|---------------|-------------|-------------|--------------|---------------|
| [Monthly Volume] | [Total] | $X,XXX | $X,XXX | $XX,XXX | XX% ($X,XXX) |

##### Optimized Architecture (if applicable)

[Same table with reduced credit count]

##### POC Phase (typically 1/4 of monthly volume)

| Scenario | Executions | Credits | Cost @ 4.0x | Cost @ 2.5x | Client Price | Margin |
|----------|------------|---------|-------------|-------------|--------------|--------|
| Full | [N] | [N] | $X,XXX | $X,XXX | $X,XXX | XX% |
| Optimized | [N] | [N] | $X,XXX | $X,XXX | $X,XXX | XX% |

---

#### Step 6: Identify Cost Optimizations

Analyze the architecture for optimization opportunities:

**Common Optimizations:**

| Strategy | Credits Saved | Impact on Quality | Recommendation |
|----------|---------------|-------------------|----------------|
| Remove optional enrichment | -X | Low | ✅ Start without, add if needed |
| Use cheaper LLM for simple tasks | -X | Low-Medium | ✅ Recommended |
| Skip optional validation | -X | High risk | ❌ Not recommended |
| Cache repeated analyses | -X avg | None | ✅ Implement when possible |
| Merge similar nodes | -X | Low | ✅ Good optimization |

**Optimization Scenarios:**
- **Minimum Viable**: Core functionality only, cheapest models
- **Balanced**: Quality/cost tradeoff, recommended for most projects
- **Premium**: Maximum quality, all features enabled

---

#### Step 7: Client Pricing Recommendations

**Pricing Model Options:**

##### Option 1: Per-Execution Pricing
```
Cost per execution = (Credits × Your Rate) + Profit Margin
Recommended margin: 40-60% for enterprise
```

**Example:**
- Your cost: $0.08/credit × 15 credits = $1.20/execution
- Client price: $2.00-$3.00/execution (40-60% margin)

##### Option 2: Fixed Monthly Retainer
```
Monthly fee = (Monthly Credits × Your Rate × 1.5) + Buffer
Buffer accounts for: overages, support, optimization
```

**Tiered Pricing:**
| Tier | Monthly Fee | Executions Included | Overage Rate | Your Margin |
|------|-------------|---------------------|--------------|-------------|
| Basic | $X,XXX | [Volume] | $X.XX/exec | XX% |
| Professional | $X,XXX | [Volume] + features | $X.XX/exec | XX% |
| Enterprise | $X,XXX | Unlimited | $X.XX/exec | XX% |

##### Option 3: Performance-Based (Hybrid)
- Base fee: Covers your costs + 20% buffer
- Performance bonus: Additional fee based on KPI achievement
- Lower risk for client, higher upside for you

---

### PHASE 4: Documentation Generation

#### Step 8: Create Comprehensive Markdown Document

Generate a markdown file with these sections:

**1. Overview**
- Agent name and purpose
- Volume and credits per execution
- Monthly cost summary

**2. Agent Architecture: X-Node Workflow**
- Complete node breakdown by section
- Each node documented with full details
- Prompt templates for LLM nodes

**3. Credit Consumption Summary**
- Per-execution breakdown table
- Cost breakdown by model type
- Visual flow diagram

**4. Cost Optimization Options**
- Optimization strategies table
- Recommended optimized architecture
- Credits saved and quality impact

**5. Monthly Economics**
- Full architecture pricing
- Optimized architecture pricing
- POC phase pricing

**6. Client Pricing Recommendations**
- Pricing model options (per-execution, monthly, hybrid)
- Tiered pricing tables
- Margin calculations

**7. Architecture Flow Diagram**
- ASCII diagram showing node flow
- Credit consumption per section
- Routing logic visualization

**8. Implementation Phases**
- Phase 1: MVP (core features only)
- Phase 2: Enhanced (add validation)
- Phase 3: Full Production (all features)
- Phase 4: Optimization (cost reduction)

**9. Success Metrics**
- Performance KPIs (accuracy, speed, quality)
- Operational KPIs (success rate, credits/exec)
- Financial KPIs (revenue, costs, margin)

**10. Technical Requirements**
- Integration requirements
- Data requirements
- LLM access needs
- Monitoring & logging

**11. Risk Mitigation**
- Potential risks and impacts
- Mitigation strategies
- Contingency plans

**12. Next Steps**
- Architecture decisions to finalize
- POC implementation plan
- Economics validation approach
- Production deployment roadmap

---

#### Step 9: Save Output

**Offer to save the document:**
```
Would you like me to save this pricing document?

Options:
1. Save to current project: 02-projects/{project-id}/01-planning/node-architecture.md
2. Save to workspace: 04-workspace/pricing-proposals/{agent-name}-pricing.md
3. Display only (I'll copy manually)
```

If saving to a project, check if project exists first. If not, suggest creating one.

---

### PHASE 5: Review & Refinement

#### Step 10: Review with User

Present the pricing analysis and ask:
```
I've calculated the following for your agent:

ARCHITECTURE: [X] nodes, [Y] credits per execution
MONTHLY COST: $[X,XXX] - $[Y,YYY] depending on markup
CLIENT PRICING: $[XX,XXX] - $[YY,YYY]/month (recommended)
MARGIN: [XX]% - [YY]%

Would you like to:
1. Adjust the architecture (add/remove features)
2. Explore different optimization scenarios
3. Refine client pricing strategy
4. Proceed with this analysis
```

---

#### Step 11: Generate Additional Deliverables (Optional)

Offer to create:
- **Client proposal deck**: Simplified pricing without internal costs
- **Implementation roadmap**: Phased delivery plan with timelines
- **Prompt library**: All LLM prompts as separate reference doc
- **Cost tracking template**: Spreadsheet for monitoring actual costs

---

## Key Decision Framework

### Model Selection Guide

**Use GPT-4o-mini / Claude Haiku (1 credit) for:**
- Simple classification tasks
- Structured data extraction
- Format conversion
- Yes/no decisions
- Confidence scoring

**Use GPT-4o / Claude Sonnet (3 credits) for:**
- Content generation (emails, messages)
- Complex analysis with context
- Multi-step reasoning
- Persona-based adaptation
- Quality validation

**Use Claude Opus (5 credits) for:**
- Highly nuanced reasoning
- Long-form content creation
- Complex decision-making with many variables
- Mission-critical validation
- Creative problem-solving

### Integration Node Planning

**Each API call = 1 credit:**
- Zoho CRM: GET contact, PATCH contact, POST activity
- Salesforce: Query, Create, Update
- HubSpot: Get record, Update property, Create engagement
- LinkedIn/Enrichment: Company lookup, People search
- Google Sheets: Read range, Append row, Update cell

**Minimize integration nodes by:**
- Batching reads where possible
- Only fetching required fields
- Caching frequently accessed data
- Using webhooks instead of polling

### Quality Validation Decision

**Always include validation (3-5 credits) when:**
- Agent generates customer-facing content
- Output could damage brand reputation
- High risk of hallucinations (factual claims about companies)
- Compliance/legal requirements apply
- Cost of error > cost of validation

**Can skip validation when:**
- Internal use only
- Output is reviewed manually before use
- Low-stakes use case
- Budget is extremely tight
- Human-in-the-loop already present

---

## Pricing Strategy Tips

### Enterprise Client Positioning

**Value Justification Formula:**
```
Agent ROI = (Time Saved × Hourly Rate) + (Revenue Impact) - (Agent Cost)
```

**Example Pitch:**
- Manual effort: 20 hours/month × $50/hr = $1,000/month saved
- Performance lift: +25% conversion = $X,XXX/month revenue impact
- Agent cost: $8,000/month
- **Net ROI**: $[X,XXX]/month positive impact

### Margin Guidelines

**Target Margins by Client Type:**
- **Startup/SMB**: 30-40% (competitive pricing)
- **Mid-Market**: 40-50% (balanced value)
- **Enterprise**: 50-65% (premium positioning, volume discount capacity)

**Adjust margins based on:**
- Client lifetime value potential
- Competitive pressure
- Strategic importance
- Implementation complexity
- Support requirements

### POC Pricing Strategy

**POC should:**
- Prove value (metrics improvement)
- Be short (2-4 weeks maximum)
- Cost client $3K-$7K (enough to show commitment)
- Give you 35-45% margin
- Include clear success criteria
- Have automatic production conversion

**POC Risk Mitigation:**
- Charge upfront (non-refundable)
- Define success metrics before starting
- Use optimized architecture (lower your costs)
- Cap your time investment
- Plan transition to production pricing

---

## Reference: Beam Credit Pricing

### Global Credit Rates

| Component | Credits | Models |
|-----------|---------|--------|
| LLM - Basic | 1 | GPT-4o-mini, Claude Haiku, DeepSeek, Granite3 |
| LLM - Standard | 3 | GPT-4o, Claude Sonnet 3.5, Gemini 2.0 Flash |
| LLM - Advanced | 5 | GPT-o1, Claude Opus, Gemini 2.5 PRO |
| Integration Node | 1 | All API calls |
| Attachment | 3 min | Cost-based: ceil(tokens × cost_per_token / credit_value) |
| Chat Trigger | 0 | Free |
| Webhook Trigger | 0 | Free |
| Other Triggers | 1 | Scheduled, integration-based |

### Beam Plans

**Pro Plan:**
- Monthly Cost: $49 (fixed)
- Credits Included: 2,500
- Cost per Credit: $0.02
- Hard stop at limit

**Enterprise Plan:**
- Usage-based billing
- Base Credit Value: $0.02
- Default Markup: 4.0x ($0.08/credit)
- Configurable per workspace
- Optional credit limits

### Your Cost Scenarios

| Markup | Cost per Credit | When to Use |
|--------|----------------|-------------|
| 4.0x (default) | $0.08 | Standard enterprise pricing |
| 2.5x (negotiated) | $0.05 | High-volume clients, strategic accounts |
| 2.0x (discount) | $0.04 | Very high volume (>500K credits/month) |

---

## Example: Quick Calculation Workflow

**User asks**: "Calculate pricing for a lead qualification agent that runs 10,000 times/month"

**Your response:**
```
Let me design the architecture and calculate pricing for your lead qualification agent.

REQUIREMENTS QUESTIONS:

1. What data sources does it need? (CRM, enrichment APIs, etc.)
2. How complex is the qualification logic? (Simple scoring vs deep analysis)
3. Does it need to generate explanations or just scores?
4. Where does the output go? (CRM update, Slack notification, etc.)
5. Do you need quality validation/confidence scores?

[Wait for answers, then design architecture]

PROPOSED ARCHITECTURE (Example):
- Webhook trigger (0) + CRM fetch (1) + Enrichment API (1) = 2 credits
- Analysis with GPT-4o-mini (1) = 1 credit
- Score logic (0) + CRM update (1) + Slack notify (1) = 2 credits
TOTAL: 6 credits/execution

MONTHLY ECONOMICS:
- Volume: 10,000 executions
- Credits: 60,000
- Your cost @ 4.0x: $4,800/month
- Your cost @ 2.5x: $3,000/month

CLIENT PRICING:
- Per-lead: $0.80-$1.20/lead (40-60% margin)
- Monthly retainer: $8,000-$10,000 (40-52% margin @ 4.0x)

VALUE JUSTIFICATION:
- Manual qualification: 10,000 leads × 5 min = 833 hours = $41,667/month
- Agent cost: $8,000/month
- Savings: $33,667/month (80% cost reduction)

Would you like me to:
1. Generate the full node architecture document
2. Adjust the design for more/less features
3. Explore optimization scenarios
```

---

## Common Agent Archetypes & Typical Costs

### Email Personalization Agent
- **Volume**: 5K-10K/month
- **Credits**: 15-20/execution
- **Monthly Credits**: 75K-200K
- **Your Cost**: $6K-$16K @ 4.0x
- **Client Price**: $12K-$25K

### Lead Qualification Agent
- **Volume**: 10K-50K/month
- **Credits**: 5-8/execution
- **Monthly Credits**: 50K-400K
- **Your Cost**: $4K-$32K @ 4.0x
- **Client Price**: $8K-$50K

### Data Extraction/Processing Agent
- **Volume**: 1K-5K/month
- **Credits**: 10-15/execution (with attachments: 15-25)
- **Monthly Credits**: 10K-125K
- **Your Cost**: $800-$10K @ 4.0x
- **Client Price**: $2K-$18K

### Support Ticket Routing Agent
- **Volume**: 20K-100K/month
- **Credits**: 3-5/execution
- **Monthly Credits**: 60K-500K
- **Your Cost**: $4.8K-$40K @ 4.0x
- **Client Price**: $10K-$70K

---

## Validation Checklist

Before finalizing pricing, verify:

**Architecture:**
- [ ] All required integrations included
- [ ] Appropriate LLM models selected (not over/under-powered)
- [ ] Quality validation included for risky outputs
- [ ] Fallback handling for failures
- [ ] Analytics/logging for monitoring

**Pricing:**
- [ ] Margins meet target (40-60% for enterprise)
- [ ] POC pricing validated (covers costs + profit)
- [ ] Volume assumptions realistic
- [ ] Optimization opportunities identified
- [ ] Scalability considered (what if 2x volume?)

**Client Value:**
- [ ] ROI calculation clear and compelling
- [ ] Pricing competitive but not undervalued
- [ ] Success metrics defined
- [ ] Risk mitigation addressed

**Documentation:**
- [ ] All nodes documented with prompts
- [ ] Credit consumption clear
- [ ] Pricing scenarios provided
- [ ] Implementation phases outlined
- [ ] Next steps actionable

---

## Post-Analysis Actions

After completing pricing calculation:

1. **Save to project** (if applicable)
2. **Update project plan.md** with pricing section
3. **Create client proposal** (simplified version)
4. **Add to skills database** (if novel architecture pattern)
5. **Track in CRM** (if active sales opportunity)

---

**Version**: 1.0
**Created**: 2026-02-03
**Category**: Beam AI | Pricing | Architecture Design
**Estimated Time**: 30-45 minutes for comprehensive analysis
**Prerequisites**: Agent requirements, volume estimates
**Outputs**: Node architecture, credit calculations, pricing recommendations, markdown document
