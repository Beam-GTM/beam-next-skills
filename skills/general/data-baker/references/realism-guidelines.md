# Realism Guidelines for Synthetic Data

Guidelines for generating realistic, plausible synthetic data across domains.

---

## Core Principles

1. **Plausibility over perfection** - Data should be believable, not flawless
2. **Consistency is critical** - Same entity referenced multiple times must match exactly
3. **Domain-appropriate** - Banking data looks like banking data, not generic text
4. **Variation with patterns** - Not all identical, but following realistic distributions
5. **Cultural awareness** - Names, addresses, dates match the region/culture

---

## Names (People)

### Realistic Name Generation

**By region/culture**:
- **US**: Mix of common (Smith, Johnson) and less common surnames; first names from SSA popular names list
- **German**: Müller, Schmidt, Schneider; first names like Andreas, Thomas, Sabine, Claudia
- **UK**: Traditional (Williams, Brown) + multicultural (Patel, Ahmed)
- **Chinese**: Family name first (Li, Wang, Zhang) + given name
- **Spanish**: Double surnames (García López, Martínez Rodríguez)

**Avoid**:
- ❌ "John Doe", "Jane Smith" (too generic, signals placeholder)
- ❌ "Test User", "Sample Name" (breaks immersion)
- ❌ Fantasy names in professional contexts ("Gandalf Thunderfist" for a bank manager)

**Professional contexts**:
- Include titles: Dr. Elisabeth Hartmann, Prof. Andreas Weber (if applicable)
- Gender-appropriate names for the culture
- Age-appropriate names (older people have older-generation names)

**Consistency**:
- Same person across multiple documents must have EXACT same spelling
- Track generated names in master list to avoid duplicates
- Consider nicknames (William → Bill, Elisabeth → Lisa) but be consistent

---

## Dates

### Realistic Date Logic

**General rules**:
- Events in logical sequence (employment start before end, birth before school)
- No dates in the future (unless explicitly a forecast/projection)
- Appropriate time gaps (not hired and fired same day)
- Realistic durations (typical job: 2-5 years, not 3 days or 47 years)

**Date formats by region**:
- **US**: MM/DD/YYYY (12/31/2024)
- **Europe/ISO**: DD.MM.YYYY (31.12.2024) or YYYY-MM-DD (2024-12-31)
- **Narrative**: "December 31, 2024" or "31. Dezember 2024"

**Common patterns**:
- **Bank statements**: Monthly (always last day of month or first day of next)
- **Employment**: Start on 1st or 15th (common hire dates), end on month-end
- **ID expiration**: Round years (5-10 year validity)
- **Invoices**: Net 30 (due date 30 days after invoice date)

**Avoid**:
- ❌ February 30, April 31 (non-existent dates)
- ❌ Worked from 2020 to 2019 (time travel)
- ❌ Born in 2010, hired in 2005 (impossible)

---

## Addresses

### Realistic Address Formatting

**By country**:
- **US**: 123 Main Street, Apt 4B, Springfield, IL 62701
- **Germany**: Hauptstraße 45, 80331 München
- **UK**: 10 Downing Street, London SW1A 2AA
- **France**: 12 Rue de la Paix, 75002 Paris

**Realism tips**:
- Use real city names (not "City Name" or "Anytown")
- Match zip/postal codes to city (don't use 10001 for Los Angeles)
- Real street types (Street, Avenue, Boulevard, Lane, Drive - not "Road 123")
- Apartment/suite numbers for urban addresses (less common in suburban)

**Avoid**:
- ❌ "123 Main St, City, State, ZIP" (too generic)
- ❌ "Address Line 1" (placeholder text)
- ❌ Mixing country formats (US zip code with German city)

---

## Numbers & Identifiers

### ID Numbers, SSNs, Account Numbers

**Realistic formats**:
- **US SSN**: XXX-XX-XXXX (9 digits, specific ranges by state)
- **US Driver's License**: Varies by state (some alphanumeric, some numeric)
- **German ID (Personalausweis)**: L + 8 digits (e.g., L12345678)
- **UK National Insurance**: 2 letters + 6 digits + 1 letter (AB123456C)
- **Bank account**: Check country format (IBAN for Europe: DE89 3704 0044 0532 0130 00)
- **Credit card**: 16 digits, use test card numbers (4111 1111 1111 1111 for Visa test)

**Checksum awareness**:
- Some ID numbers have checksums (IBANs, credit cards with Luhn algorithm)
- If generating for realistic validation testing, use proper checksums
- If checksums not needed, just match the format

**Avoid**:
- ❌ 000-00-0000, 111-11-1111 (obviously fake)
- ❌ 123456789 for everything (not realistic)
- ❌ Mixing formats (US SSN format for German citizen)

---

## Financial Data

### Amounts, Currency, Precision

**Realistic amounts**:
- **Salaries**: Round numbers ($75,000/year, not $74,837.23/year)
- **Retail prices**: End in .99, .95, .00 ($19.99, $24.95, $50.00)
- **B2B invoices**: More precise ($12,847.50)
- **Bank balances**: Varied ($1,234.56, not always $1,000.00)
- **Rent**: Round hundreds ($1,800/month, not $1,847.23/month)

**Currency formatting**:
- **US**: $1,234.56
- **Europe**: 1.234,56 € or € 1.234,56
- **UK**: £1,234.56
- Include currency symbols consistently

**Transaction realism**:
- Bank statement: debits + credits = new balance (must calculate correctly!)
- Invoice: line items + tax = total (arithmetic must be correct)
- Not all transactions for same amount (vary realistically)
- Some transactions on weekends/holidays okay for automated payments

**Avoid**:
- ❌ Salary of $0.37 (nonsensical)
- ❌ All transactions exactly $100.00 (unrealistic uniformity)
- ❌ Balance doesn't match transaction history (math errors destroy credibility)

---

## Professional Terminology

### Domain-Specific Language

**Banking/Finance**:
- Use proper terms: "credit facility", "Kreditwürdigkeitsprüfung", "risk appetite", "MaRisk compliance"
- Not: "money stuff", "bank things"

**Healthcare**:
- Medical terms: "hypertension" not "high blood pressure issue", ICD-10 codes (I10 for hypertension)
- SOAP notes format: Subjective, Objective, Assessment, Plan

**Legal**:
- Proper clauses: "Force Majeure", "Indemnification", "Severability"
- Not: "bad things clause", "punishment section"

**Tech/IT**:
- Real technologies: "AWS Lambda", "PostgreSQL", "Kubernetes"
- Not: "cloud thing", "database software"

**Manufacturing**:
- Industry terms: "Six Sigma", "lean manufacturing", "OEE", "kanban"

**Source terminology**:
- If input context provides specific terms, USE THEM EXACTLY
- If input lacks terminology, research common terms for that domain
- Consistency: pick one term and stick with it (don't alternate "client" and "customer" randomly)

---

## Document Formatting

### Professional Document Standards

**Structure**:
- Headers/footers for multi-page docs (company name, page numbers)
- Proper sectioning (numbered sections: 1.1, 1.2, not random bullets)
- Tables for structured data (not prose for everything)
- Signature blocks where appropriate
- Version numbers and dates for policies/procedures

**Tone**:
- **Corporate docs**: Professional, formal ("The Company shall...", "Employees must...")
- **Emails**: Conversational but professional ("Hi Sarah, Thanks for reaching out...")
- **Clinical notes**: Concise, medical jargon ("Pt presents with...")
- **Legal**: Precise, formal ("Party A hereby agrees to indemnify Party B...")

**Formatting conventions**:
- Consistent heading styles (markdown: # for H1, ## for H2, etc.)
- Bullet points for lists, not paragraphs
- Bold for emphasis, not ALLCAPS (unless acronyms)
- Proper spacing (not walls of text)

---

## Cross-Document Consistency

### When Generating Multiple Related Documents

**Entity consistency**:
- Create a "master entity list" before generating documents
- Track: Names, addresses, ID numbers, companies, dates
- Reference master list when generating each document

**Example**: Customer journey (profile + invoices + support tickets)
1. Generate customer profile first: "Sarah Chen, 123 Oak Street, Chicago, IL"
2. Master list: `customer_001 = {name: "Sarah Chen", address: "123 Oak Street...", email: "schen@email.com"}`
3. Invoice references: "Bill To: Sarah Chen, 123 Oak Street..."
4. Support ticket: "Customer: Sarah Chen (schen@email.com)"

**Timeline consistency**:
- Events in chronological order
- No date contradictions (invoice dated Jan 10, support ticket about that invoice dated Jan 5)

**Relationship consistency**:
- Invoice #1234 referenced in support ticket must exist
- Employee mentioned in org chart must appear in employee list
- System mentioned in process doc must be in system landscape

---

## Variation Without Chaos

### Creating Realistic Diversity

**Good variation**:
- Different people have different names (obvious, but don't use same name 50 times)
- Amounts vary realistically (salaries: $50K-$200K range, not all $75K)
- Dates spread across reasonable range (not all hired on Jan 1)
- Mix of scenarios (some invoices paid, some overdue)

**Patterns to maintain**:
- All documents in same dataset follow same format
- Company name spelled identically everywhere
- Address formatting consistent across all addresses
- Date format consistent (don't mix MM/DD/YYYY and DD.MM.YYYY)

**Avoid**:
- ❌ All data points identical (100 customers, all named "John Smith")
- ❌ Completely random chaos (no patterns at all, unbelievable)
- ❌ Perfectly uniform distribution (real data has clusters and outliers)

---

## Cultural & Regional Awareness

### Localization Considerations

**Language**:
- German org docs should be IN GERMAN (Arbeitsanweisung, not "Work Instruction")
- Spanish invoices: "Factura", not "Invoice"
- Respect language conventions (formal vs. informal "you")

**Business practices**:
- US: At-will employment common
- Germany: Strong employee protections, works councils
- Japan: Lifetime employment tradition
- France: 35-hour work week standard

**Currency & measurements**:
- US: $ and imperial units (feet, pounds)
- Europe: € and metric (meters, kilograms)
- Don't mix: "Height: 6 feet, Weight: 80kg" (pick one system)

**Holidays & schedules**:
- US: Thanksgiving (November), no August vacation culture
- Europe: August shutdown common, more vacation days
- Different public holidays affect transaction dates

---

## Metadata for RAG Systems

### Ensuring Documents Are RAG-Friendly

**Include metadata** (YAML frontmatter or structured headers):
```yaml
---
document_id: INV-2024-001234
document_type: Invoice
date: 2024-11-15
customer: Sarah Chen
amount: 1234.56
status: paid
---
```

**Section headers**:
- Clear, descriptive headers (## Payment Terms, not ## Section 4)
- Hierarchical structure (H1 → H2 → H3)
- Enables chunking at logical boundaries

**Keywords**:
- Include searchable terms naturally in text
- Don't keyword-stuff, but ensure key concepts appear
- Use synonyms (e.g., "credit assessment" and "Kreditwürdigkeitsprüfung")

**Cross-references**:
- Link related documents explicitly ("See also: AA-KWP-001 Section 4.2")
- Enables graph-based retrieval

---

## Quality Checklist

Before finalizing generated data:

- [ ] Names are realistic and consistent across documents
- [ ] Dates are logical and chronologically sound
- [ ] Addresses match proper country/regional formats
- [ ] ID numbers follow correct formats
- [ ] Financial calculations are arithmetically correct
- [ ] Terminology is domain-appropriate
- [ ] Formatting is professional and consistent
- [ ] Cross-references between documents are valid
- [ ] Metadata is complete and accurate
- [ ] No placeholder text ("TODO", "XXX", "sample")
- [ ] No obvious fake markers ("John Doe", "000-00-0000")
- [ ] Cultural/regional conventions respected

---

## When to Prioritize Speed Over Realism

**High realism needed**:
- Demo to stakeholders
- Production-grade testing
- Training ML models
- Client deliverables

**Moderate realism acceptable**:
- Internal testing
- Proof-of-concept
- Quick prototypes
- Educational examples

Adjust effort based on use case. Always aim for "good enough" realism, not perfection.
