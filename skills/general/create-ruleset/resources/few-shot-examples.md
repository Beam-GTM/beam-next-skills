# Example Rulesets

Complete, production-quality examples demonstrating every section of the template. Use these as few-shot references when generating new rulesets.

---

## Example 1: Insurance Claims Triage (Multi-Entity, Scoring)

A complete example showing test scenarios with What/Why/Varies cards, output derivation, and scoring formulas.

```markdown
---
schema_version: "2.0"
domain: insurance-claims-triage
created: 2026-03-31
updated: 2026-03-31
---

# Ruleset: Insurance Claims Triage

## USE CASE

### The Context

A mid-size property insurance company operates an AI triage agent that receives new claims and assigns them a priority level + recommended handler. The agent runs as part of the claims intake pipeline — every new claim passes through it within 60 seconds of submission. Human adjusters review the triage decision but rely on it for queue ordering. The company processes ~200 claims/day across home, auto, and commercial property lines.

### Real-World Inputs

The agent receives TWO documents per claim:
1. **Claim form** — structured submission from the policyholder via web portal or mobile app. Contains incident date, description, estimated damage, photos (referenced but not inline), and policy number.
2. **Policy document** — the active policy for the claimant, pulled from the policy management system. Contains coverage types, limits, deductibles, exclusions, and endorsements.

### Three Layers of Difficulty

**Realistic (bread-and-butter):** Clear incident description, straightforward coverage match. Water damage claim on a homeowner's policy with standard water damage coverage. Auto collision with clear fault. These are 70% of production volume — the agent should nail them.

**Challenging (messy but real):** Ambiguous incident descriptions ("something fell on the roof during the storm — not sure what"), multi-peril events (storm caused both water damage and structural damage), policies with endorsements that modify base coverage, claims filed 30+ days after incident, commercial policies with complex sublimits.

**Deceptive (intentionally misleading):** Claims that look routine but have hidden complexity — a water damage claim where the policy has a specific mold exclusion and the description mentions "musty smell" (mold indicator). Pre-existing damage disguised as new. Claims where the estimated damage conveniently sits just below the deductible threshold (potential fraud signal). Policies that appear to cover the peril but have a relevant exclusion buried in endorsements.

### The Litmus Test

> "Would an experienced claims adjuster spend more than 10 seconds questioning this claim-policy pair, or would they immediately see it as either routine or flagged?"

---

<!-- planning:
  purpose: score
  agent_complexity: medium
  input_surface_area: low
  surface_multiplier: 1.0
  base_size: 35
  final_size: 35
  coverage_distribution:
    happy_path: 19
    edge_case: 11
    error_case: 3
    adversarial: 2
  approved_by: user
  approved_at: 2026-03-31T14:00:00Z
-->

---

## INPUT SCHEMA

### Entity 1: Claim Form

**File Type:** JSON object in index.json

**Content:**

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| claim_id | string | Unique claim identifier (CLM-XXXXXX) | yes |
| policy_number | string | Reference to active policy | yes |
| incident_date | date | When the incident occurred | yes |
| report_date | date | When the claim was filed | yes |
| incident_type | enum | water_damage, fire, theft, collision, weather, liability, other | yes |
| description | string | Free-text incident description (50-500 words) | yes |
| estimated_damage | number | Policyholder's damage estimate in USD | no |
| photos_attached | number | Count of attached photo evidence | no |
| location | string | Incident location (address or description) | yes |

**Content Texture:** Claim descriptions range from clear and detailed (60% — specific cause, timeline, damage extent) to vague/brief (30% — "something happened to the roof") to contradictory (10% — conflicting dates or descriptions). Format is always JSON from the web portal.

### Entity 2: Policy Document

**File Type:** JSON object in index.json (70% extracted from PDF via OCR pipeline, 30% direct JSON from policy management API)

**Content:**

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| policy_number | string | Matches claim form | yes |
| policy_type | enum | homeowner, auto, commercial_property, renter | yes |
| coverage_types | array | List of covered perils with limits | yes |
| deductible | number | Per-incident deductible in USD | yes |
| exclusions | array | Specific exclusions and conditions | yes |
| endorsements | array | Policy modifications/riders | no |
| effective_dates | object | Start and end dates | yes |
| insured_value | number | Total insured property value | yes |

**Content Texture:** Policy documents arrive as PDF-extracted text (70%) or JSON API responses (30%). PDF extraction quality varies: clean (60%), minor noise from headers/footers (30%), or garbled tables (10%).

---

## OUTPUT SCHEMA

### Output: Triage Decision

**File Type:** JSON object in index.json

**Format:** JSON

| Field | Type | Description | Value Range | Required |
|-------|------|-------------|-------------|----------|
| claim_id | string | Echo from input | CLM-XXXXXX | yes |
| priority | enum | Triage priority level | low, standard, high, urgent | yes |
| confidence | number | Agent's confidence in the triage | 0.0-1.0 | yes |
| routing | string | Recommended handler/team | adjuster_pool, senior_adjuster, coverage_specialist, SIU, policy_verification | yes |
| reasoning | string | 2-4 sentence explanation | free text | yes |
| flags | array | Risk or attention flags | coverage_gap, fraud_indicator, high_value, policy_issue, late_filing | no |

**Priority assignment formula:**

```
Base priority from incident_type:
  fire, weather (severe) → high
  theft, liability → standard
  water_damage, collision, weather (minor) → standard
  other → low

Modifiers (each can escalate, never de-escalate):
  estimated_damage > insured_value × 0.5 → escalate one level
  filing_delay > 30 days → escalate one level + add late_filing flag
  exclusion_may_apply → escalate to high minimum
  fraud_signals ≥ 2 → escalate to urgent + route to SIU
  policy_expired → urgent + route to policy_verification

Final: priority = max(base_priority, all_modifier_escalations)
```

---

## OUTPUT DERIVATION PROCEDURE

1. **Extract claim details** — Pull incident_type, description keywords, estimated_damage, filing delay (report_date - incident_date), and photo count from claim form.
2. **Extract policy coverage** — Pull covered perils, exclusions, endorsements, deductible, and limits from policy document.
3. **Match coverage** — Check if incident_type falls under a covered peril. Check if any exclusion applies. Check if endorsements modify the match.
4. **Compute base priority** — Use the incident_type → priority mapping from the formula above.
5. **Apply modifiers** — Check each modifier condition. Escalate priority as specified. Never de-escalate.
6. **Determine routing** — Based on final priority and which modifiers fired, select the handler.
7. **Generate reasoning** — Summarize: what coverage applies, what complications exist, why this priority was assigned.
8. **Validate** — Check: Does the priority match the modifiers? Does the routing match the priority? Is the reasoning consistent with the flags?

**Intermediate artifact:**

```
Claim: CLM-789012 (water_damage, estimated $15,000)
Policy: HO-456, homeowner, covers water damage
  - Exclusion: "flood damage from external water sources"
  - Description mentions: "heavy rain, basement flooding"

Coverage match: water_damage → covered
Exclusion check: "basement flooding from rain" → flood exclusion MAY apply
Base priority: standard (water_damage)
Modifier: exclusion_may_apply → escalate to high
Routing: senior_adjuster (exclusion requires interpretation)
Flags: [coverage_gap]
```

---

## TEST SCENARIOS

### Clear Coverage, Clean Data (19 samples)

**What:** Complete claim forms with clear incident descriptions paired with clean policy documents. Incident type is directly covered with no exclusion ambiguity. Filed within 7 days.

**Why it's hard:** Pure triage accuracy. The agent must correctly match coverage, assign priority, and route — the baseline that must work flawlessly before testing harder cases.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Claim completeness | All fields present | 90 |
| Claim completeness | Missing photos only | 10 |
| Description quality | Clear and detailed | 80 |
| Description quality | Standard | 20 |
| Policy extraction | Clean text | 90 |
| Policy extraction | Minor noise | 10 |
| Coverage match | Direct coverage, no exclusions | 100 |
| Filing delay | Same day to 7 days | 90 |
| Filing delay | 8-30 days | 10 |

### Ambiguous Coverage, Messy Data (11 samples)

**What:** Claims with vague descriptions, endorsements that modify coverage, multi-peril incidents, or late filings. Policy docs may have extraction noise or garbled tables.

**Why it's hard:** Multiple ambiguities compound — a vague description + an endorsement that modifies base coverage + a late filing creates uncertainty the agent must reason through. The agent cannot default to "standard" — it must identify which modifier applies and escalate appropriately.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Claim completeness | Vague description | 40 |
| Claim completeness | Missing estimated_damage | 30 |
| Claim completeness | Late filing | 30 |
| Description quality | Vague/brief | 50 |
| Description quality | Contradictory | 20 |
| Description quality | Clear | 30 |
| Policy extraction | Minor noise | 40 |
| Policy extraction | Garbled tables | 20 |
| Policy extraction | Clean | 40 |
| Coverage match | Endorsement modifies coverage | 40 |
| Coverage match | Ambiguous exclusion | 40 |
| Coverage match | Multi-peril | 20 |
| Filing delay | 8-30 days | 40 |
| Filing delay | 30+ days | 30 |
| Filing delay | Within 7 days | 30 |

### Broken Input (3 samples)

**What:** Claims with missing required fields or contradictory dates paired with garbled or incomplete policy documents. The policy may be expired or for the wrong type.

**Why it's hard:** The agent must recognize that the data is insufficient for confident triage — route to verification rather than guessing, and flag the specific issue (expired policy, missing sections) rather than producing a low-confidence triage.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Claim completeness | Missing required fields | 60 |
| Claim completeness | Contradictory dates | 40 |
| Policy extraction | Garbled | 60 |
| Policy extraction | Missing sections | 40 |
| Coverage match | Policy expired | 50 |
| Coverage match | Wrong policy type | 50 |

### Deceptive Input (2 samples)

**What:** Claims that are intentionally well-written and complete — clean, detailed, polished. But they contain hidden signals: a coverage exclusion buried in endorsements, or multiple subtle fraud indicators that individually are explainable but collectively are suspicious.

**Why it's hard:** The deception is in the polish. Unlike messy edge cases, these look routine at first glance. The agent must dig deeper — checking endorsement interactions, cross-referencing filing delays with damage estimates, spotting that the "musty smell" in a water damage claim triggers a mold exclusion.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Claim completeness | Full (intentionally complete) | 100 |
| Description quality | Clean, detailed (deception requires polish) | 100 |
| Coverage match | Appears covered but hidden exclusion | 50 |
| Coverage match | Fraud signals present but subtle | 50 |

---

## FEW-SHOT EXAMPLES

### Example 1: Happy Path — Clear Water Damage Claim

**Input:**
```json
{
  "claim_form": {
    "claim_id": "CLM-234567",
    "policy_number": "HO-891234",
    "incident_date": "2026-03-28",
    "report_date": "2026-03-28",
    "incident_type": "water_damage",
    "description": "Kitchen sink supply line burst while we were at work. Came home to standing water in the kitchen and dining room. Hardwood floors are warped and drywall behind cabinets is saturated. Shut off water main immediately. Plumber confirmed the copper fitting failed due to corrosion.",
    "estimated_damage": 12000,
    "photos_attached": 8,
    "location": "742 Evergreen Terrace, Springfield, IL 62704"
  },
  "policy": {
    "policy_number": "HO-891234",
    "policy_type": "homeowner",
    "coverage_types": ["water_damage", "fire", "theft", "weather", "liability"],
    "deductible": 1000,
    "exclusions": ["flood_external", "earthquake", "mold_remediation_over_10k"],
    "endorsements": [],
    "effective_dates": {"start": "2025-07-01", "end": "2026-07-01"},
    "insured_value": 350000
  }
}
```

**Expected Output:**
```json
{
  "claim_id": "CLM-234567",
  "priority": "standard",
  "confidence": 0.95,
  "routing": "adjuster_pool",
  "reasoning": "Internal water damage from burst pipe is clearly covered under the homeowner policy's water damage provision. No exclusions apply — this is an internal plumbing failure, not external flood. Estimated damage of $12,000 is well within policy limits. Same-day filing with photo evidence supports straightforward processing.",
  "flags": []
}
```

**Derivation:** incident_type=water_damage → base priority standard. No modifiers fire: damage ($12k) < insured_value × 0.5 ($175k), same-day filing, no exclusion applies (flood exclusion is for external sources only), no fraud signals. Final: standard priority, route to general adjuster pool.

### Example 2: Edge Case — Ambiguous Exclusion

**Input:**
```json
{
  "claim_form": {
    "claim_id": "CLM-345678",
    "policy_number": "HO-567890",
    "incident_date": "2026-03-15",
    "report_date": "2026-03-29",
    "incident_type": "water_damage",
    "description": "Heavy rainstorm last week. Noticed water stains on basement ceiling and musty smell. Carpet is damp. Not sure if it came through the foundation or the window well.",
    "estimated_damage": null,
    "photos_attached": 2,
    "location": "1234 Oak Street, Columbus, OH 43215"
  },
  "policy": {
    "policy_number": "HO-567890",
    "policy_type": "homeowner",
    "coverage_types": ["water_damage", "fire", "theft", "weather"],
    "deductible": 2500,
    "exclusions": ["flood_external", "mold_remediation_over_10k", "gradual_seepage"],
    "endorsements": [{"type": "water_backup", "sublimit": 5000}],
    "effective_dates": {"start": "2025-01-01", "end": "2026-01-01"},
    "insured_value": 280000
  }
}
```

**Expected Output:**
```json
{
  "claim_id": "CLM-345678",
  "priority": "high",
  "confidence": 0.55,
  "routing": "senior_adjuster",
  "reasoning": "Water damage source is ambiguous — could be covered internal water damage, excluded external flood, or excluded gradual seepage. The 'musty smell' suggests possible mold, which has a $10k remediation sublimit. Policy has a water backup endorsement that may apply if the cause was drain backup. Filing was 14 days after incident. A senior adjuster needs to determine the water source before coverage can be confirmed.",
  "flags": ["coverage_gap"]
}
```

**Derivation:** incident_type=water_damage → base priority standard. Modifiers: flood exclusion MAY apply (rain-related, basement) → escalate to high. Ambiguous source (foundation vs window well vs backup) means coverage is uncertain. Musty smell → potential mold adds complexity. 14-day delay is within normal range, no escalation. Final: high priority, route to senior adjuster who can inspect and determine cause.

### Example 3: Adversarial — Subtle Fraud Signals

**Input:**
```json
{
  "claim_form": {
    "claim_id": "CLM-456789",
    "policy_number": "AU-123456",
    "incident_date": "2026-03-20",
    "report_date": "2026-03-28",
    "incident_type": "theft",
    "description": "Vehicle was parked in my driveway overnight. In the morning the car was gone. I have comprehensive coverage. The car is a 2024 BMW X5 M Sport, purchased last year. I'd like to file for the full insured value. I have all purchase receipts and the original window sticker.",
    "estimated_damage": 72000,
    "photos_attached": 0,
    "location": "5678 Maple Drive, Phoenix, AZ 85001"
  },
  "policy": {
    "policy_number": "AU-123456",
    "policy_type": "auto",
    "coverage_types": ["collision", "comprehensive", "liability"],
    "deductible": 500,
    "exclusions": ["wear_and_tear", "mechanical_failure"],
    "endorsements": [{"type": "gap_coverage", "added": "2026-03-01"}],
    "effective_dates": {"start": "2025-06-01", "end": "2026-06-01"},
    "insured_value": 75000
  }
}
```

**Expected Output:**
```json
{
  "claim_id": "CLM-456789",
  "priority": "urgent",
  "confidence": 0.70,
  "routing": "SIU",
  "reasoning": "Vehicle theft claim with multiple fraud indicators: (1) gap coverage endorsement added just 20 days before the incident — recent coverage enhancement before a major claim, (2) 8-day filing delay for a theft which is typically reported immediately, (3) estimated damage of $72,000 is 96% of insured value — unusually precise and high, (4) no photos despite claiming the car was in the driveway. Each signal individually is explainable, but the combination warrants SIU review.",
  "flags": ["fraud_indicator", "high_value"]
}
```

**Derivation:** incident_type=theft → base priority standard. Modifiers: estimated_damage ($72k) > insured_value × 0.5 ($37.5k) → escalate one level to high. Fraud signals: recent gap coverage addition (20 days), 8-day filing delay for theft, estimate near full value, zero photos = 4 fraud signals ≥ 2 → escalate to urgent + route to SIU. Flags: fraud_indicator + high_value.

---

## ANTI-PATTERNS

1. **Cookie-cutter descriptions** — All claim descriptions follow the same sentence structure ("X happened. Y was damaged. Z was the cause."). Why it's wrong: real descriptions vary wildly in detail, grammar, and emotional tone.
2. **Obvious fraud** — Adversarial examples with cartoonish red flags ("my brand new Ferrari was stolen from an unlocked garage the day after I doubled my coverage"). Why it's wrong: real fraud is subtle — individual signals are each explainable.
3. **Perfect policy documents** — All policies have clean text with no extraction artifacts. Why it's wrong: 30% of policy PDFs have noisy extraction (garbled tables, merged cells, missing sections).
4. **Uniform filing delay** — All claims filed same day. Why it's wrong: filing delay distribution varies by incident type (theft = fast, water damage = sometimes delayed, weather = often delayed due to widespread damage).
```

---

## Example 2: Email Classification (Single-Entity, Simple)

A simpler example for a single-entity agent with no pairing strategy needed.

```markdown
---
schema_version: "2.0"
domain: email-classification
created: 2026-03-31
updated: 2026-03-31
---

# Ruleset: Support Email Classification

## USE CASE

### The Context

A B2B SaaS company's support team receives 300+ emails daily. An AI classifier tags each email with a category and urgency level, routing it to the right team queue. The agent processes the raw email body — no metadata, no thread history, just the text of the latest message.

### Real-World Inputs

Plain text email bodies, ranging from one-line questions to multi-paragraph complaints with inline screenshots (referenced as "[image]" placeholders). Emails arrive in English (85%) and German (15%). Some are auto-forwarded from other systems and include forwarding headers as noise.

### Three Layers of Difficulty

**Realistic:** Clear single-topic emails. "I can't log into my account" → access_issue. "How do I export my data?" → feature_question.

**Challenging:** Multi-topic emails ("I can't log in AND my last export was wrong"), emails in broken English/German mix, auto-forwarded emails with noisy headers, extremely short emails ("it's broken again").

**Deceptive:** Emails that look like one category but are another — a "feature request" that's actually a complaint disguised as a suggestion, or a "billing question" that's actually a cancellation threat.

### The Litmus Test

> "Would a support agent reading just this email body route it to the same team the AI did?"

---

<!-- planning:
  purpose: score
  agent_complexity: easy
  input_surface_area: medium
  surface_multiplier: 1.0
  base_size: 20
  final_size: 20
  coverage_distribution:
    happy_path: 11
    edge_case: 6
    error_case: 2
    adversarial: 1
  approved_by: user
  approved_at: 2026-03-31T14:00:00Z
-->

---

## INPUT SCHEMA

### Entity 1: Email Body

**File Type:** text string in index.json

**Content:**

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| email_body | string | Raw email text, 10-2000 words | yes |

**Content Texture:** Emails range from terse one-liners ("it's broken again") to multi-paragraph complaints with inline screenshot references ("[image]"). Three length profiles: Short (<50 words, 25%), Medium (50-200 words, 55%), Long (200+, 20%). Language is English (70%), German (20%), or mixed EN/DE (10%). Some include forwarding headers or auto-generated signatures as noise.

---

## OUTPUT SCHEMA

### Output: Classification

**File Type:** JSON object in index.json

**Format:** JSON

| Field | Type | Description | Value Range | Required |
|-------|------|-------------|-------------|----------|
| category | enum | Email topic | access_issue, billing, feature_question, bug_report, complaint, cancellation, general | yes |
| urgency | enum | How quickly it needs attention | low, medium, high, critical | yes |
| confidence | number | Classification confidence | 0.0-1.0 | yes |
| reasoning | string | One-sentence explanation | free text | yes |

---

## OUTPUT DERIVATION PROCEDURE

1. **Scan for keywords** — Check email body for category indicator words (e.g., "password"/"login" → access_issue, "invoice"/"charge" → billing, "cancel"/"terminate" → cancellation).
2. **Assess sentiment** — Negative/angry tone escalates urgency. Neutral tone keeps default urgency.
3. **Handle multi-topic** — If multiple categories detected, assign the highest-urgency one as primary.
4. **Assign urgency** — cancellation/complaint → high minimum. bug_report → medium minimum. Others → low default, escalated by sentiment.
5. **Validate** — Category and urgency must be consistent with the reasoning sentence.

---

## TEST SCENARIOS

### Clear Single-Topic Emails (11 samples)

**What:** Standard support emails with one clear topic — login issues, billing questions, bug reports, feature requests. Well-written in English or German with clean formatting.

**Why it's hard:** Baseline accuracy test. The agent must correctly classify the topic and assign appropriate urgency. Even "easy" emails can have nuanced urgency (a bug report that blocks a workflow is high, not medium).

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Topics | Single topic, clear category | 100 |
| Language | English | 80 |
| Language | German | 20 |
| Length | Medium | 60 |
| Length | Short | 25 |
| Length | Long | 15 |
| Noise | Clean | 80 |
| Noise | Light signature | 20 |

### Ambiguous &amp; Messy Emails (6 samples)

**What:** Multi-topic emails ("billing AND API error"), mixed EN/DE language, auto-forwarded messages with noisy headers, or extremely short emails ("it's broken again") with no context.

**Why it's hard:** Multiple ambiguities at once — the agent must decide which topic is primary (highest urgency wins), handle mixed-language parsing, and extract signal from noise. An extremely short email requires inference rather than keyword matching.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Topics | Multi-topic | 40 |
| Topics | Ambiguous single topic | 40 |
| Topics | Extremely short | 20 |
| Language | Mixed EN/DE | 30 |
| Language | Broken grammar | 30 |
| Language | Standard | 40 |
| Noise | Forwarding headers | 40 |
| Noise | Auto-generated | 30 |
| Noise | Clean | 30 |

### Non-Emails (2 samples)

**What:** Content that isn't actually a support request — empty email bodies, out-of-office auto-replies, or system-generated notifications that landed in the support inbox.

**Why it's hard:** The agent must recognize these are not classifiable support requests and handle them gracefully (e.g., "general" category with low urgency) rather than forcing a classification.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Content | Empty/near-empty body | 50 |
| Content | Non-email (auto-reply, OOO) | 50 |

### Disguised Category (1 sample)

**What:** A polished, well-written email that appears to be one category but is actually another — a "feature request" that's really a complaint, or a "billing question" that's a cancellation threat.

**Why it's hard:** Surface-level keyword matching would misclassify it. The agent must read the underlying intent, not just the words. The deception is intentional — the sender is being indirect about their real concern.

**Varies:**

| Dimension | Option | % |
|-----------|--------|---|
| Content | Disguised category (complaint as feature request) | 100 |

---

## FEW-SHOT EXAMPLES

### Example 1: Happy Path — Clear Bug Report

**Input:**
```
Since yesterday's update, the dashboard export button generates a CSV with duplicate header rows.
Steps to reproduce: Settings > Export > CSV format > Download.
Browser: Chrome 124, macOS. This is blocking our weekly reporting.
```

**Expected Output:**
```json
{
  "category": "bug_report",
  "urgency": "high",
  "confidence": 0.95,
  "reasoning": "Clear bug report with reproduction steps; marked high urgency because it blocks a recurring workflow."
}
```

### Example 2: Edge Case — Multi-Topic Mixed Language

**Input:**
```
Hi, ich habe zwei Probleme. First, my invoice from March shows the wrong amount — it says €299 but we're on the €199 plan. Zweitens, the API endpoint /v2/users returns 500 errors since this morning. Bitte um schnelle Hilfe.
```

**Expected Output:**
```json
{
  "category": "bug_report",
  "urgency": "high",
  "confidence": 0.65,
  "reasoning": "Multi-topic (billing discrepancy + API 500 error) in mixed EN/DE. Classified as bug_report due to higher urgency of the API outage; billing issue flagged in reasoning."
}
```

---

## ANTI-PATTERNS

1. **Keyword-only emails** — Emails that are just category keywords strung together ("login password access help"). Why it's wrong: real emails have context, not just keywords.
2. **Identical tone** — All emails are polite and professional. Why it's wrong: real support emails range from terse to angry to apologetic.
3. **English-only adversarial** — All tricky examples are in English. Why it's wrong: ambiguity in German (or mixed language) is a real production challenge.
4. **Perfect grammar** — All emails are grammatically correct. Why it's wrong: real emails have typos, incomplete sentences, and auto-correct artifacts.
```
