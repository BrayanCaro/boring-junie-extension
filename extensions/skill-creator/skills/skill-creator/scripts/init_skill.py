#!/usr/bin/env python3
"""
Skill Initializer - Creates a new Junie agent skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--resources scripts,templates,checklists] [--examples]

Examples:
    init_skill.py my-new-skill --path .junie/skills
    init_skill.py my-new-skill --path .junie/skills --resources scripts,checklists
    init_skill.py my-api-helper --path .junie/skills --resources templates --examples
    init_skill.py custom-skill --path ~/.junie/skills
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "templates", "checklists"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

Use this skill when [describe when Junie should use this skill].

## Key Principles

[TODO: Add core principles for this skill]

## Guidelines

[TODO: Add specific guidelines and instructions]

## Examples

[TODO: Include code examples, patterns, or references to project files]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that Junie can run directly.

**Appropriate for:** Automation scripts, data processing, file conversion, or any code that performs specific operations deterministically.

### templates/
Boilerplate code or document templates Junie can use as starting points.

**Appropriate for:** Component scaffolds, file templates, boilerplate code, or any files meant to be copied or modified.

### checklists/
Step-by-step verification lists for complex processes.

**Appropriate for:** Code review checklists, deployment verification, migration steps, or any multi-step workflow where completeness matters.

---

**Not every skill requires all three types of resources.**
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that Junie can execute directly.
Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_TEMPLATE = """// Template for {skill_name}
// This is a placeholder template file.
// Replace with actual template content or delete if not needed.

// Example: component scaffold, API endpoint boilerplate,
// configuration file template, etc.
"""

EXAMPLE_CHECKLIST = """# Checklist for {skill_title}

This is a placeholder checklist. Replace with actual items or delete if not needed.

- [ ] Item 1: Describe what to verify
- [ ] Item 2: Describe what to verify
- [ ] Item 3: Describe what to verify

## Notes
- Add any context or references for each checklist item
- Link to relevant project files where applicable
"""


def normalize_skill_name(skill_name):
    """Normalize a skill name to lowercase hyphen-case."""
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def parse_resources(raw_resources):
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed = ", ".join(sorted(ALLOWED_RESOURCES))
        print(f"[ERROR] Unknown resource type(s): {', '.join(invalid)}")
        print(f"   Allowed: {allowed}")
        sys.exit(1)
    deduped = []
    seen = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def create_resource_dirs(skill_dir, skill_name, skill_title, resources, include_examples):
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        if resource == "scripts":
            if include_examples:
                example_script = resource_dir / "example.py"
                example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
                print("[OK] Created scripts/example.py")
            else:
                print("[OK] Created scripts/")
        elif resource == "templates":
            if include_examples:
                example_template = resource_dir / "example.txt"
                example_template.write_text(EXAMPLE_TEMPLATE.format(skill_name=skill_name))
                print("[OK] Created templates/example.txt")
            else:
                print("[OK] Created templates/")
        elif resource == "checklists":
            if include_examples:
                example_checklist = resource_dir / "checklist.md"
                example_checklist.write_text(EXAMPLE_CHECKLIST.format(skill_title=skill_title))
                print("[OK] Created checklists/checklist.md")
            else:
                print("[OK] Created checklists/")


def init_skill(skill_name, path, resources, include_examples):
    """
    Initialize a new Junie skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created (e.g., .junie/skills)
        resources: Resource directories to create
        include_examples: Whether to create example files in resource directories

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        print("[OK] Created SKILL.md")
    except Exception as e:
        print(f"[ERROR] Error creating SKILL.md: {e}")
        return None

    # Create resource directories if requested
    if resources:
        try:
            create_resource_dirs(skill_dir, skill_name, skill_title, resources, include_examples)
        except Exception as e:
            print(f"[ERROR] Error creating resource directories: {e}")
            return None

    # Print next steps
    print(f"\n[OK] Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    if resources:
        if include_examples:
            print("2. Customize or delete the example files in scripts/, templates/, and checklists/")
        else:
            print("2. Add resources to scripts/, templates/, and checklists/ as needed")
    else:
        print("2. Create resource directories only if needed (scripts/, templates/, checklists/)")
    print("3. Run quick_validate.py when ready to check the skill structure")
    print("4. Ask Junie to list its available skills to confirm it loaded correctly")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Create a new Junie skill directory with a SKILL.md template.",
    )
    parser.add_argument("skill_name", help="Skill name (normalized to hyphen-case)")
    parser.add_argument("--path", required=True, help="Output directory for the skill (e.g., .junie/skills)")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated list: scripts,templates,checklists",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create example files inside the selected resource directories",
    )
    args = parser.parse_args()

    raw_skill_name = args.skill_name
    skill_name = normalize_skill_name(raw_skill_name)
    if not skill_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        sys.exit(1)
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(
            f"[ERROR] Skill name '{skill_name}' is too long ({len(skill_name)} characters). "
            f"Maximum is {MAX_SKILL_NAME_LENGTH} characters."
        )
        sys.exit(1)
    if skill_name != raw_skill_name:
        print(f"Note: Normalized skill name from '{raw_skill_name}' to '{skill_name}'.")

    resources = parse_resources(args.resources)
    if args.examples and not resources:
        print("[ERROR] --examples requires --resources to be set.")
        sys.exit(1)

    path = args.path

    print(f"Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    if resources:
        print(f"   Resources: {', '.join(resources)}")
        if args.examples:
            print("   Examples: enabled")
    else:
        print("   Resources: none (create as needed)")
    print()

    result = init_skill(skill_name, path, resources, args.examples)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
