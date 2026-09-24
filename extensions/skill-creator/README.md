# skill-creator

Junie extension that packages the **skill-creator** agent skill: guidance for creating and updating effective Junie agent skills (`SKILL.md` folders) for Junie CLI and Junie in JetBrains IDEs. Follows the open [Agent Skills](https://agentskills.io/specification) format.

## What it provides

- Workflows for designing concise, high-signal skills
- Conventions for skill structure (`SKILL.md`, scripts, templates, checklists)
- Helper scripts to scaffold and validate skills

## Files

- `skills/skill-creator/SKILL.md` — main skill guide
- `skills/skill-creator/scripts/init_skill.py` — scaffold a new skill
- `skills/skill-creator/scripts/quick_validate.py` — quick validation helper

## Installation

1. In Junie CLI, run `/extensions` and add this repository as a marketplace:
   - `BrayanCaro/boring-junie-extension`
   - or `https://github.com/BrayanCaro/boring-junie-extension`
   - or `git@github.com:BrayanCaro/boring-junie-extension.git`
2. Install the **skill-creator** extension (project or user scope).
3. Use the skill when creating or updating Junie skills (`/skill-creator` or automatic match).
