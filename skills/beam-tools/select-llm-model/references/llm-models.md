# LLM Model Reference

**Last Updated**: February 2026

Complete specifications for supported LLM models in Beam AI agents.

---

## Pricing Overview

### Google Gemini

| Model | Input (per 1M) | Output (per 1M) | Context | Max Output |
|-------|----------------|-----------------|---------|------------|
| **Gemini 3 Pro** | $2.00-$4.00 | $12.00-$18.00 | 1M | 64K |
| **Gemini 2.5 Pro** | $1.25 | $10.00 | 1M (2M planned) | 64K |
| **Gemini 3 Flash** | $0.50 | $3.00 | 1M | 64K |

### OpenAI GPT

| Model | Input (per 1M) | Output (per 1M) | Context | Max Output |
|-------|----------------|-----------------|---------|------------|
| **GPT-4.1** | $2.00 | $8.00 | 1M | 32K |
| **GPT-4o** | $2.50 | $10.00 | 128K | 16K |
| **GPT-4o-mini** | $0.15 | $0.60 | 128K | 16K |
| **GPT-5** | $1.25 | $10.00 | 400K | 128K |
| **GPT-5.2** | $1.75 | $14.00 | 400K | 128K |

### Anthropic Claude

| Model | Input (per 1M) | Output (per 1M) | Context | Max Output |
|-------|----------------|-----------------|---------|------------|
| **Claude 3 Sonnet** | $3.00 | $15.00 | 200K | 4K |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 | 200K | 8K |
| **Claude 3.7 Sonnet** | $3.00 | $15.00 | 200K | 128K (extended) |
| **Claude 4 Sonnet** | $3.00 | $15.00 | 200K | 8K |
| **Claude 4.5 Sonnet** | $3.00 ($6.00 >200K) | $15.00 ($22.50 >200K) | 200K (1M beta) | 64K |
| **Claude 4.5 Opus** | $5.00 | $25.00 | 200K | 64K |

---

## Speed & Latency

### Fastest (Real-time suitable)

| Model | Time to First Token | Throughput | Best For |
|-------|---------------------|------------|----------|
| **Gemini 3 Flash** | 0.21-0.37s | ~218 tokens/s | Real-time apps, fast agents |
| **GPT-4o-mini** | Very fast | High | High-volume, cost-sensitive |
| **GPT-4.1** | ~0.39s | High | Long-context fast retrieval |

### Balanced (Standard use)

| Model | Time to First Token | Notes |
|-------|---------------------|-------|
| **GPT-5** | Medium | Good for most applications |
| **Gemini 2.5 Pro** | Medium | Solid reasoning performance |
| **Claude 4.5 Sonnet** | Medium | Reliable general use |

### Slower (Deep reasoning)

| Model | Latency | Notes |
|-------|---------|-------|
| **Gemini 3 Pro** (Deep Think) | Variable | Extended thinking mode |
| **Claude 4.5 Opus** | 2-4s typical | Use async for intensive tasks |
| **GPT-5.2** (Thinking) | Variable | Best reasoning, worth the wait |

---

## Best Use Cases

### By Task Type

| Task Type | Primary Choice | Alternative | Avoid |
|-----------|----------------|-------------|-------|
| **Simple extraction** | GPT-4o-mini | Gemini 3 Flash | Opus (overkill) |
| **Data validation** | Claude 4.5 Sonnet | GPT-5 | - |
| **Complex reasoning** | GPT-5.2 | Claude 4.5 Opus | Mini models |
| **Code generation** | Claude 4.5 Opus | GPT-4.1 | Gemini |
| **Long documents** | GPT-4.1 | Gemini 2.5 Pro | Claude 3 Sonnet |
| **High-volume batch** | GPT-4o-mini | Claude + caching | Opus |
| **Real-time chat** | Gemini 3 Flash | GPT-4o-mini | Opus |

### By Context Size

| Context Need | Best Options |
|--------------|--------------|
| **<10K tokens** | GPT-4o-mini, Gemini 3 Flash |
| **10K-100K** | Claude 4.5 Sonnet, GPT-4o, GPT-5 |
| **100K-400K** | GPT-5, GPT-5.2, Gemini 2.5 Pro |
| **400K-1M** | GPT-4.1, Gemini 3 Pro, Gemini 2.5 Pro |
| **>1M** | Gemini 3 Pro (1M), GPT-4.1 (1M) |

### By Output Size

| Output Need | Best Options |
|-------------|--------------|
| **<4K tokens** | Any model |
| **4K-16K** | GPT-4o, GPT-4o-mini, Claude 3.5+ |
| **16K-64K** | Claude 4.5 (Sonnet/Opus), Gemini, GPT-4.1 |
| **64K-128K** | GPT-5, GPT-5.2, Claude 3.7 Sonnet |

---

## Known Limitations

### Gemini

| Model | Limitations |
|-------|-------------|
| **Gemini 3 Pro** | Higher latency with Deep Think; expensive for high-volume |
| **Gemini 2.5 Pro** | Slower than Flash variants |
| **Gemini 3 Flash** | 91% hallucination rate on refusals (rarely admits ignorance) |

### OpenAI GPT

| Model | Limitations |
|-------|-------------|
| **GPT-4.1** | 15s TTFT at 128K context, 1 min at 1M |
| **GPT-4o** | Smaller context (128K) vs newer models |
| **GPT-4o-mini** | Knowledge cutoff Oct 2023; less capable for complex reasoning |
| **GPT-5** | Context limited to 400K vs competitors' 1M |
| **GPT-5.2** | 40% more expensive than GPT-5.1 |

### Claude

| Model | Limitations |
|-------|-------------|
| **Claude 3 Sonnet** | Outdated (Aug 2023 knowledge); only 4K output |
| **Claude 3.5 Sonnet** | Limited output (8K) |
| **Claude 3.7 Sonnet** | Extended thinking not on free tier |
| **Claude 4 Sonnet** | Standard context (200K); no extended thinking |
| **Claude 4.5 Sonnet** | Long-context (>200K) costs 2x; 1M beta limited |
| **Claude 4.5 Opus** | 2-4s latency; not ideal for real-time; most expensive |

---

## Cost Optimization Features

| Provider | Feature | Savings | Notes |
|----------|---------|---------|-------|
| **Anthropic** | Prompt Caching | Up to 90% | 5-min or 1-hour cache |
| **Anthropic** | Batch Processing | Up to 50% | Non-time-sensitive |
| **OpenAI** | Prompt Caching | 50% | 5-10 minute persistence |
| **OpenAI** | Batch API | 50% | Async, 24-hour turnaround |
| **Google** | Context Caching | 50% | Reuse identical prompts |
| **Google** | Batch Inference | 20-45% | Async processing |

---

## Quick Decision Tree

```
START: What's your primary constraint?

[COST] → Is context <50K?
    YES → GPT-4o-mini ($0.15/$0.60)
    NO → Is context <200K?
        YES → Claude 4.5 Sonnet ($3/$15) + caching
        NO → GPT-5 ($1.25/$10)

[SPEED] → Need <1s latency?
    YES → Gemini 3 Flash (0.21s TTFT)
    NO → GPT-4o-mini or GPT-4.1

[QUALITY] → Is this complex reasoning?
    YES → Is coding involved?
        YES → Claude 4.5 Opus (80.9% SWE-bench)
        NO → GPT-5.2 (90%+ ARC-AGI)
    NO → Claude 4.5 Sonnet (balanced)

[CONTEXT] → Need >200K context?
    YES → Need >400K?
        YES → GPT-4.1 or Gemini 2.5 Pro (1M)
        NO → GPT-5 or GPT-5.2 (400K)
    NO → Any model works

[OUTPUT] → Need >16K output?
    YES → Claude 4.5 Sonnet/Opus (64K) or GPT-5/5.2 (128K)
    NO → Any model works
```

---

## Cost Calculator

**Formula**:
```
Cost per call = (input_tokens / 1,000,000 * input_price) + (output_tokens / 1,000,000 * output_price)
Cost per 1K calls = Cost per call * 1000
```

**Example**: 5K input, 2K output with GPT-4o-mini
```
Input cost:  5,000 / 1,000,000 * $0.15 = $0.00075
Output cost: 2,000 / 1,000,000 * $0.60 = $0.0012
Per call:    $0.00195
Per 1K:      $1.95
```

**Same with Claude 4.5 Sonnet**:
```
Input cost:  5,000 / 1,000,000 * $3.00 = $0.015
Output cost: 2,000 / 1,000,000 * $15.00 = $0.030
Per call:    $0.045
Per 1K:      $45.00
```

---

## Beam AI Model Identifiers

When setting `preferredModel` in Beam tools:

| Model | Beam Identifier |
|-------|-----------------|
| GPT-4o | `gpt-4o` |
| GPT-4o-mini | `gpt-4o-mini` |
| GPT-4.1 | `gpt-4.1` |
| GPT-5 | `gpt-5` |
| GPT-5.2 | `gpt-5.2` |
| Claude 3.5 Sonnet | `claude-3-5-sonnet` |
| Claude 4 Sonnet | `claude-4-sonnet` |
| Claude 4.5 Sonnet | `claude-4.5-sonnet` |
| Claude 4.5 Opus | `claude-4.5-opus` |
| Gemini 2.5 Pro | `gemini-2.5-pro` |
| Gemini 3 Pro | `gemini-3-pro` |
| Gemini 3 Flash | `gemini-3-flash` |

*Note: Verify exact identifiers in Beam documentation as they may update.*

---

## Sources

### Pricing & Specifications
- OpenAI API Pricing (platform.openai.com)
- Anthropic Claude Pricing (platform.claude.com)
- Google Vertex AI Pricing (cloud.google.com)
- LLM Stats (llm-stats.com)

### Benchmark & Accuracy Research
- Artificial Analysis - Gemini 3 Flash Analysis (artificialanalysis.ai)
- DocsBot - Model Comparisons (docsbot.ai)
- Engadget - Gemini 3 Flash vs GPT-5.2 (engadget.com)
- Medium/UnderDoc - Document Extraction Evaluation (medium.com)
- Cleanlab - Structured Output Benchmark (cleanlab.ai)
- All About AI - Hallucination Rates (allaboutai.com)

### Key Research Findings (Feb 2026)
- Gemini 3 Flash: 15% better extraction accuracy than Gemini 2.5 Flash
- Gemini 3 Flash competes with GPT-5.2 in benchmarks
- GPT-4o-mini: 17 months older, Oct 2023 training cutoff
- Gemini 3 Flash: 218 tok/s vs GPT-4o-mini: 85 tok/s
- GPT-4o-mini hallucination: ~1.69% (simple tasks), higher on extraction
