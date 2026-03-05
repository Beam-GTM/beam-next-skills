# Beam Next Skills Library

Installable skills for [Beam Next](https://github.com/Beam-GTM/beam-next-raw). 240 skills across integrations, general workflows, learning, and more.

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
  integrations/       # HubSpot, Langfuse, Google, Slack, Notion, Linear, Airtable, …
  beam/               # Beam AI platform tools
  beam-next-learning/ # Onboarding & tutorials
  general/            # Productivity, sales, projects, tools, engineering, …
```

## Skills overview

Extended index with owner and version. See `registry.yaml` for the full machine-readable index.

| Skill | Owner | Version | Category |
|-------|-------|---------|----------|
| expert-improve | — | 1.0 | experts |
| expert-review | — | 1.0 | experts |
| abstract | — | 1.0 | general |
| analyze-competitors | Mahnoor Jawed | 1.0 | general |
| better-doc | Jack Li | 1.0 | general |
| blackbird | Jack Li | 1.0 | general |
| calculate-beam-agent-pricing | Safi Haider | 1.0 | general |
| candidate-compare | Manahil Shaikh | 1.0 | general |
| create-beam-task-auto-trigger | Safi Haider | 1.4 | general |
| create-client-project | Hassaan Ahmed | 1.0 | general |
| create-data | Aqib Ansari | 1.0 | general |
| create-meeting-minutes | Hassaan Ahmed | 1.0 | general |
| create-meeting-presentation-html | Hassaan Ahmed | 1.0 | general |
| create-ruleset | Aqib Ansari | 1.0 | general |
| create-weekly-update | — | 1.0 | general |
| data-baker | Safi Haider | 1.0 | general |
| dealroom-creation | Quentin | 1.0 | general |
| demo-documentation-generation-agent | Safi Haider | 1.2 | general |
| design-beam-agent | — | 1.0 | general |
| document-nodes | — | 1.0 | general |
| evaluate-solutions-case-study | Sven Djokic | 1.0 | general |
| extract-requirements | Sven Djokic | 1.0 | general |
| fathom | Hassaan Ahmed | 1.2 | general |
| fathom-fetch-meetings | Hassaan Ahmed | 1.0 | general |
| fathom-get-transcript | Hassaan Ahmed | 1.0 | general |
| figma-connect | Mo Bekdache | 1.0 | general |
| follow-up-automation | Quentin | 1.0 | general |
| generate-demo-agent-sample-input-data | Hassaan Ahmed, Safi Haider | 1.0 | general |
| generate-linear-project-update | Jack Li | 1.0 | general |
| get-beam-agent-graph | Safi Haider | 1.0 | general |
| git | Abdul Rafay | 1.0 | general |
| graph-slicer | Sven Djokic | 1.2 | general |
| interview-coach | Jonas Diezun | 2.0 | general |
| lead-research | Jonas Diezun | 1.0 | general |
| linear-create-tickets | Hassaan Ahmed | 1.0 | general |
| linear-update-tickets | Hassaan Ahmed | 1.0 | general |
| linkedin-outbounding-automation | — | 1.0 | general |
| process-client-meeting | Hassaan Ahmed | 1.0 | general |
| prompt-versioning | Anas Duksi | 1.0 | general |
| qa-checklist | Jack Li | 1.0 | general |
| qa-test-case-writer | Ahsun Iqbal | 1.0 | general |
| scope-of-work-creation | Quentin | 1.0 | general |
| select-llm-model | — | 1.3 | general |
| setup-linear-onboarding-template | Jack Li | 1.0 | general |
| setup-notion-customer-onboarding | Jack Li | 1.0 | general |
| tavily-gtm-research | — | 1.0 | general |
| transcript-to-hubspot-sections | — | 1.0 | general |
| ui-developer | — | 1.0 | general |
| ultrathink | Quentin | 1.0 | general |
| update-variables-in-notion | Jack Li | 1.0 | general |
| write-integration-ticket | Saqib | 1.0 | general |
| airtable-connect | — | 1.1 | integrations |
| airtable-master | — | 1.0 | integrations |
| amie-connect | — | 1.0 | integrations |
| amie-master | — | 1.0 | integrations |
| attio-connect | — | 1.0 | integrations |
| beam-connect | — | 1.0 | integrations |
| beam-debug-issue-tasks | Jack Li | 1.0 | integrations |
| beam-design-system | Mo Bekdache | 1.0 | integrations |
| beam-feedback-automation | — | 1.0 | integrations |
| beam-get-agent-analytics | Hassaan Ahmed | 1.0 | integrations |
| beam-get-task-details | Hassaan Ahmed | 1.0 | integrations |
| beam-graph-edit | Anas Duksi | 1.0 | integrations |
| beam-master | — | 1.0 | integrations |
| beam-retry-tasks | Jack Li | 1.0 | integrations |
| create-deal | — | 1.0 | integrations |
| gemini-edit-image | — | 1.0 | integrations |
| gemini-generate-image | — | 1.0 | integrations |
| gemini-refine-image | — | 1.0 | integrations |
| gmail | Fredrik Falk | 1.3 | integrations |
| google-calendar | Fredrik Falk | 1.0 | integrations |
| google-connect | Fredrik Falk | 1.0 | integrations |
| google-docs | Fredrik Falk | 1.0 | integrations |
| google-drive | Fredrik Falk | 1.0 | integrations |
| google-gemini-image | — | 1.0 | integrations |
| google-integration | Fredrik Falk | 1.1 | integrations |
| google-master | Fredrik Falk | 1.0 | integrations |
| google-sheets | Fredrik Falk | 1.2 | integrations |
| google-slides | Fredrik Falk | 1.0 | integrations |
| google-speech-to-text | — | 1.0 | integrations |
| google-tasks | Fredrik Falk | 1.0 | integrations |
| happenstance-connect | — | 1.0 | integrations |
| heyreach | — | 1.0 | integrations |
| heyreach-connect | — | 1.0 | integrations |
| heyreach-master | — | 1.0 | integrations |
| hubspot-connect | — | 1.0 | integrations |
| hubspot-create-company | — | 1.0 | integrations |
| hubspot-create-contact | — | 1.0 | integrations |
| hubspot-create-deal | — | 1.0 | integrations |
| hubspot-create-deal-from-transcript | — | 1.0 | integrations |
| hubspot-create-meeting | — | 1.0 | integrations |
| hubspot-create-note | — | 1.0 | integrations |
| hubspot-get-associations | — | 1.0 | integrations |
| hubspot-list-calls | — | 1.0 | integrations |
| hubspot-list-companies | — | 1.0 | integrations |
| hubspot-list-contacts | — | 1.0 | integrations |
| hubspot-list-deals | — | 1.0 | integrations |
| hubspot-list-emails | — | 1.0 | integrations |
| hubspot-list-meetings | — | 1.0 | integrations |
| hubspot-list-notes | — | 1.0 | integrations |
| hubspot-log-call | — | 1.0 | integrations |
| hubspot-log-email | — | 1.0 | integrations |
| hubspot-master | — | 1.0 | integrations |
| hubspot-search-companies | — | 1.0 | integrations |
| hubspot-search-contacts | — | 1.0 | integrations |
| hubspot-search-deals | — | 1.0 | integrations |
| hubspot-update-contact | — | 1.0 | integrations |
| hubspot-update-deal | — | 1.0 | integrations |
| langfuse-batch-ingest | — | 1.0 | integrations |
| langfuse-connect | — | 1.0 | integrations |
| langfuse-create-annotation-queue | — | 1.0 | integrations |
| langfuse-create-comment | — | 1.0 | integrations |
| langfuse-create-dataset | — | 1.0 | integrations |
| langfuse-create-dataset-item | — | 1.0 | integrations |
| langfuse-create-dataset-run-item | — | 1.0 | integrations |
| langfuse-create-model | — | 1.0 | integrations |
| langfuse-create-project | — | 1.0 | integrations |
| langfuse-create-project-api-key | — | 1.0 | integrations |
| langfuse-create-prompt | — | 1.0 | integrations |
| langfuse-create-queue-assignment | — | 1.0 | integrations |
| langfuse-create-queue-item | — | 1.0 | integrations |
| langfuse-create-score | — | 1.0 | integrations |
| langfuse-create-score-config | — | 1.0 | integrations |
| langfuse-delete-dataset-item | — | 1.0 | integrations |
| langfuse-delete-dataset-run | — | 1.0 | integrations |
| langfuse-delete-model | — | 1.0 | integrations |
| langfuse-delete-org-membership | — | 1.0 | integrations |
| langfuse-delete-project | — | 1.0 | integrations |
| langfuse-delete-project-api-key | — | 1.0 | integrations |
| langfuse-delete-prompt | — | 1.0 | integrations |
| langfuse-delete-queue-assignment | — | 1.0 | integrations |
| langfuse-delete-queue-item | — | 1.0 | integrations |
| langfuse-delete-score | — | 1.0 | integrations |
| langfuse-delete-trace | — | 1.0 | integrations |
| langfuse-delete-traces | — | 1.0 | integrations |
| langfuse-get-annotation-queue | — | 1.0 | integrations |
| langfuse-get-comment | — | 1.0 | integrations |
| langfuse-get-dataset | — | 1.0 | integrations |
| langfuse-get-dataset-item | — | 1.0 | integrations |
| langfuse-get-dataset-run | — | 1.0 | integrations |
| langfuse-get-media | — | 1.0 | integrations |
| langfuse-get-model | — | 1.0 | integrations |
| langfuse-get-observation | — | 1.0 | integrations |
| langfuse-get-project | — | 1.0 | integrations |
| langfuse-get-prompt | — | 1.0 | integrations |
| langfuse-get-queue-item | — | 1.0 | integrations |
| langfuse-get-score | — | 1.0 | integrations |
| langfuse-get-score-config | — | 1.0 | integrations |
| langfuse-get-session | — | 1.0 | integrations |
| langfuse-get-trace | — | 1.0 | integrations |
| langfuse-get-upload-url | — | 1.0 | integrations |
| langfuse-health | — | 1.0 | integrations |
| langfuse-help | — | 1.0 | integrations |
| langfuse-list-annotation-queues | — | 1.0 | integrations |
| langfuse-list-comments | — | 1.0 | integrations |
| langfuse-list-dataset-items | — | 1.0 | integrations |
| langfuse-list-dataset-run-items | — | 1.0 | integrations |
| langfuse-list-dataset-runs | — | 1.0 | integrations |
| langfuse-list-datasets | — | 1.0 | integrations |
| langfuse-list-models | — | 1.0 | integrations |
| langfuse-list-observations | — | 1.0 | integrations |
| langfuse-list-org-api-keys | — | 1.0 | integrations |
| langfuse-list-org-memberships | — | 1.0 | integrations |
| langfuse-list-org-projects | — | 1.0 | integrations |
| langfuse-list-project-api-keys | — | 1.0 | integrations |
| langfuse-list-prompts | — | 1.0 | integrations |
| langfuse-list-queue-items | — | 1.0 | integrations |
| langfuse-list-score-configs | — | 1.0 | integrations |
| langfuse-list-scores | — | 1.0 | integrations |
| langfuse-list-sessions | — | 1.0 | integrations |
| langfuse-list-traces | — | 1.0 | integrations |
| langfuse-master | — | 1.0 | integrations |
| langfuse-metrics | — | 1.0 | integrations |
| langfuse-otel-ingest | — | 1.0 | integrations |
| langfuse-update-media | — | 1.0 | integrations |
| langfuse-update-org-membership | — | 1.0 | integrations |
| langfuse-update-project | — | 1.0 | integrations |
| langfuse-update-prompt-version | — | 1.0 | integrations |
| langfuse-update-queue-item | — | 1.0 | integrations |
| langfuse-update-score-config | — | 1.0 | integrations |
| notebooklm | — | 1.0 | integrations |
| notebooklm-connect | — | 1.0 | integrations |
| notebooklm-master | — | 1.0 | integrations |
| notion-connect | — | 1.1 | integrations |
| notion-master | — | 1.0 | integrations |
| slack | Fredrik Falk | 1.1 | integrations |
| slack-connect | Fredrik Falk | 1.0 | integrations |
| slack-master | Fredrik Falk | 1.0 | integrations |
| workable-master | Jonas Diezun | 2.0 | integrations |
| analyze-context | — | 1.0 | learning |
| create-roadmap | — | 1.0 | learning |
| how-beam-next-works | — | 1.0 | learning |
| learn-beam-next | — | 1.0 | learning |
| learn-integrations | — | 1.0 | learning |
| learn-projects | — | 1.0 | learning |
| learn-skills | — | 1.0 | learning |
| quick-start | — | 2.0 | learning |
| setup-goals | — | 1.0 | learning |
| setup-memory | — | 1.0 | learning |
| setup-workspace | — | 1.0 | learning |
| 1on1-followup | Jonas Diezun | 1.0 | productivity |
| 1on1-prep | Jonas Diezun | 1.0 | productivity |
| 1on1-review | Jonas Diezun | 1.0 | productivity |
| email-automation | Jonas Diezun | 1.0 | productivity |
| archive-project | — | 1.0 | projects |
| bulk-complete | — | 1.0 | projects |
| create-project | — | 1.0 | projects |
| execute-project | — | 1.0 | projects |
| plan-project | — | 1.0 | projects |
| create-master-skill | — | 1.0 | skill-dev |
| create-skill | — | 1.0 | skill-dev |
| import-skill | — | 1.0 | skill-dev |
| search-skill-database | — | 1.0 | skill-dev |
| share-skill | — | 1.0 | skill-dev |
| validate-skill-functionality | — | 1.0 | skill-dev |
| add-integration | — | 1.0 | system |
| allhands-prep | — | 1.0 | system |
| list-skills | — | 1.0 | system |
| mid-session-cleanup | — | 1.0 | system |
| format-and-lint-code | — | 1.0 | tools |
| generate-philosophy-doc | — | 1.0 | tools |
| mental-models | — | 1.0 | tools |

## Contribute

1. Add your skill folder under the appropriate category
2. Ensure it has a valid `SKILL.md` with YAML frontmatter (required: `name`, `description`; recommended: `author`, `version`, `category`)
3. Regenerate the index (README overview updates automatically):
   ```bash
   python3 build_registry.py .
   ```
4. Open a PR
