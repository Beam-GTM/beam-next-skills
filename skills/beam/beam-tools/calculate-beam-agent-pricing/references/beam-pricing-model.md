# Beam Pricing Model Reference

**Last Updated**: 2026-02-03
**Source**: Beam Billing & Usage PRD

---

## Credit-Based Pricing System

Beam uses a unified credit-based pricing model across all plans with transparent, predictable costs.

### Formula

```
Total Credits = Σ(Triggers) + Σ(LLM Calls) + Σ(Integration Nodes) + Σ(Attachments)

Pro Plan Cost = Total Credits × $0.02
Enterprise Cost = Total Credits × Base Credit Value × Markup
```

---

## Global Credit Rates

**Admin Configurable** - Applied globally across all workspaces

| Component | Credits | Notes |
|-----------|---------|-------|
| **LLM - Basic** | 1 | GPT-4o-mini, Claude Haiku, DeepSeek, Granite3 |
| **LLM - Standard** | 3 | GPT-4o, Claude Sonnet variants, Gemini 2.0 Flash |
| **LLM - Advanced** | 5 | GPT-o1, Claude Opus, Gemini 2.5 PRO |
| **Integration Node** | 1 | All integration API calls |
| **Attachment** | 3 Min | Cost-based: ceil(tokens × cost_per_token / credit_value) |
| **Chat Trigger** | 0 | Free |
| **Webhook Trigger** | 0 | Free |
| **Other Triggers** | 1 | Scheduled, integration-based |

---

## Beam Plans

### Free Plan

| Parameter | Value |
|-----------|-------|
| **Monthly Cost** | $0 |
| **Credits Included** | 200 |
| **Cost per Credit** | $0.02 |
| **Credit Limit** | Hard stop at 200 |
| **Overage** | Not allowed |
| **Rollover** | No |

---

### Pro Plan

| Parameter | Value |
|-----------|-------|
| **Monthly Cost** | $49 (fixed) |
| **Credits Included** | 2,500 |
| **Cost per Credit** | $0.02 |
| **Markup** | None (1.0x) |
| **Credit Limit** | Hard stop at 2,500 |
| **Overage** | Not allowed |
| **Billing** | Automatic (Stripe) |
| **Rollover** | No |

**Credit Limit Behavior:**
- Low credit alert when running low
- Tasks stop at 0 credits
- Workspace remains accessible (view-only)
- Failed payment: Workspace accessible, tasks stopped

---

### Enterprise Plan

| Parameter | Value |
|-----------|-------|
| **Monthly Cost** | Usage-based |
| **Credits Included** | Unlimited |
| **Base Credit Value** | $0.02 (configurable per workspace) |
| **Markup** | 4.0x default (configurable per workspace) |
| **Effective Cost** | $0.08/credit default |
| **Credit Limit** | Optional (can set per workspace) |
| **Allow After Limit** | Yes (configurable) |
| **Billing** | Offline/Custom invoicing |
| **Rollover** | N/A |

**Configurable Settings** (per workspace):
- Base credit value
- Markup multiplier
- Credit limit (optional)
- Usage alert thresholds

---

## Your Cost Scenarios (Enterprise Plan)

| Markup | Cost per Credit | Typical Use Case |
|--------|----------------|------------------|
| **4.0x** (default) | **$0.08** | Standard enterprise pricing |
| **2.5x** (negotiated) | **$0.05** | High-volume clients (>100K credits/month) |
| **2.0x** (volume discount) | **$0.04** | Strategic accounts (>500K credits/month) |

**Negotiation Leverage:**
- Volume commitments (6-12 month contracts)
- Strategic partnership potential
- Multiple workspace deployments
- Early adopter/reference customer

---

## Attachment Processing Details

**Formula**: `Credits = max(MIN_CREDITS, ceil(total_tokens × COST_PER_TOKEN / CREDIT_VALUE))`

**Variables:**
- `COST_PER_TOKEN`: $0.000000158 (GPT-4o-mini OCR, configurable)
- `CREDIT_VALUE`: $0.02 (Pro) or configurable (Enterprise)
- `MIN_CREDITS`: 3 (default, configurable)

**Pricing Structure:**
- **Minimum charge**: 3 credits
- **Cost-based scaling**: Reflects actual OCR model costs
- **Always rounds up**: Partial credits → next whole credit

**Examples** (GPT-4o-mini @ $0.000000158/token):
- Small PDF (2 pages, ~2K tokens): **3 credits** (minimum)
- Contract (10 pages, ~8K tokens): **3 credits** (minimum)
- Report (50 pages, ~35K tokens): **3 credits** (minimum)
- Large CSV (5K rows, ~500K tokens): **4 credits**
- Massive PDF (1M tokens): **8 credits**

**Cost Efficiency:**
- Old formula: 1 credit per 1,000 tokens
- New formula: 1 credit per ~126,582 tokens
- **Result**: ~126x more economical for large documents

---

## Model Selection Guide

### LLM - Basic (1 Credit)

**Models:**
- GPT-4o-mini
- Claude 3.5 Haiku
- DeepSeek
- Granite3

**Best For:**
- Simple classification (persona, sentiment, category)
- Structured data extraction
- Yes/no decisions
- Confidence scoring
- Format conversion
- Quick analysis without deep context

**When NOT to Use:**
- Complex multi-step reasoning
- Creative content generation
- Nuanced decision-making
- Long-form content

---

### LLM - Standard (3 Credits)

**Models:**
- GPT-4o
- Claude 3.5 Sonnet
- Gemini 2.0 Flash
- Claude 3 Sonnet

**Best For:**
- Content generation (emails, messages, responses)
- Context-aware personalization
- Multi-step reasoning
- Quality validation
- Complex analysis with multiple variables
- Persona-based adaptation

**When NOT to Use:**
- Simple classification (use Basic)
- Extremely complex reasoning (use Advanced)
- Budget is very tight (try Basic first)

---

### LLM - Advanced (5 Credits)

**Models:**
- GPT-o1 (reasoning model)
- Claude Opus
- Gemini 2.5 PRO

**Best For:**
- Highly nuanced reasoning
- Complex decision-making with many variables
- Mission-critical validation
- Creative problem-solving
- Long-form content requiring coherence
- Strategic analysis

**When NOT to Use:**
- Simple tasks (massive overkill)
- High-volume use cases (cost prohibitive)
- Fast response needed (slower models)
- Standard personalization (Sonnet sufficient)

---

## Integration Node Pricing

**Every API call = 1 credit**

### Common Integrations

**CRM Systems:**
- Zoho CRM: GET contact (1), PATCH contact (1), POST activity (1)
- Salesforce: Query (1), Create (1), Update (1)
- HubSpot: Get record (1), Update property (1), Create engagement (1)

**Enrichment APIs:**
- LinkedIn Sales Navigator: Company lookup (1), People search (1)
- Clearbit: Enrich company (1), Find person (1)
- Hunter.io: Email finder (1), Verify email (1)

**Communication:**
- Gmail API: Send email (1), Read email (1)
- Slack: Post message (1), Get channel history (1)
- Twilio: Send SMS (1)

**Data Storage:**
- Google Sheets: Read range (1), Append row (1), Update cell (1)
- Airtable: Query records (1), Create record (1), Update record (1)
- PostgreSQL: Query (1), Insert (1), Update (1)

**Optimization Tips:**
- Batch reads where API supports it (still 1 credit)
- Only fetch required fields
- Cache frequently accessed static data
- Use webhooks instead of polling (0 vs 1 credit)

---

## Trigger Pricing

| Trigger Type | Credits | Use Case |
|--------------|---------|----------|
| **Webhook** | 0 | External system pushes data to agent |
| **Chat/Manual** | 0 | User initiates task manually |
| **Scheduled** | 1 | Agent runs on cron schedule |
| **Integration-Based** | 1 | Agent polls external system |

**Cost Optimization:**
- Prefer webhook triggers over scheduled polling
- Use chat triggers for low-volume testing
- Scheduled triggers accumulate costs (1 credit per run even if no work)

---

## Credit Consumption Examples

### Simple Lead Qualification Agent

```
Webhook trigger (0) +
CRM fetch contact (1) +
LLM Basic classification (1) +
CRM update score (1) +
Slack notification (1)
= 4 credits/execution
```

**Monthly at 10K executions:**
- 40,000 credits
- Cost @ 4.0x: $3,200
- Cost @ 2.5x: $2,000

---

### Email Personalization Agent

```
Webhook (0) +
Fetch contact (1) + Fetch company (1) + Fetch campaign (1) +
Persona classification Basic (1) + Context synthesis Basic (1) +
Subject generation Standard (3) + Body generation Standard (3) + CTA Basic (1) +
Quality check Standard (3) +
Update CRM (1) + Send email (1) + Log analytics (1)
= 18 credits/execution
```

**Monthly at 8K executions:**
- 144,000 credits
- Cost @ 4.0x: $11,520
- Cost @ 2.5x: $7,200

---

### Document Processing Agent (with attachments)

```
Webhook (0) +
Attachment processing (3-8 depending on size) +
LLM Standard extraction (3) +
Data validation Basic (1) +
Database insert (1) +
Notification (1)
= 9-14 credits/execution
```

**Monthly at 2K documents:**
- 18,000-28,000 credits
- Cost @ 4.0x: $1,440-$2,240
- Cost @ 2.5x: $900-$1,400

---

## Profitability Metrics

### Pro Plan (Not Typical for Your Use)

- **Average Margin**: 59%
- **Margin Range**: 19-82%
- **Target Margin**: 55-65%
- **Status**: ✅ Sustainable for small workloads

### Enterprise Plan (Your Primary Model)

- **Average Margin**: 88%
- **Margin Range**: 80-98%
- **Target Margin**: 85-90%
- **Volume Discount Capacity**: Can offer 30-50% discount while maintaining >60% margins
- **Status**: ✅ Highly profitable

### Your Margin Goals (Building for Clients)

**Target Margins by Client Type:**
- **Startup/SMB**: 30-40% (competitive pricing)
- **Mid-Market**: 40-50% (balanced value)
- **Enterprise**: 50-65% (premium positioning)

**Factors Affecting Margin:**
- Your negotiated markup (4.0x vs 2.5x)
- Client volume commitments
- Implementation complexity
- Support requirements
- Competitive pressure
- Strategic account value

---

## Cost Calculation Template

### Step 1: Count Nodes by Type

| Type | Count | Credits Each | Total |
|------|-------|--------------|-------|
| LLM Basic | [N] | 1 | [N] |
| LLM Standard | [N] | 3 | [N×3] |
| LLM Advanced | [N] | 5 | [N×5] |
| Integration | [N] | 1 | [N] |
| Attachment | [N] | 3-8 avg | [N×5] |
| Triggers (paid) | [N] | 1 | [N] |
| **TOTAL** | - | - | **[SUM]** |

### Step 2: Calculate Monthly Cost

```
Monthly Credits = Credits per Execution × Monthly Volume

Your Cost @ 4.0x = Monthly Credits × $0.08
Your Cost @ 2.5x = Monthly Credits × $0.05
Your Cost @ 2.0x = Monthly Credits × $0.04
```

### Step 3: Price to Client

```
Client Price = Your Cost / (1 - Target Margin %)

Example (50% margin target):
Your Cost: $10,000
Client Price: $10,000 / 0.50 = $20,000/month
```

---

## Optimization Strategies

### High-Impact, Low-Risk Optimizations

1. **Remove Optional Enrichment** (-1-2 credits)
   - Skip LinkedIn/Clearbit if CRM has sufficient data
   - Add back later if needed

2. **Use Basic Models for Simple Tasks** (-2 credits per swap)
   - Classification → Basic instead of Standard
   - Validation → Basic instead of Standard (if simple checks)

3. **Cache Repeated Analyses** (-0.5-1 avg credits)
   - Store persona classifications for repeat contacts
   - Cache company analyses

4. **Merge Similar Nodes** (-1-2 credits)
   - Combine multiple analysis steps into one LLM call
   - Batch similar API calls where supported

5. **Smart Validation** (-3 credits conditionally)
   - Only validate first email in campaign
   - Skip validation for low-risk outputs
   - Sample validation (10% of executions)

### Medium-Impact Optimizations (Consider Trade-offs)

1. **Simplify CTA/Subject Generation** (-1-2 credits)
   - Use template variations instead of full generation
   - Basic model instead of Standard

2. **Reduce Context Fetching** (-1-2 credits)
   - Only fetch data that materially impacts output
   - Lazy load optional enrichment

3. **Conditional Features** (-1-3 credits)
   - Only enrich for high-value prospects
   - Skip analytics for test executions

### Low-Impact (Not Usually Worth It)

1. **Skip Quality Validation** (-3 credits) ❌
   - High risk of poor output
   - Reputational damage potential
   - Only skip for internal/low-stakes use

2. **Use Basic for Everything** (-6-9 credits) ❌
   - Quality drops 40-60%
   - Defeats purpose of AI personalization
   - Client won't see value

---

## Quick Reference: Cost Per Credit

| Markup | Base ($0.02) | Per 1K Credits | Per 10K Credits | Per 100K Credits |
|--------|--------------|----------------|-----------------|------------------|
| 1.0x | $0.02 | $20 | $200 | $2,000 |
| 2.0x | $0.04 | $40 | $400 | $4,000 |
| 2.5x | $0.05 | $50 | $500 | $5,000 |
| 4.0x | $0.08 | $80 | $800 | $8,000 |

---

**Document Version**: 1.0
**Last Updated**: 2026-02-03
**Source**: Beam PRD - Billing & Usage Documentation
