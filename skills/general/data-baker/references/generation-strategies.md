# Generation Strategies by Data Type

This reference provides patterns for generating different types of synthetic datasets.

---

## 1. Organizational/Institutional Knowledge

**Use case**: Agent needs understanding of an organization's structure, processes, policies, systems

**What to generate**:
- Company/organization profile
- Organizational structure (departments, roles, responsibilities)
- Work instructions/procedures (step-by-step processes)
- Policies/guidelines (high-level frameworks)
- System documentation (IT systems, tools, integrations)
- Process maps (visual workflows with control points)
- Metadata files (department mappings, product catalogs, responsibility matrices)

**Key characteristics**:
- Cross-referenced documents (policies reference procedures, procedures reference systems)
- Hierarchical structure (policies → guidelines → work instructions)
- Domain-specific terminology (banking: MaRisk, BAIT; healthcare: HIPAA, clinical protocols)
- Realistic regulatory mappings
- 30-60 pages typical for MVP, 100+ for comprehensive

**Template structure**:
```
organization-name/
├── 01-company-profile/
├── 02-organizational-structure/
├── 03-work-instructions/
├── 04-policies-guidelines/
├── 05-system-documentation/
├── 06-process-maps/
└── 07-metadata/
```

**Critical for RAG**:
- Document metadata in YAML frontmatter
- Section headers for chunking
- Cross-reference links between documents
- Keywords for searchability

---

## 2. Identity Documents

**Use case**: Agent needs to process/validate/extract from identity documents

**What to generate**:
- Passports
- Driver's licenses
- National ID cards
- Social security cards
- Birth certificates
- Work permits/visas

**Key characteristics**:
- Realistic formats (specific to country/region)
- Proper ID number formats (checksums if applicable)
- Consistent person data across multiple IDs
- Realistic photos/signatures (describe, don't generate actual images)
- Security features descriptions (holograms, watermarks)
- Expiry dates, issue dates (logical consistency)

**Format considerations**:
- **Text representation**: Markdown tables with field descriptions
- **Structured data**: JSON with all ID fields
- **Visual description**: "Photo shows [description], hologram in top-right corner"

**Batch generation**:
- Generate consistent person across multiple ID types
- Vary demographics (age, gender, ethnicity)
- Mix of valid/expired documents if testing validation

---

## 3. Professional Documents

**Use case**: Agent processes resumes, evaluates candidates, generates job materials

**What to generate**:
- Resumes/CVs
- Cover letters
- Job descriptions
- Performance reviews
- Reference letters
- Professional portfolios

**Key characteristics**:
- Realistic career progression (junior → senior roles)
- Domain-appropriate skills (tech: Python, AWS; marketing: SEO, analytics)
- Plausible dates (no overlapping employment)
- Consistent formatting (ATS-friendly for resumes)
- Appropriate tone (professional, concise)

**Variation parameters**:
- Experience level (0-3 years, 3-7 years, 7-15 years, 15+ years)
- Industry (tech, finance, healthcare, retail, manufacturing)
- Role type (IC, manager, director, executive)
- Education level (high school, bachelor's, master's, PhD)

---

## 4. Financial Documents

**Use case**: Agent processes invoices, statements, receipts for accounting/expense tracking

**What to generate**:
- Bank statements
- Invoices
- Receipts
- Tax forms (W-2, 1099, etc.)
- Credit card statements
- Purchase orders
- Payment confirmations

**Key characteristics**:
- Realistic amounts (not random - context-appropriate)
- Proper formatting (currency, decimals, dates)
- Transaction consistency (debits + credits = balance)
- Tax calculations (if applicable)
- Merchant/vendor details (real-sounding business names)

**Critical for accuracy**:
- Running balances on statements
- Invoice totals match line items
- Tax rates match jurisdiction
- Date sequences (statement periods, due dates)

---

## 5. Medical Records

**Use case**: Agent processes patient data, clinical documentation, prescriptions

**What to generate**:
- Patient records (demographics, history)
- Clinical notes (SOAP format)
- Lab results (bloodwork, imaging)
- Prescriptions (medications, dosages)
- Discharge summaries
- Insurance claims (medical coding)

**Key characteristics**:
- HIPAA-aware (synthetic but realistic PHI)
- Medical terminology (ICD-10 codes, medication names)
- Logical clinical progression (symptoms → diagnosis → treatment)
- Proper units (mg, ml, mmHg, etc.)
- Realistic vitals (BP 120/80, not 200/50)

**Safety note**:
- Always mark as "SYNTHETIC DATA - NOT REAL PATIENT"
- Do NOT use for actual medical training without review

---

## 6. Legal Documents

**Use case**: Agent reviews contracts, generates agreements, checks compliance

**What to generate**:
- Contracts (employment, vendor, service)
- NDAs (mutual, one-way)
- Terms of Service / Privacy Policies
- Settlement agreements
- Lease agreements
- Power of attorney documents

**Key characteristics**:
- Proper legal structure (recitals, definitions, clauses, signatures)
- Jurisdiction-specific language (US vs. UK vs. EU)
- Realistic clauses (not nonsensical legalese)
- Cross-references between sections
- Proper formatting (numbered paragraphs, defined terms in CAPS)

**Variation parameters**:
- Complexity (simple 2-page NDA vs. 50-page M&A agreement)
- Jurisdiction (state law references, governing law clauses)
- Party types (individual, corporation, LLC, partnership)

---

## 7. Product Catalogs & Inventory

**Use case**: Agent manages inventory, processes orders, recommends products

**What to generate**:
- Product listings (SKU, name, description, price)
- Inventory records (stock levels, locations)
- Supplier information
- Product specifications (dimensions, materials, features)
- Pricing tiers (MSRP, wholesale, bulk discounts)

**Key characteristics**:
- Hierarchical categories (Electronics → Laptops → Gaming Laptops)
- Realistic pricing (not $1.00 for everything)
- SKU format consistency (ABC-1234-XL-BLU)
- Stock quantities (not all in stock or all out of stock)
- Product relationships (bundles, alternatives, accessories)

---

## 8. Customer/User Data

**Use case**: Agent handles customer support, CRM, user management

**What to generate**:
- Customer profiles (demographics, preferences)
- Transaction histories (purchases, returns)
- Support tickets (issues, resolutions)
- Communication logs (emails, chats, calls)
- Loyalty program data (points, tier status)

**Key characteristics**:
- Realistic customer journeys (first purchase → repeat → loyalty)
- Varied ticket types (technical, billing, shipping)
- Appropriate response times (SLA compliance)
- Sentiment variation (happy, frustrated, neutral)
- GDPR/privacy considerations (consent flags)

---

## 9. Email & Communication

**Use case**: Agent drafts emails, analyzes sentiment, automates responses

**What to generate**:
- Business emails (formal, professional tone)
- Support emails (empathetic, solution-focused)
- Marketing emails (persuasive, clear CTA)
- Internal memos (concise, action-oriented)
- Email threads (multi-party conversations)

**Key characteristics**:
- Realistic subject lines
- Appropriate signatures (name, title, contact)
- Proper threading (Re:, Fwd:)
- Time zones on timestamps
- Attachments mentioned in body text

---

## Strategy Selection Logic

**For Claude to determine which strategy:**

1. **Scan input context for keywords**:
   - "company", "organization", "regulatory", "compliance" → Organizational
   - "ID", "passport", "license", "identity" → Identity Documents
   - "resume", "CV", "job", "candidate" → Professional Documents
   - "invoice", "receipt", "statement", "tax" → Financial Documents
   - "patient", "medical", "clinical", "prescription" → Medical Records
   - "contract", "agreement", "NDA", "legal" → Legal Documents
   - "product", "inventory", "SKU", "catalog" → Product Catalogs
   - "customer", "user", "profile", "support ticket" → Customer Data
   - "email", "message", "communication" → Email/Communication

2. **Check for quantity indicators**:
   - "50 resumes" → Batch generation
   - "single company profile" → Single instance
   - "dataset of 100 invoices" → Batch generation

3. **Identify realism requirements**:
   - "realistic", "production-ready", "demo" → High realism
   - "test", "dummy", "placeholder" → Moderate realism

4. **Determine output format**:
   - "for RAG", "knowledge base", "vector DB" → Markdown with metadata
   - "structured data", "JSON", "CSV" → Structured formats
   - "visual", "PDF-like" → Descriptive format (text representation)

---

## Cross-Strategy Considerations

**When combining multiple strategies** (e.g., customer profile + invoices + support tickets):
- Ensure consistency (same customer name across all documents)
- Maintain logical relationships (invoice dates before support ticket dates)
- Generate a "master entity list" to track references
- Use shared metadata file for cross-document consistency

**Example**: Generating "customer journey dataset"
1. Generate customer profile (strategy 8)
2. Generate purchase invoices (strategy 4) referencing customer
3. Generate support tickets (strategy 8) referencing invoices
4. Generate follow-up emails (strategy 9) referencing tickets
5. Create cross-reference manifest tracking all relationships
