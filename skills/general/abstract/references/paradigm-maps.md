# Paradigm Maps

Reference hierarchies for common domains. Use these to quickly identify where a concept fits.

---

## AI Agents

```
AI AGENTS
│
├── Agent Architecture
│   ├── Agentic loops (ReAct, Plan-Execute, Reflexion)
│   ├── Tool use (function calling, MCP)
│   ├── Multi-agent systems (orchestration, delegation)
│   └── Human-in-the-loop patterns
│
├── Memory & Context
│   ├── Short-term (conversation history, sliding window)
│   ├── Long-term (RAG, vector stores, knowledge bases)
│   ├── Episodic (past interactions, learning from experience)
│   └── Working memory (active context management)
│
├── Evaluation & Quality
│   ├── Offline evals (test suites, benchmarks)
│   ├── Online evals (production monitoring, A/B tests)
│   ├── Human evaluation (labeling, feedback loops)
│   └── Metrics (accuracy, latency, cost, user satisfaction)
│
├── Observability & Debugging
│   ├── Tracing (Langfuse, LangSmith, Arize)
│   ├── Logging (structured logs, log levels)
│   ├── Metrics (token usage, latency percentiles)
│   └── Alerting (failure detection, anomaly detection)
│
└── Deployment & Operations
    ├── Hosting (serverless, containers, edge)
    ├── Scaling (rate limits, queuing, load balancing)
    ├── Versioning (prompt versioning, model versioning)
    └── Cost management (token optimization, caching)
```

---

## APIs & Integrations

```
API INTEGRATION
│
├── API Styles
│   ├── REST (resources, HTTP verbs, stateless)
│   ├── GraphQL (queries, mutations, subscriptions)
│   ├── RPC (gRPC, JSON-RPC, procedure calls)
│   └── WebSockets (bidirectional, real-time)
│
├── Authentication
│   ├── API Keys (simple, header-based)
│   ├── OAuth 2.0 (authorization code, client credentials)
│   ├── JWT (tokens, claims, expiration)
│   └── mTLS (certificates, mutual auth)
│
├── Data Flow Patterns
│   ├── Request-Response (synchronous, blocking)
│   ├── Webhooks (push-based, event-driven)
│   ├── Polling (pull-based, interval checks)
│   └── Streaming (SSE, chunked responses)
│
├── Error Handling
│   ├── HTTP status codes (4xx client, 5xx server)
│   ├── Retry strategies (exponential backoff, jitter)
│   ├── Circuit breakers (fail fast, recovery)
│   └── Idempotency (safe retries, deduplication)
│
└── Rate Limiting & Quotas
    ├── Token bucket (burst capacity)
    ├── Sliding window (request counting)
    ├── Quota management (daily/monthly limits)
    └── Backpressure (queue depth, throttling)
```

---

## Debugging & Observability

```
OBSERVABILITY
│
├── Three Pillars
│   ├── Logs (events, structured data, searchable)
│   ├── Metrics (counters, gauges, histograms)
│   └── Traces (distributed, spans, context propagation)
│
├── Debugging Workflow
│   ├── Reproduce (isolate, minimal case)
│   ├── Instrument (add observability)
│   ├── Hypothesize (root cause theories)
│   ├── Verify (test hypotheses)
│   └── Fix & Prevent (patch + systemic fix)
│
├── Agent-Specific Debugging
│   ├── Trace analysis (Langfuse, step-by-step)
│   ├── Prompt debugging (input/output inspection)
│   ├── Tool call inspection (parameters, responses)
│   └── Memory inspection (context, retrieval quality)
│
└── Root Cause Patterns
    ├── Input issues (bad data, edge cases)
    ├── Logic issues (wrong prompt, bad flow)
    ├── Integration issues (API failures, timeouts)
    └── Resource issues (rate limits, memory, cost)
```

---

## Distributed Systems

```
DISTRIBUTED SYSTEMS
│
├── Consistency Models
│   ├── Strong consistency (linearizable)
│   ├── Eventual consistency (convergence)
│   ├── Causal consistency (happens-before)
│   └── Read-your-writes (session guarantees)
│
├── Communication Patterns
│   ├── Synchronous (request-response, blocking)
│   ├── Asynchronous (queues, events, non-blocking)
│   ├── Pub/Sub (topics, subscribers, fan-out)
│   └── Event sourcing (append-only, replay)
│
├── Failure Handling
│   ├── Timeouts (connection, read, write)
│   ├── Retries (idempotent, exponential backoff)
│   ├── Fallbacks (degraded mode, defaults)
│   └── Bulkheads (isolation, blast radius)
│
└── Scaling Strategies
    ├── Horizontal (more instances, sharding)
    ├── Vertical (bigger machines)
    ├── Caching (CDN, in-memory, distributed)
    └── Load balancing (round-robin, least connections)
```

---

## Data & Pipelines

```
DATA SYSTEMS
│
├── Processing Models
│   ├── Batch (scheduled, high throughput)
│   ├── Streaming (real-time, continuous)
│   ├── Micro-batch (small batches, near real-time)
│   └── Lambda architecture (batch + stream)
│
├── Storage Patterns
│   ├── Relational (SQL, ACID, joins)
│   ├── Document (JSON, flexible schema)
│   ├── Key-Value (fast lookups, caching)
│   ├── Vector (embeddings, similarity search)
│   └── Graph (relationships, traversal)
│
├── ETL/ELT
│   ├── Extract (sources, connectors, APIs)
│   ├── Transform (clean, enrich, aggregate)
│   └── Load (destinations, warehouses, lakes)
│
└── Quality & Governance
    ├── Schema validation (contracts, evolution)
    ├── Data quality (completeness, accuracy)
    ├── Lineage (source tracking, impact analysis)
    └── Access control (RBAC, encryption)
```

---

## Startup / Business

```
STARTUP BUILDING
│
├── Product
│   ├── Problem-Solution Fit (does it solve pain?)
│   ├── Product-Market Fit (do people want it?)
│   ├── MVP (minimum viable, learn fast)
│   └── Iteration (feedback loops, pivots)
│
├── Go-to-Market
│   ├── Positioning (who, what, why different)
│   ├── Channels (direct, PLG, partnerships)
│   ├── Pricing (value-based, competitive)
│   └── Sales motion (self-serve, enterprise, hybrid)
│
├── Metrics
│   ├── Acquisition (CAC, channels, conversion)
│   ├── Activation (time-to-value, aha moment)
│   ├── Retention (churn, NRR, engagement)
│   ├── Revenue (ARR, MRR, expansion)
│   └── Referral (NPS, viral coefficient)
│
└── Operations
    ├── Hiring (roles, culture, comp)
    ├── Fundraising (stages, pitch, terms)
    ├── Legal (incorporation, IP, contracts)
    └── Finance (burn rate, runway, unit economics)
```

---

## When Paradigm is Unclear

If a concept doesn't fit neatly into above maps:

1. **Identify the field** - What discipline does this belong to?
2. **Find the core question** - What problem does this paradigm solve?
3. **Build hierarchy** - What are the 3-5 top-level categories?
4. **Locate concept** - Which category does the user's concept fall under?
5. **Show adjacencies** - What's related at the same level?

The goal is always: **Help user see where they are on the map.**
