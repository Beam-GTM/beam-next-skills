# Batch Generation Patterns

Strategies for generating multiple related documents efficiently while maintaining consistency.

---

## Core Concepts

**Batch generation** = Creating multiple instances of similar data (50 resumes, 100 invoices, 20 customer profiles)

**Key challenges**:
1. **Variation**: Each instance must be unique but realistic
2. **Consistency**: Related data must reference same entities correctly
3. **Efficiency**: Generate quickly without sacrificing quality
4. **Relationships**: Maintain logical connections between documents

---

## Pattern 1: Independent Batch (No Cross-References)

**Use case**: Documents don't reference each other

**Examples**:
- 50 resumes for different candidates
- 100 product listings for catalog
- 30 bank statements for different accounts

**Strategy**:
1. Define variation parameters
2. Generate each instance independently
3. Ensure diversity without patterns being obvious

**Example - 50 Resumes**:
```python
# Variation parameters
experience_levels = ["0-3 years", "3-7 years", "7-15 years", "15+ years"]
industries = ["tech", "finance", "healthcare", "retail", "manufacturing"]
roles = ["IC", "senior IC", "manager", "director"]

# Generate distribution
for i in range(50):
    experience = random.choice(experience_levels)
    industry = random.choice(industries)
    role = random.choice(roles)

    generate_resume(
        name=generate_name(),
        experience=experience,
        industry=industry,
        role=role
    )
```

**Tips**:
- Use realistic distributions (more junior than executives)
- Vary document length (some 1 page, some 2 pages)
- Mix formatting styles (chronological vs. functional)

---

## Pattern 2: Master Entity with Multiple Documents

**Use case**: One central entity (person, company) with multiple related documents

**Examples**:
- Customer profile + 5 invoices + 3 support tickets
- Employee profile + performance reviews + training records
- Company profile + organizational docs + system docs

**Strategy**:
1. Generate master entity first (with all key attributes)
2. Create entity reference file
3. Generate related documents referencing master entity

**Example - Customer Journey**:
```markdown
# Step 1: Master Entity
customer_001:
  name: "Sarah Chen"
  email: "schen@email.com"
  address: "123 Oak Street, Chicago, IL 60614"
  customer_since: "2022-03-15"
  tier: "gold"

# Step 2: Generate Related Docs
- Invoice 1: Bill To: Sarah Chen, 123 Oak Street... (references customer_001)
- Invoice 2: Same customer reference
- Support Ticket 1: Customer: Sarah Chen (schen@email.com) re: Invoice 1
- Support Ticket 2: Customer: Sarah Chen (schen@email.com) re: Invoice 2
```

**Consistency checks**:
- Name spelled identically everywhere
- Email format consistent
- Address matches exactly
- Timeline is logical (invoices before support tickets about those invoices)

---

## Pattern 3: Network of Entities

**Use case**: Multiple entities with interconnected relationships

**Examples**:
- Organization (5 departments, 20 employees, 30 processes, 50 documents)
- Supply chain (10 suppliers, 50 products, 200 orders)
- Healthcare system (10 doctors, 100 patients, 500 appointments)

**Strategy**:
1. Define entity types and relationships
2. Generate master entity registry
3. Generate documents following relationship graph
4. Create cross-reference manifest

**Example - Organizational Knowledge**:
```markdown
# Entity Registry
departments:
  - id: dept_001
    name: "Risikomanagement"
    head: "Dr. Christoph Müller"
  - id: dept_002
    name: "IT-Systeme"
    head: "Lars Hofmann"

employees:
  - id: emp_001
    name: "Dr. Christoph Müller"
    department: dept_001
    role: "Abteilungsleiter"
  - id: emp_002
    name: "Lars Hofmann"
    department: dept_002
    role: "Abteilungsleiter"

documents:
  - id: doc_001
    type: "Arbeitsanweisung"
    name: "AA-KWP-001"
    owner: dept_001  # Risikomanagement
    references: [doc_002, sys_001]
  - id: doc_002
    type: "Richtlinie"
    name: "RL-RISK-002"
    owner: dept_001

systems:
  - id: sys_001
    name: "Scoring-Engine"
    owner: dept_002  # IT-Systeme
    used_by: [dept_001]  # Also used by Risikomanagement

# Cross-Reference Validation
- doc_001 mentions "See RL-RISK-002" → doc_002 must exist ✓
- doc_001 mentions "Scoring-Engine" → sys_001 must exist ✓
- sys_001 owner is IT but used by Risk → relationship valid ✓
```

**Relationship types**:
- **Ownership**: Document owned by department
- **Reference**: Document references another document
- **Usage**: System used by department
- **Reporting**: Employee reports to manager
- **Dependencies**: Process depends on another process

**Generation order**:
1. Core entities (departments, people)
2. Assets (systems, products)
3. Processes (workflows)
4. Documents (policies, procedures)
5. Transactions (invoices, tickets)

---

## Pattern 4: Time-Series Data

**Use case**: Sequential data over time

**Examples**:
- 12 months of bank statements
- Daily transaction logs for a year
- Quarterly performance reviews over 2 years
- Weekly inventory snapshots

**Strategy**:
1. Define time range and frequency
2. Generate seed values (opening balance, starting inventory)
3. Simulate realistic changes over time
4. Maintain running totals/states

**Example - Bank Statements**:
```markdown
# Month 1 (Jan 2024)
Opening Balance: $5,000.00
Transactions:
  - Jan 5: Salary Deposit +$4,200.00
  - Jan 10: Rent Payment -$1,800.00
  - Jan 15: Groceries -$250.00
  - Jan 20: Electric Bill -$120.00
Closing Balance: $7,030.00

# Month 2 (Feb 2024)
Opening Balance: $7,030.00  # Must match previous closing!
Transactions:
  - Feb 5: Salary Deposit +$4,200.00
  - Feb 10: Rent Payment -$1,800.00
  - Feb 12: Groceries -$280.00
  - Feb 18: Internet Bill -$80.00
Closing Balance: $9,070.00

# Month 3 (Mar 2024)
Opening Balance: $9,070.00  # Must match previous closing!
...
```

**Realism tips**:
- Recurring transactions (rent, subscriptions) same date each month
- Salary deposits on consistent schedule (1st and 15th)
- Seasonal variation (more spending in December)
- Occasional large purchases (not every month)

---

## Pattern 5: Synthetic Personas with Complete Histories

**Use case**: Realistic "person" with full document set

**Examples**:
- Job candidate: Resume + cover letter + references + portfolio + work samples
- Patient: Demographics + medical history + lab results + prescriptions + visit notes
- Employee: Profile + performance reviews + training records + timesheets

**Strategy**:
1. Define persona template (demographics, characteristics, history)
2. Generate persona profile with internal consistency
3. Generate all documents for that persona
4. Repeat for N personas

**Example - Job Candidate Persona**:
```markdown
# Persona: Alex Rivera

## Core Attributes
- Age: 32
- Education: BS Computer Science, MIT (2014)
- Experience: 8 years (2016-2024)
- Specialization: Full-stack development, AWS
- Current Location: San Francisco, CA

## Career Timeline
- 2016-2018: Junior Developer at StartupCo
- 2018-2021: Software Engineer at MegaCorp
- 2021-2024: Senior Engineer at TechUnicorn

## Documents to Generate
1. Resume: Reflects career timeline, MIT education, 8 years exp
2. Cover Letter: Mentions transition from MegaCorp to TechUnicorn, explains why seeking new role
3. Reference Letter 1: From manager at MegaCorp (2018-2021 timeframe)
4. Reference Letter 2: From manager at TechUnicorn (current)
5. Portfolio: Projects from each company (respecting NDA constraints)
6. Code Samples: Python/JS, AWS experience evident

## Consistency Checks
- All dates align with timeline
- Technologies mentioned match era (no Kubernetes in 2016 portfolio)
- References are from real managers at those companies (generate those personas too)
- No employment gaps unexplained
```

---

## Efficiency Techniques

### 1. Template-Based Generation

**Instead of writing each document from scratch**:
- Create parameterized templates
- Fill in variables per instance
- Vary structure slightly (but not every time)

**Example Template - Invoice**:
```markdown
Invoice #{invoice_number}
Date: {date}
Due: {due_date}

Bill To:
{customer_name}
{customer_address}

Items:
{for item in items}
  - {item.description}: ${item.amount}
{endfor}

Subtotal: ${subtotal}
Tax ({tax_rate}%): ${tax_amount}
Total: ${total}
```

Fill template for each invoice, varying invoice_number, customer, items, amounts.

### 2. Batch Parameters

**Define variations upfront**:
```python
batch_config = {
    "count": 50,
    "variation": {
        "names": "generate_random",
        "amounts": "range(100, 10000)",
        "dates": "spread_over_year(2024)"
    },
    "relationships": {
        "customer_to_invoices": "1_to_many",
        "invoice_to_tickets": "optional"
    }
}
```

### 3. Lazy Generation

**Don't generate everything upfront**:
- Generate high-level list first (50 customer IDs)
- Generate details on-demand (when that customer's docs are needed)
- Saves memory and time for large batches

---

## Validation for Batch Data

### Automated Checks

**Uniqueness**:
- [ ] No duplicate IDs (invoice numbers, customer IDs, SSNs)
- [ ] Names vary (not all "John Smith")
- [ ] Amounts vary realistically

**Consistency**:
- [ ] All references resolve (document mentions another document that exists)
- [ ] Dates are chronological (no time travel)
- [ ] Math is correct (invoice totals, bank balances)

**Realism**:
- [ ] Distributions look realistic (bell curve for salaries, not uniform)
- [ ] Outliers exist but are rare (some very high/low values)
- [ ] No obvious patterns (not all amounts ending in .00)

**Completeness**:
- [ ] All required fields populated (no "TBD" or "NULL")
- [ ] Relationships complete (every invoice has a customer)
- [ ] No broken references (document links to non-existent document)

---

## Output Organization

### Folder Structure for Batches

**Pattern 1: Flat Structure (Independent Documents)**
```
output/
├── resume_001.md
├── resume_002.md
├── resume_003.md
...
├── resume_050.md
```

**Pattern 2: Entity-Centric (Documents Grouped by Entity)**
```
output/
├── customer_001/
│   ├── profile.md
│   ├── invoice_001.md
│   ├── invoice_002.md
│   └── support_ticket_001.md
├── customer_002/
│   ├── profile.md
│   ├── invoice_003.md
│   └── invoice_004.md
```

**Pattern 3: Type-Centric (Documents Grouped by Type)**
```
output/
├── profiles/
│   ├── customer_001_profile.md
│   ├── customer_002_profile.md
├── invoices/
│   ├── invoice_001.md
│   ├── invoice_002.md
│   ├── invoice_003.md
└── support_tickets/
    ├── ticket_001.md
```

**Pattern 4: Hierarchical (Complex Relationships)**
```
output/
├── README.md (manifest)
├── entities/
│   ├── customers.json
│   ├── products.json
│   └── employees.json
├── documents/
│   ├── invoices/
│   ├── policies/
│   └── procedures/
└── metadata/
    ├── cross-references.yaml
    └── statistics.md
```

Choose based on how the data will be used.

---

## Batch Generation Checklist

Before starting batch generation:

- [ ] Define entity types and relationships
- [ ] Create entity registry/master list
- [ ] Set variation parameters (ranges, distributions)
- [ ] Determine generation order (dependencies first)
- [ ] Define consistency rules (what must match across docs)
- [ ] Set realism targets (high/medium/low)
- [ ] Choose output structure (flat/entity-centric/type-centric)
- [ ] Plan validation checks (uniqueness, consistency, math)

During generation:

- [ ] Track generated entities in registry
- [ ] Validate each document before moving to next
- [ ] Check cross-references as you go
- [ ] Log any inconsistencies for manual review

After generation:

- [ ] Run automated validation suite
- [ ] Spot-check random samples (10% of batch)
- [ ] Generate summary statistics (counts, distributions)
- [ ] Create manifest file (what was generated, relationships)
- [ ] Package for delivery (zip/archive if needed)

---

## Common Pitfalls

**Pitfall 1: Inconsistent entity references**
- Problem: Invoice references "Sarah Chen", support ticket references "Sarah Chen-Smith"
- Solution: Generate all names ONCE, store in registry, reference registry

**Pitfall 2: Unrealistic uniformity**
- Problem: All invoices for exactly $100.00
- Solution: Use realistic distributions (mean $500, std dev $200)

**Pitfall 3: Timeline violations**
- Problem: Support ticket about invoice dated before invoice was created
- Solution: Generate timeline first, assign dates respecting order

**Pitfall 4: Broken cross-references**
- Problem: Document mentions "See AA-FOMA-001" but that document doesn't exist
- Solution: Validate all references against entity registry before finalizing

**Pitfall 5: Obvious patterns**
- Problem: Customer IDs are cust_001, cust_002, ... cust_999 (too obvious)
- Solution: Use randomized IDs or realistic formats (BMW-C-2024-001234)

---

## Performance Optimization

**For large batches (100+ documents)**:

1. **Parallelize where possible**
   - Independent documents can be generated concurrently
   - Use multiprocessing for CPU-bound generation

2. **Use templates aggressively**
   - Pre-compile templates once
   - Fill templates rapidly for each instance

3. **Batch I/O operations**
   - Don't write files one-by-one
   - Buffer writes, flush at end

4. **Profile and optimize**
   - Identify slow steps (usually LLM calls or file I/O)
   - Cache repeated operations (e.g., date parsing)

**Example**: Generating 100 invoices
- Without optimization: ~10 minutes (6 seconds per invoice)
- With templates: ~2 minutes (1.2 seconds per invoice)
- With parallelization: ~30 seconds (4 workers, 0.3 seconds per invoice)

---

This guide enables efficient, consistent batch generation while maintaining realism and relationships.
