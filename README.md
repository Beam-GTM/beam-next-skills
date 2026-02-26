# Beam Next Skills Registry

Central repository of installable skills for [Beam Next](https://github.com/Beam-GTM/beam-next-raw).

## Structure

```
skills/
  integrations/       # Platform & service integrations
    hubspot/          #   22 HubSpot CRM skills
    langfuse/         #   72 Langfuse observability skills
    google/           #   Gmail, Calendar, Docs, Drive, Sheets, Slides, Gemini
    slack/            #   Slack messaging
    notion/           #   Notion databases
    linear/           #   Linear project management
    fathom/           #   Fathom meeting transcripts
    figma/            #   Figma design files
    airtable/         #   Airtable bases
    heyreach/         #   HeyReach outbound
    amie/             #   Amie calendar & transcripts
    notebooklm/       #   NotebookLM
    attio/            #   Attio CRM
    happenstance/     #   Happenstance LinkedIn
    workable/         #   Workable ATS
    tavily/           #   Tavily research
  beam/               # Beam AI platform tools
    beam/             #   Core connect + master
    beam-tools/       #   Credit analysis, graph edit, retry, analytics, etc.
  beam-next-learning/ # Onboarding & tutorials
  general/            # Everything else
    productivity/     #   1-on-1s, meetings, email
    experts/          #   Expert review & improve
    projects/         #   Project management
    sales/            #   Lead research, SOWs, follow-ups
    tools/            #   Mental models, formatting, writing
    hiring/           #   Interviewing & candidates
    skill-dev/        #   Skill creation & sharing
    research/         #   Competitive analysis, requirements
    engineering/      #   API planning, QA, UI dev
```

## Install a Skill

```bash
# By name from the registry
python3 install_skill.py hubspot-connect

# Search available skills
python3 search_skills.py "crm"

# From any GitHub URL
python3 install_skill.py https://github.com/someone/repo/tree/main/my-skill
```

## Browse Skills

See `registry.yaml` for a machine-readable index of all 237 available skills.

Each skill includes metadata: `author`, `category`, `tags`, `platform`, `version`, `updated`, `visibility`.

## Contribute

1. Add your skill folder under the appropriate category
2. Ensure it has a valid `SKILL.md` with YAML frontmatter
3. Run `build_registry.py` to regenerate the index
4. Open a PR
