---
name: tavily-gtm-research
version: '1.0'
description: Load when user mentions "tavily research", "market intelligence", "competitive
  research", "GTM research", or needs real-time market data for sales, marketing,
  or vertical strategy.
category: general
tags:
- sales
- tavily
platform: Tavily
updated: '2026-01-16'
visibility: public
metadata:
  version: '1.0'
---
# Tavily GTM Research

Real-time market intelligence and competitive research for GTM teams using Tavily's AI-powered search.

## Purpose

Enable GTM teams to conduct fast, comprehensive market research using Tavily's AI-powered search capabilities. This skill provides role-specific workflows for sales, marketing, customer success, partnerships, and vertical strategy, transforming research from a 30-minute manual process into a 5-minute AI-assisted workflow.

**Key Benefits:**
- **80% faster research** - From 30 minutes to 5 minutes per task
- **More comprehensive insights** - 10-15 sources vs. 3-5 traditional sources
- **Real-time data** - Current information, not training data
- **Source attribution** - All results include URLs and citations
- **Consistent quality** - Standardized research across team

---

## When to Use

### Pre-Meeting Research
- Research prospect companies before sales calls
- Understand client's industry challenges
- Find recent news, funding, or strategic initiatives

### Competitive Intelligence
- Track competitor product launches and updates
- Monitor competitor messaging and positioning
- Identify differentiation opportunities

### Industry Trends
- Monitor vertical-specific market trends
- Track emerging pain points and shifts
- Gather statistics and data points

### Technical Validation
- Research integration possibilities
- Find API documentation for prospects' tech stack
- Validate technical approaches

### Content Creation
- Find statistics for proposals and presentations
- Research industry best practices
- Validate claims and trends

### Partnership Development
- Research potential partners and their ecosystems
- Understand partner technology stacks
- Find integration opportunities

---

## Prerequisites

✅ **Tavily MCP must be configured in Cursor**

**Setup Instructions:**
1. See: `/01-memory/integrations/TAVILY-SETUP-GUIDE.md` for complete setup
2. Or: `/01-memory/integrations/INSTALL-NOW.md` for quick start
3. Verify: Ask "Search Tavily for test query" to confirm it's working

**If not configured:**
- Configuration file: `/01-memory/integrations/tavily-mcp-config.json`
- Full documentation: `/01-memory/integrations/tavily-mcp.md`

---

## Quick Start

### Basic Search
```
Search Tavily for "AI automation trends 2026"
```

### Advanced Search (Deeper Research)
```
Search Tavily for "recruitment technology market" with advanced depth
```

### Domain-Specific Search
```
Search Tavily for "competitor analysis" only from crunchbase.com and linkedin.com
```

### Content Extraction
```
Extract content from https://example.com/article using Tavily
```

---

## Use Cases by Role

### For Account Executives (AEs)

**Pre-Call Research**
```
Search Tavily for "[Company Name] recent news 2026"
Search Tavily for "[Company Name] industry challenges"
Search Tavily for "[Company Name] competitors"
```

**Competitive Positioning**
```
Search Tavily for "[Competitor] vs Beam AI comparison"
Search Tavily for "[Competitor] customer reviews" only from g2.com and trustradius.com
```

**Deal Support**
```
Search Tavily for "[Industry] ROI statistics automation"
Search Tavily for "[Technology] implementation best practices"
```

**Time Savings:** 25 minutes → 5 minutes per prospect research

---

### For SDRs (Sales Development Reps)

**Account Qualification**
```
Search Tavily for "[Company Name] tech stack"
Search Tavily for "[Company Name] pain points [industry]"
Search Tavily for "[Industry] automation challenges 2026"
```

**Personalization**
```
Search Tavily for "[Prospect Name] LinkedIn recent activity"
Search Tavily for "[Company Name] recent announcements"
```

**Industry Research**
```
Search Tavily for "[Industry] trends 2026"
Search Tavily for "[Vertical] market size statistics"
```

**Time Savings:** 15 minutes → 3 minutes per prospect research

---

### For Customer Success Managers (CSMs)

**Account Expansion Research**
```
Search Tavily for "[Customer Name] expansion news"
Search Tavily for "[Customer Industry] trends affecting operations"
Search Tavily for "use cases for [product] in [customer industry]"
```

**QBR Preparation**
```
Search Tavily for "[Customer Industry] benchmarks 2026"
Search Tavily for "[Customer Industry] best practices"
Search Tavily for "[Technology] ROI case studies"
```

**Risk Monitoring**
```
Search Tavily for "[Customer Name] layoffs or restructuring"
Search Tavily for "[Customer Industry] economic challenges"
```

**Time Savings:** 20 minutes → 5 minutes per QBR prep

---

### For Marketing Team

**Content Research**
```
Search Tavily for "[Topic] statistics 2026"
Search Tavily for "[Industry] case study examples"
Search Tavily for "[Topic] trending discussions" only from medium.com and substack.com
```

**Campaign Intelligence**
```
Search Tavily for "trending topics in [vertical] 2026"
Search Tavily for "[Competitor] marketing campaigns"
Search Tavily for "[Industry] content marketing examples"
```

**SEO & Thought Leadership**
```
Search Tavily for "[Topic] frequently asked questions"
Search Tavily for "[Industry] pain points discussions"
```

**Time Savings:** 30 minutes → 5 minutes per content piece research

---

### For Partnerships Team

**Partner Research**
```
Search Tavily for "[Potential Partner] company overview"
Search Tavily for "[Potential Partner] integration partners"
Search Tavily for "[Vertical] technology ecosystem map"
```

**Ecosystem Mapping**
```
Search Tavily for "[Technology] popular integrations"
Search Tavily for "[Platform] partner program"
```

**Due Diligence**
```
Search Tavily for "[Partner] customer reviews"
Search Tavily for "[Partner] recent funding or news"
```

**Time Savings:** 40 minutes → 10 minutes per partner evaluation

---

### For Vertical Leads

**Market Intelligence**
```
Search Tavily for "[Vertical] automation trends 2026"
Search Tavily for "[Vertical] market size and growth" only from gartner.com and forrester.com
Search Tavily for "[Vertical] emerging technologies"
```

**Competitive Landscape**
```
Search Tavily for "[Vertical] key players and vendors"
Search Tavily for "[Competitor] market share [vertical]"
Search Tavily for "[Vertical] vendor comparison"
```

**Strategic Planning**
```
Search Tavily for "[Vertical] regulatory changes 2026"
Search Tavily for "[Vertical] investment trends"
Search Tavily for "[Vertical] pain points survey data"
```

**Time Savings:** 45 minutes → 10 minutes per market research task

---

## Search Patterns & Templates

### Pre-Meeting Research Template
```
1. Search Tavily for "[Company] recent news 2026"
2. Search Tavily for "[Company] [industry] challenges"
3. Search Tavily for "[Company] tech stack"
4. Search Tavily for "[Industry] trends 2026"
```

### Competitive Intelligence Template
```
1. Search Tavily for "[Competitor] product updates 2026"
2. Search Tavily for "[Competitor] vs [Our Product] comparison"
3. Search Tavily for "[Competitor] customer reviews" only from g2.com
4. Search Tavily for "[Competitor] pricing changes"
```

### Content Research Template
```
1. Search Tavily for "[Topic] statistics 2026"
2. Search Tavily for "[Topic] case studies"
3. Search Tavily for "[Topic] best practices"
4. Search Tavily for "[Topic] expert opinions" only from authoritative-site.com
```

### Technical Validation Template
```
1. Search Tavily for "[Technology] API documentation"
2. Search Tavily for "[Technology] integration guide"
3. Search Tavily for "[Technology] implementation examples"
4. Search Tavily for "[Technology] common issues"
```

---

## Best Practices

### Query Optimization

**Be Specific**
- ❌ Bad: "Search Tavily for AI"
- ✅ Good: "Search Tavily for AI automation in recruitment 2026"

**Use Quotes for Exact Phrases**
- ❌ Bad: "Search Tavily for machine learning model"
- ✅ Good: "Search Tavily for 'machine learning model deployment best practices'"

**Add Time Context**
- ❌ Bad: "Search Tavily for market trends"
- ✅ Good: "Search Tavily for market trends 2026"

**Filter by Authority**
- ❌ Bad: "Search Tavily for statistics"
- ✅ Good: "Search Tavily for statistics only from statista.com and census.gov"

### Search Depth Selection

**Use Basic (default) for:**
- Quick facts and general information
- Initial exploration
- Time-sensitive research

**Use Advanced for:**
- Comprehensive research
- Detailed analysis
- Critical decision-making

### Domain Filtering

**Authoritative Sources:**
```
only from gartner.com and forrester.com and mckinsey.com
```

**News Sources:**
```
only from techcrunch.com and reuters.com and bloomberg.com
```

**Tech Documentation:**
```
only from github.com and stackoverflow.com and docs.domain.com
```

**Business Intelligence:**
```
only from crunchbase.com and linkedin.com and glassdoor.com
```

### Rate Limits & Usage

**Development API Key Limits:**
- 1,000 searches per month
- Monitor at: https://tavily.com/dashboard
- Upgrade if needed for production use

**Best Practices:**
- Use basic search for quick lookups
- Save advanced for deep research
- Cache results when possible
- Combine with other research methods

---

## Integration with Nexus Skills

### Enhanced Skills

**`discovery-brief`**
- Use Tavily for client industry research
- Gather competitive landscape data
- Find recent company news and initiatives

**`scope-of-work-creation`**
- Research technical feasibility
- Find integration documentation
- Validate technology choices

**`client-qbr-report`**
- Gather industry trends and statistics
- Find relevant case studies
- Research best practices

**`qualify-opportunity`**
- Research prospect company background
- Understand industry challenges
- Validate fit signals

**`add-integration`**
- Find API documentation
- Discover endpoint references
- Locate authentication guides

---

## Troubleshooting

### Issue: Tavily tools not appearing

**Solution:**
1. Verify Tavily MCP is configured in `/Users/suf/.cursor/mcp.json`
2. Restart Cursor completely (⌘ + Q, then reopen)
3. Wait 5-10 seconds for MCP servers to initialize
4. Test with: "Search Tavily for test query"

### Issue: No results found

**Solution:**
- Broaden search terms
- Remove domain filters
- Check spelling
- Try different keywords

### Issue: Irrelevant results

**Solution:**
- Add more specific terms
- Use domain filtering
- Try advanced search depth
- Add year/context (2026)

### Issue: Rate limit exceeded

**Solution:**
- Check usage at https://tavily.com/dashboard
- Wait for monthly reset
- Consider upgrading plan
- Use alternative research methods

### Issue: Authentication errors

**Solution:**
- Verify API key in MCP config
- Check for extra spaces or quotes
- Ensure key starts with `tvly-`
- Restart Cursor after config changes

---

## Resources

### Quick Reference
- **Command Templates**: `references/quick-commands.md`
- **GTM Playbook**: `references/gtm-playbook.md`
- **Domain Filters**: `references/domain-filters.md`
- **Success Stories**: `references/success-stories.md`

### Tavily Documentation
- **Setup Guide**: `/01-memory/integrations/TAVILY-SETUP-GUIDE.md`
- **Quick Start**: `/01-memory/integrations/INSTALL-NOW.md`
- **Complete Docs**: `/01-memory/integrations/tavily-mcp.md`
- **How MCP Works**: `/01-memory/integrations/tavily-mcp-explained.md`
- **Quick Reference**: `/01-memory/integrations/tavily-quick-reference.md`

### External Links
- **Tavily Dashboard**: https://tavily.com/dashboard
- **Tavily API Docs**: https://docs.tavily.com
- **MCP Documentation**: https://modelcontextprotocol.io

---

## Success Metrics

### Individual Metrics
- **Research time**: 30 min → 5 min per task (83% reduction)
- **Sources per research**: 3-5 → 10-15 (3x increase)
- **Research quality**: Self-reported improvement
- **Use frequency**: Track daily usage

### Team Metrics
- **Adoption rate**: % of team using Tavily weekly
- **Use cases created**: Team-contributed workflows
- **Time savings**: Aggregate across team
- **Quality feedback**: Team satisfaction scores

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-16 | Initial release with role-specific use cases |

---

**Created**: 2026-01-16  
**Author**: Nexus GTM Team  
**Status**: Production Ready  
**Team**: General  
**Integration**: Tavily
