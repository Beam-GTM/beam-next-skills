---
name: data-baker
version: '1.0'
description: 'Generate realistic synthetic datasets for AI agent training and testing
  across diverse domains. Use when user provides meeting transcripts, requirements
  documents, process flows, or requests synthetic data generation for identity documents,
  resumes, financial records, medical records, legal contracts, product catalogs,
  customer profiles, organizational knowledge, or email communications. Generates
  10-100+ pages of realistic, cross-referenced, domain-appropriate synthetic data
  with proper formatting, metadata, and RAG-friendly structure. Keywords: synthetic
  data, dataset generation, dummy data, test data, mock documents, institutional knowledge,
  training data, sample documents, realistic data, batch generation, identity cards,
  resumes, invoices, bank statements, medical records, contracts, organizational documentation.'
author: Safi Haider
category: general
tags:
- email
- meeting
- transcript
updated: '2026-01-05'
visibility: public
---
# Data Baker

Generate realistic synthetic datasets for AI agent training, testing, and RAG knowledge bases from meeting transcripts, requirements docs, or process flows.

## Purpose

Data Baker transforms input context (meeting transcripts, requirements documents, process flows) into comprehensive, realistic synthetic datasets suitable for AI agent training, testing, and RAG (Retrieval Augmented Generation) systems. It generates 10-100+ pages of domain-appropriate, cross-referenced documents with proper metadata, realistic formatting, and logical consistency.

**Key Features**:
- **9 Data Generation Strategies**: Organizational knowledge, identity documents, professional documents, financial records, medical records, legal contracts, product catalogs, customer data, email communications
- **Batch Generation**: Create 10-500+ related documents with maintained cross-references and entity consistency
- **Realism-First**: Domain-appropriate terminology, realistic formatting, proper calculations, cultural awareness
- **RAG-Optimized**: YAML frontmatter, section headers for chunking, cross-reference links, searchable keywords
- **Flexible Input**: Process flows, meeting transcripts, requirements docs, or simple text descriptions

**Time Estimate**: 15-45 minutes depending on dataset size and complexity

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Analyze input context and determine data type
- [ ] Load appropriate reference guides
- [ ] Define dataset scope and structure
- [ ] Generate master entity registry (if applicable)
- [ ] Generate documents with cross-references
- [ ] Validate consistency and realism
- [ ] Package output with README
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: Analyze Input Context

**Goal**: Understand what type of synthetic data is needed

**Actions**:
1. Read user's input (meeting transcript, requirements doc, process flow, or request)
2. Identify key indicators:
   - **Domain**: Banking, healthcare, legal, tech, manufacturing, etc.
   - **Data Type**: Organizational knowledge, identity docs, financial records, etc.
   - **Quantity**: Single entity vs. batch (10-100+ documents)
   - **Realism Level**: High (demo/production) vs. moderate (testing)
   - **Relationships**: Independent documents vs. interconnected network
3. Determine which generation strategy to use (see references/generation-strategies.md)

**Decision Logic**:
- Keywords like "company", "organization", "regulatory", "compliance" → Organizational Knowledge
- Keywords like "ID", "passport", "license" → Identity Documents
- Keywords like "resume", "CV", "candidate" → Professional Documents
- Keywords like "invoice", "statement", "receipt" → Financial Documents
- Keywords like "patient", "medical", "clinical" → Medical Records
- Keywords like "contract", "agreement", "NDA" → Legal Documents
- Keywords like "product", "inventory", "SKU" → Product Catalogs
- Keywords like "customer", "profile", "support ticket" → Customer Data
- Keywords like "email", "message", "communication" → Email/Communication

**Mark this todo complete before proceeding.**

---

### Step 3: Load Appropriate Reference Guides

**Goal**: Load relevant reference files into context

**Actions**:
1. **Always load**: [references/realism-guidelines.md](references/realism-guidelines.md)
   - Core principles for realistic data
   - Names, dates, addresses, financial data, terminology
   - Cross-document consistency rules

2. **Load if batch generation**: [references/batch-generation.md](references/batch-generation.md)
   - Patterns for generating 10-500+ related documents
   - Master entity registry techniques
   - Relationship management strategies

3. **Load for strategy selection**: [references/generation-strategies.md](references/generation-strategies.md)
   - 9 generation strategies with examples
   - Cross-strategy considerations
   - Output organization patterns

**Mark this todo complete before proceeding.**

---

### Step 4: Define Dataset Scope and Structure

**Goal**: Plan exactly what will be generated

**Actions**:
1. **Define entities**:
   - Main entities (people, companies, products, departments)
   - Quantity (1 person vs. 50 customers)
   - Demographics/characteristics (age ranges, industries, roles)

2. **Define documents**:
   - Document types (invoices, resumes, policies, etc.)
   - Quantity per entity (1 resume per person, 5 invoices per customer)
   - Relationships (which documents reference which entities)

3. **Define variation parameters**:
   - Ranges (salaries $50K-$200K, dates across 2024)
   - Distributions (more junior than senior, bell curve for amounts)
   - Patterns (recurring transactions on same date)

4. **Choose output structure**:
   - Flat (independent documents)
   - Entity-centric (grouped by person/company)
   - Type-centric (grouped by document type)
   - Hierarchical (complex relationships with metadata)

**Example Plan**:
```markdown
## Dataset: Customer Journey for E-commerce Platform

### Entities:
- 10 customers (varied demographics, ages 25-65)
- 5 products (price range $50-$500)

### Documents:
- 10 customer profiles (1 per customer)
- 30 invoices (3 per customer on average, range 1-5)
- 15 support tickets (not all customers have tickets)
- 20 emails (mix of marketing, support, transactional)

### Relationships:
- Invoices reference customers and products
- Support tickets reference invoices
- Emails reference customers and may reference tickets

### Output Structure: Entity-centric
customer_001/
  profile.md
  invoice_001.md
  invoice_002.md
  support_ticket_001.md
  emails/
```

**Mark this todo complete before proceeding.**

---

### Step 5: Generate Master Entity Registry

**Goal**: Create consistent reference for all entities (if batch generation or network of entities)

**Actions**:
1. **Generate core entities first**:
   - People (names, demographics, IDs, addresses, emails)
   - Companies (names, addresses, industries)
   - Products (SKUs, names, prices, descriptions)
   - Departments (names, heads, responsibilities)

2. **Create registry file** (YAML or JSON):
   ```yaml
   customers:
     - id: cust_001
       name: "Sarah Chen"
       email: "schen@email.com"
       address: "123 Oak Street, Chicago, IL 60614"
       customer_since: "2022-03-15"
       tier: "gold"
     - id: cust_002
       name: "Michael Rodriguez"
       email: "mrodriguez@example.com"
       ...

   products:
     - id: prod_001
       sku: "LAPTOP-001-XL"
       name: "ProBook 15 Laptop"
       price: 1299.99
       category: "Electronics"
   ```

3. **Validate uniqueness**:
   - No duplicate IDs
   - No duplicate names (unless intentional)
   - All required fields populated

**Mark this todo complete before proceeding.**

---

### Step 6: Generate Documents with Cross-References

**Goal**: Generate all documents with proper relationships

**Actions**:
1. **Follow generation order** (for dependent documents):
   - Core entities (departments, people)
   - Assets (systems, products)
   - Processes (workflows)
   - Documents (policies, procedures)
   - Transactions (invoices, tickets)

2. **For each document**:
   - Include YAML frontmatter with metadata
   - Use section headers for RAG chunking
   - Reference master entity registry for consistency
   - Include cross-reference links to related documents
   - Apply realism guidelines (proper formatting, domain terminology)

3. **Maintain running state** (for time-series data):
   - Bank statements: closing balance becomes next opening balance
   - Inventory: stock levels change with transactions
   - Employee records: promotions update titles and dates

4. **Validate as you go**:
   - Math is correct (invoice totals, balances)
   - Dates are chronological (no time travel)
   - References resolve (mentioned documents exist)

**Example Document with Proper Structure**:
```markdown
---
document_id: INV-2024-001234
document_type: Invoice
date: 2024-11-15
customer_id: cust_001
customer_name: Sarah Chen
amount: 1234.56
status: paid
---

# Invoice #INV-2024-001234

**Date**: November 15, 2024
**Due Date**: December 15, 2024

## Bill To

Sarah Chen
123 Oak Street
Chicago, IL 60614
schen@email.com

## Items

| Description | Quantity | Unit Price | Total |
|-------------|----------|------------|-------|
| ProBook 15 Laptop (SKU: LAPTOP-001-XL) | 1 | $1,299.99 | $1,299.99 |

**Subtotal**: $1,299.99
**Tax (8.75%)**: $113.75
**Total**: $1,413.74

## Payment Information

**Status**: PAID
**Payment Date**: November 18, 2024
**Payment Method**: Credit Card (****1234)

---

*For support inquiries, see Support Ticket #TICKET-001*
```

**Mark this todo complete before proceeding.**

---

### Step 7: Validate Consistency and Realism

**Goal**: Ensure dataset is believable and error-free

**Actions**:
1. **Run automated checks**:
   - [ ] All entity IDs are unique
   - [ ] All cross-references resolve (no broken links)
   - [ ] All math is correct (totals, balances)
   - [ ] All dates are chronological
   - [ ] No placeholder text ("TODO", "XXX", "TBD")
   - [ ] No obvious fake markers ("John Doe", "000-00-0000")

2. **Check realism**:
   - [ ] Names vary and are culturally appropriate
   - [ ] Amounts follow realistic distributions (not all $100.00)
   - [ ] Terminology is domain-appropriate
   - [ ] Formatting is professional and consistent
   - [ ] No impossible scenarios (born 2010, hired 2005)

3. **Spot-check samples**:
   - Read 10% of generated documents
   - Verify they "feel real"
   - Check for consistency across related documents

4. **Fix any issues** before finalizing

**Mark this todo complete before proceeding.**

---

### Step 8: Package Output with README

**Goal**: Deliver organized, documented dataset

**Actions**:
1. **Create README.md**:
   - Overview of dataset
   - Statistics (page count, document count, entity count)
   - Directory structure explanation
   - Usage instructions (how to load into RAG system)
   - Key entities and relationships

2. **Create QUICK-START.md** (optional):
   - Step-by-step guide for immediate use
   - Test cases with expected outputs
   - Integration examples (vector DB loading, chunking strategies)

3. **Create manifest file** (optional):
   - List of all generated files
   - Entity registry with cross-reference map
   - Statistics (distributions, counts)

4. **Organize output**:
   ```
   output/
   ├── README.md
   ├── QUICK-START.md
   ├── manifest.yaml
   ├── entities/
   │   ├── customers.yaml
   │   └── products.yaml
   ├── documents/
   │   ├── customer_001/
   │   ├── customer_002/
   │   └── ...
   └── metadata/
       └── cross-references.yaml
   ```

**Mark this todo complete before proceeding.**

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

## Resources

### references/

**references/generation-strategies.md** - 9 data generation strategies:
1. Organizational/Institutional Knowledge (policies, procedures, org structure)
2. Identity Documents (passports, licenses, IDs)
3. Professional Documents (resumes, cover letters, performance reviews)
4. Financial Documents (invoices, statements, receipts, tax forms)
5. Medical Records (patient records, clinical notes, lab results, prescriptions)
6. Legal Documents (contracts, NDAs, agreements, leases)
7. Product Catalogs & Inventory (SKUs, specifications, pricing)
8. Customer/User Data (profiles, transaction histories, support tickets)
9. Email & Communication (business emails, support emails, threads)

**references/realism-guidelines.md** - Guidelines for realistic data:
- Names (regional/cultural appropriateness, professional titles)
- Dates (logical sequences, realistic durations, proper formats)
- Addresses (country-specific formatting, real cities, proper postal codes)
- Numbers & Identifiers (realistic formats, checksums, no obvious fakes)
- Financial Data (realistic amounts, proper currency formatting, correct math)
- Professional Terminology (domain-specific language, consistent usage)
- Document Formatting (professional structure, appropriate tone, proper headers)
- Cross-Document Consistency (master entity lists, timeline consistency)

**references/batch-generation.md** - Strategies for generating 10-500+ documents:
- Pattern 1: Independent Batch (no cross-references)
- Pattern 2: Master Entity with Multiple Documents (1-to-many)
- Pattern 3: Network of Entities (complex relationships)
- Pattern 4: Time-Series Data (sequential over time)
- Pattern 5: Synthetic Personas with Complete Histories (realistic "person")

### scripts/

No scripts currently included. This skill relies on Claude's generation capabilities guided by the reference documentation.

### assets/

No assets currently included. Generated documents are created from scratch based on input context and reference guidelines.

---

## Notes

**About Input Context:**
- **Meeting Transcripts**: Extract requirements, entities, processes, terminology from conversation
- **Requirements Documents**: Parse specifications, constraints, entities, relationships
- **Process Flows**: Convert steps into procedural documents with proper structure
- **Simple Descriptions**: Accept brief requests like "50 resumes for tech candidates" or "customer journey dataset"

**About Realism Levels:**
- **High Realism** (demos, production testing, ML training, client deliverables): Apply all realism guidelines rigorously, validate extensively
- **Moderate Realism** (internal testing, PoCs, prototypes, educational examples): Focus on core realism (no "John Doe"), less precision on edge cases

**About RAG Optimization:**
- Always include YAML frontmatter for metadata extraction
- Use clear section headers (## Payment Terms, not ## Section 4)
- Include cross-reference links explicitly ("See also: AA-KWP-001 Section 4.2")
- Add keywords naturally in text for searchability
- Structure documents for logical chunking (1-2 page sections)

**About Cultural Awareness:**
- Match language to region (German docs IN GERMAN, Spanish invoices use "Factura")
- Use appropriate date formats (US: MM/DD/YYYY, Europe: DD.MM.YYYY)
- Apply correct currency symbols and formats (US: $1,234.56, Europe: 1.234,56 €)
- Respect business practices (German works councils, French 35-hour week)

**Common Pitfalls to Avoid:**
- ❌ Inconsistent entity references across documents
- ❌ Unrealistic uniformity (all amounts exactly $100.00)
- ❌ Timeline violations (support ticket dated before invoice)
- ❌ Broken cross-references (mentioning non-existent documents)
- ❌ Obvious patterns (customer_001, customer_002, ... too sequential)
- ❌ Math errors (invoice totals don't match line items)
- ❌ Placeholder text remaining ("TODO", "XXX", "sample")
