# Beam Next Skills Registry

Central repository of installable skills for [Beam Next](https://github.com/Beam-GTM/beam-next-raw).

## Install a Skill

```bash
python3 00-system/skills/system/install-skill/scripts/install_skill.py <skill-name>
```

## Browse Skills

See `registry.yaml` for a machine-readable index of all available skills.

## Contribute

1. Add your skill folder under `skills/<skill-name>/`
2. Ensure it has a valid `SKILL.md` with YAML frontmatter
3. Run `build_registry.py` to regenerate the index
4. Open a PR
