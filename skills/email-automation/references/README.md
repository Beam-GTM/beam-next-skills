# Email Automation - Reference Files

This folder contains reference materials for generating AI-powered email drafts that match Jonas's authentic writing style.

## Files

### `jonas-writing-style.md`
**Comprehensive style guide** covering:
- Tone and structure
- Common phrases and patterns
- Response templates by email type
- DO's and DON'Ts
- Language mixing (German/English)
- AI draft generation instructions

**Usage**: Primary reference for AI models (Claude) when generating email drafts.

### `draft-examples.md`
**Quick reference library** with:
- 10 categories of common email scenarios
- Real examples in Jonas's style
- Context-specific templates
- German and mixed-language examples

**Usage**: Pattern matching for common email types.

### `classification-rules.yaml` (future)
**Email classification rules** for:
- Sender patterns (clients, team, investors, recruiters)
- Keyword triggers for categories
- Custom rules per sender/domain

**Usage**: Enhance AI classification accuracy.

---

## How It Works

1. **Email arrives** → Classified (URGENT, DO, RESPOND, etc.)
2. **Draft needed** → AI reads `jonas-writing-style.md`
3. **AI generates draft** → Following Jonas's patterns
4. **You review** → Edit if needed, send

---

## Maintaining Quality

### When to Update

Update these files when:
- Jonas's style evolves (new phrases, patterns)
- Common email scenarios change (new role, company stage)
- AI drafts consistently miss the mark on certain types

### What NOT to Change

Keep these consistent:
- Core tone (friendly, concise, action-oriented)
- Sign-off ("-Jonas" with hyphen)
- Structure (short paragraphs, clear next steps)
- No corporate jargon

---

## AI Model Integration (Coming Next)

### Phase 1: Template-Based (Current)
- Uses predefined templates from `draft-examples.md`
- Fills in brackets with context
- Fast but rigid

### Phase 2: AI-Powered (Next)
- Claude Sonnet 4.5 reads `jonas-writing-style.md`
- Generates fully contextual responses
- Adapts to each email's unique context
- Maintains Jonas's authentic style

### Phase 3: Learning (Future)
- Learns from accepted vs edited drafts
- Adapts style guide based on feedback
- Improves accuracy over time

---

**Last Updated**: 2026-02-11
