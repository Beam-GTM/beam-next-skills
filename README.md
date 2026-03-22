# Beam Next Skills Library

Installable skills for [Beam Next](https://github.com/Beam-GTM/beam-next-raw). **144 skills** across integrations, general workflows, learning, and more.

## Install a Skill

```bash
# By name from the library
python3 install_skill.py hubspot-connect

# Search available skills
python3 search_skills.py "crm"

# From any GitHub URL
python3 install_skill.py https://github.com/someone/repo/tree/main/my-skill
```

## Structure

```
skills/
  beam/                 # Beam AI platform tools (connect, master, graph tools)
  beam-next-learning/   # Onboarding & tutorials
  general/              # Productivity, sales, projects, tools, engineering
  integrations/         # HubSpot, Langfuse, Google, Slack, Notion, Linear, …
scripts/                # Shared utilities (frontmatter validation)
```

### Category breakdown

| Category | Count |
|----------|-------|
| experts | 2 |
| general | 51 |
| integrations | 56 |
| learning | 11 |
| productivity | 4 |
| projects | 5 |
| skill-dev | 7 |
| system | 3 |
| tools | 5 |

### Integration platforms

| Platform | Skills |
|----------|--------|
| beam | 12 |
| google | 11 |
| langfuse | 11 |
| hubspot | 3 |
| airtable | 2 |
| amie | 2 |
| heyreach | 2 |
| miro | 2 |
| notebooklm | 2 |
| notion | 2 |
| slack | 2 |
| attio | 1 |
| figma | 1 |
| granola | 1 |
| happenstance | 1 |
| workable | 1 |

## Skills index

Full machine-readable index: [`registry.yaml`](registry.yaml). Regenerate with `python3 build_registry.py .`

| Skill | Version | Category |
|-------|---------|----------|
| expert-improve | 1.0 | experts |
| expert-review | 1.0 | experts |
| abstract | 1.0 | general |
| analyze-competitors | 1.0 | general |
| beam-credit-analysis | 1.1 | general |
| better-doc | 1.0 | general |
| blackbird | 1.0 | general |
| calculate-beam-agent-pricing | 1.0 | general |
| candidate-compare | 1.0 | general |
| create-beam-task-auto-trigger | 1.4 | general |
| create-client-project | 1.0 | general |
| create-data | 1.0 | general |
| create-meeting-minutes | 1.0 | general |
| create-meeting-presentation-html | 1.0 | general |
| create-ruleset | 1.0 | general |
| create-weekly-update | 1.0 | general |
| data-baker | 1.0 | general |
| dealroom-creation | 1.0 | general |
| demo-documentation-generation-agent | 1.2 | general |
| document-nodes | 1.0 | general |
| evaluate-solutions-case-study | 1.0 | general |
| extract-requirements | 1.0 | general |
| fathom | 1.2 | general |
| fathom-fetch-meetings | 1.0 | general |
| fathom-get-transcript | 1.0 | general |
| figma-connect | 1.0 | general |
| follow-up-automation | 1.0 | general |
| generate-demo-agent-sample-input-data | 1.0 | general |
| generate-linear-project-update | 1.0 | general |
| get-beam-agent-graph | 1.0 | general |
| git | 1.0 | general |
| graph-slicer | 1.2 | general |
| interview-coach | 2.0 | general |
| lead-research | 1.0 | general |
| linear-create-tickets | 1.0 | general |
| linear-update-tickets | 1.0 | general |
| linkedin-outbounding-automation | 1.0 | general |
| manager-review | 1.0 | general |
| okr-self-review | 1.0 | general |
| process-client-meeting | 1.0 | general |
| prompt-versioning | 1.0 | general |
| qa-checklist | 1.0 | general |
| qa-test-case-writer | 1.0 | general |
| scope-of-work-creation | 1.0 | general |
| select-llm-model | 1.3 | general |
| setup-linear-onboarding-template | 1.0 | general |
| setup-notion-customer-onboarding | 1.0 | general |
| tavily-gtm-research | 1.0 | general |
| transcript-to-hubspot-sections | 1.0 | general |
| ui-developer | 1.0 | general |
| ultrathink | 1.0 | general |
| update-variables-in-notion | 1.0 | general |
| write-integration-ticket | 1.0 | general |
| airtable-connect | 1.1 | integrations |
| airtable-master | 1.0 | integrations |
| amie-connect | 1.0 | integrations |
| amie-master | 1.0 | integrations |
| attio-connect | 1.0 | integrations |
| beam-agent-manager | 1.0 | integrations |
| beam-ape-optimizer | 1.0 | integrations |
| beam-connect | 1.0 | integrations |
| beam-debug-issue-tasks | 1.0 | integrations |
| beam-design-system | 1.0 | integrations |
| beam-feedback-automation | 1.0 | integrations |
| beam-get-agent-analytics | 1.0 | integrations |
| beam-get-task-details | 1.0 | integrations |
| beam-graph-creator | 1.0 | integrations |
| beam-graph-edit | 1.0 | integrations |
| beam-master | 1.0 | integrations |
| beam-put-payload-builder | 1.0 | integrations |
| beam-retry-tasks | 1.0 | integrations |
| create-deal | 1.0 | integrations |
| gmail | 1.3 | integrations |
| google-calendar | 1.0 | integrations |
| google-connect | 1.0 | integrations |
| google-docs | 1.0 | integrations |
| google-drive | 1.0 | integrations |
| google-gemini-image | 2.0 | integrations |
| google-master | 1.0 | integrations |
| google-sheets | 1.2 | integrations |
| google-slides | 1.0 | integrations |
| google-speech-to-text | 1.0 | integrations |
| google-tasks | 1.0 | integrations |
| happenstance-connect | 1.0 | integrations |
| heyreach-connect | 1.0 | integrations |
| heyreach-master | 1.0 | integrations |
| hubspot-connect | 1.0 | integrations |
| hubspot-crm | 1.0 | integrations |
| hubspot-master | 1.0 | integrations |
| langfuse-admin | 1.0 | integrations |
| langfuse-connect | 1.1 | integrations |
| langfuse-datasets | 1.0 | integrations |
| langfuse-ingestion | 1.0 | integrations |
| langfuse-master | 1.0 | integrations |
| langfuse-models | 1.0 | integrations |
| langfuse-prompts | 1.0 | integrations |
| langfuse-queues | 1.0 | integrations |
| langfuse-scores | 1.0 | integrations |
| langfuse-status | 1.0 | integrations |
| langfuse-traces | 1.0 | integrations |
| miro-connect | 1.0 | integrations |
| miro-master | 1.0 | integrations |
| notebooklm-connect | 1.0 | integrations |
| notebooklm-master | 1.0 | integrations |
| notion-connect | 1.1 | integrations |
| notion-master | 1.0 | integrations |
| slack-connect | 1.0 | integrations |
| slack-master | 1.0 | integrations |
| workable-master | 2.0 | integrations |
| analyze-context | 1.0 | learning |
| create-roadmap | 1.0 | learning |
| how-beam-next-works | 1.0 | learning |
| learn-beam-next | 1.0 | learning |
| learn-integrations | 1.0 | learning |
| learn-projects | 1.0 | learning |
| learn-skills | 1.0 | learning |
| quick-start | 2.0 | learning |
| setup-goals | 1.0 | learning |
| setup-memory | 1.0 | learning |
| setup-workspace | 1.0 | learning |
| 1on1-followup | 1.0 | productivity |
| 1on1-prep | 1.0 | productivity |
| 1on1-review | 1.0 | productivity |
| email-automation | 1.0 | productivity |
| archive-project | 1.0 | projects |
| bulk-complete | 1.0 | projects |
| create-project | 1.0 | projects |
| execute-project | 1.0 | projects |
| plan-project | 1.0 | projects |
| create-master-skill | 1.0 | skill-dev |
| create-skill | 1.0 | skill-dev |
| import-skill | 1.0 | skill-dev |
| search-skill-database | 1.0 | skill-dev |
| share-skill | 1.0 | skill-dev |
| validate-skill-functionality | 1.0 | skill-dev |
| add-integration | 1.0 | system |
| allhands-prep | 1.0 | system |
| list-skills | 1.0 | system |
| deep-thinking | 1.0 | tools |
| format-and-lint-code | 1.0 | tools |
| generate-philosophy-doc | 1.0 | tools |
| markdown-to-pdf | 1.0 | tools |
| mental-models | 1.0 | tools |

## Contribute

1. Add your skill folder under the appropriate category directory
2. Ensure it has a valid `SKILL.md` with YAML frontmatter (required: `name`, `description`; recommended: `version`, `category`, `tags`, `updated`)
3. Validate frontmatter: `python3 scripts/validate_skill_frontmatter.py`
4. Regenerate the index: `python3 build_registry.py .`
5. Open a PR
