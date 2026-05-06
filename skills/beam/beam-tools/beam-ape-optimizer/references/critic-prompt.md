# Critic Agent Prompt Template

Use this prompt to run credit assignment on a failing node. Replace placeholders with actual values.

---

```
You are a prompt analysis specialist. You will receive:

1. A PROMPT (segmented into numbered instructions)
2. The model's REASONING trace (its chain-of-thought)
3. The model's OUTPUT
4. The GROUND TRUTH (correct answer)

Your task:

A. Identify whether the OUTPUT matches GROUND TRUTH
B. If MISMATCH: trace through the REASONING to find WHERE the model went wrong
C. For each numbered instruction in the PROMPT, assign one label:
   - KEEP: The model followed this instruction correctly
   - MODIFY: This instruction contributed to the error (explain why)
   - NEUTRAL: This instruction was not relevant to the error

Focus on the ROOT CAUSE — not just the final wrong answer, but which instruction
led the model down the wrong path. The reasoning trace shows the model's thinking
step by step. Find the earliest point where the reasoning diverged from correct
and trace that back to a specific instruction.

# PROMPT (numbered instructions)
{prompt_with_numbered_instructions}

# REASONING TRACE
{reasoning_output}

# MODEL OUTPUT
{model_output}

# GROUND TRUTH
{ground_truth}

# Your Analysis

Output as JSON:
{
  "match": true/false,
  "error_description": "...",
  "error_root_cause": "which reasoning step failed and why",
  "instruction_labels": [
    {"instruction": 1, "label": "KEEP", "reason": "Correctly identified language"},
    {"instruction": 2, "label": "MODIFY", "reason": "Rule too broad — matched keyword without checking context"},
    {"instruction": 3, "label": "NEUTRAL", "reason": "Not relevant to this classification error"}
  ]
}
```

## How to Segment Prompts into Instructions

Before feeding to the Critic, number each distinct instruction in the prompt:

1. Each rule or numbered step becomes one instruction
2. Each section header with guidance becomes one instruction
3. Definitions and examples stay grouped with their parent instruction
4. Keep the numbering sequential

Example:
```
Original: "Check if the email is from a service center. SC emails contain @sc- domains."
Numbered: "[1] Check if the email is from a service center. SC emails contain @sc- domains."
```

## Aggregating Across Multiple Failures

After running the Critic on all failing test cases for a node:

1. Count how many times each instruction got `MODIFY`
2. Instructions with MODIFY on 2+ different test cases are high-priority fixes
3. Instructions with MODIFY on only 1 test case may be edge cases — fix if clear, otherwise note for next iteration
4. Instructions that are always `KEEP` are working well — protect them during editing
