# Beam Next Skills Registry

Central repository of installable skills for [Beam Next](https://github.com/Beam-GTM/beam-next-raw).

## Structure

Skills are organized into category subfolders:

```
skills/
  hubspot/          # 22 HubSpot CRM skills
  langfuse/         # 60+ Langfuse observability skills
  google/           # Gmail, Calendar, Docs, Drive, Sheets, Slides, Gemini
  slack/            # Slack messaging
  notion/           # Notion databases
  airtable/         # Airtable bases
  heyreach/         # HeyReach outbound
  amie/             # Amie calendar & transcripts
  beam/             # Beam platform
  notebooklm/       # NotebookLM
  attio/            # Attio CRM
  happenstance/     # Happenstance LinkedIn
  workable/         # Workable ATS
  productivity/     # 1-on-1s, meetings, email
  experts/          # Expert review & improve
  projects/         # Project management
  learning/         # Onboarding & tutorials
  hiring/           # Interviewing & candidates
  sales/            # Lead research
  skill-dev/        # Skill creation & sharing
  tools/            # Formatting, mental models
  engineering/      # Handovers & production
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

See `registry.yaml` for a machine-readable index of all 189 available skills.

## Contribute

1. Add your skill folder under `skills/<category>/<skill-name>/`
2. Ensure it has a valid `SKILL.md` with YAML frontmatter
3. Run `build_registry.py` to regenerate the index
4. Open a PR
