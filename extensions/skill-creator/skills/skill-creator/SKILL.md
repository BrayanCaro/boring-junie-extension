---
name: skill-creator
description: Guide for creating effective Junie agent skills. Use this skill when creating a new Junie agent skill or updating an existing one. Junie skills are folders with a SKILL.md file that provide task-specific context to Junie CLI and Junie in JetBrains IDEs. Follows the open Agent Skills specification (agentskills.io).
---

# Skill Creator

This skill provides guidance for creating effective Junie agent skills.

## About Skills

Skills are modular, self-contained folders that extend Junie's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Junie from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

Skills follow the open [Agent Skills](https://agentskills.io/specification) format and are portable across agents.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, templates, and checklists for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a shared resource. Skills share it with everything else Junie needs: system prompt, conversation history, other skills' metadata, and the actual user request.

**Default assumption: Junie is already very smart.** Only add context Junie doesn't already have. Challenge each piece of information: "Does Junie really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Junie as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Skill Location

Junie CLI looks for skill folders in two locations:

1. **Project scope**: `<projectRoot>/.junie/skills/<skill-name>/`
   - Available only in the current project
   - Can be checked into version control and shared across all team members
   - Takes precedence over user-level skills with the same name

2. **User scope**: `~/.junie/skills/<skill-name>/` (macOS/Linux) or `%USERPROFILE%\.junie\skills\<skill-name>\` (Windows)
   - Available globally across all projects on your machine
   - Private to your user account

### Anatomy of a Skill

Every skill consists of a required `SKILL.md` file and optional bundled resources:

```
skill-name/
├── SKILL.md              # Required: Main skill documentation
├── scripts/              # Optional: Executable scripts Junie can run
├── templates/            # Optional: Code or doc templates
└── checklists/           # Optional: Detailed step-by-step checklists
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` (required) and `description` (recommended) fields. These are the only fields Junie reads to determine when the skill gets used, so be clear and comprehensive in describing what the skill is and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded after the skill triggers.

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context

##### Templates (`templates/`)

Boilerplate code or document templates Junie can use as starting points.

- **When to include**: When Junie should scaffold files from a known template
- **Examples**: `templates/component.kt` for Kotlin component scaffolding, `templates/endpoint.kt` for REST endpoint boilerplate
- **Benefits**: Consistent output, reduces repetition

##### Checklists (`checklists/`)

Step-by-step verification lists for complex processes.

- **When to include**: For multi-step workflows where completeness matters
- **Examples**: `checklists/review.md` for code review checklists, `checklists/deployment.md` for deployment verification
- **Benefits**: Ensures nothing is missed, loaded only when needed

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for Junie to do the job at hand. It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a progressive loading system to manage context efficiently:

1. **Metadata (name + description)** - Always available to Junie for skill matching
2. **SKILL.md body** - Loaded when the skill triggers
3. **Bundled resources** - Loaded as needed by Junie (scripts can be executed without reading into context)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details into separate files in `checklists/`, `templates/`, or `scripts/`.

**Pattern 1: High-level guide with checklists**

```markdown
# Code Review

## Quick start
[core instructions]

## Detailed checklists
- **Kotlin review**: See `checklists/kotlin.md` for language-specific checks
- **Security review**: See `checklists/security.md` for security-focused review
```

Junie loads the specific checklist file only when needed.

**Pattern 2: Domain-specific organization**

For skills with multiple domains, organize content by domain:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── checklists/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

When a user asks about sales metrics, Junie only reads `checklists/sales.md`.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md.
- **Structure longer files** - For files longer than 100 lines, include a table of contents at the top.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, templates, checklists)
3. Create the skill folder and SKILL.md
4. Edit the skill (implement resources and write SKILL.md)
5. Validate the skill
6. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Skill Naming

- Use lowercase letters, digits, and hyphens only; normalize user-provided titles to hyphen-case (e.g., "Plan Mode" -> `plan-mode`).
- Keep names under 64 characters (letters, digits, hyphens).
- Prefer short, verb-led phrases that describe the action.
- Namespace by tool when it improves clarity or triggering (e.g., `gh-address-comments`, `linear-address-issue`).
- Name the skill folder exactly after the skill name.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building a `code-review` skill, relevant questions include:

- "What should the code-review skill check? Style, security, performance?"
- "Can you give examples of code patterns we want to enforce?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, templates, and checklists would be helpful when executing these workflows repeatedly

Example: When building a `code-review` skill, the analysis shows:

1. Code review requires checking the same patterns repeatedly
2. A `checklists/kotlin.md` file with Kotlin-specific review items would be helpful

Example: When designing a `component-scaffolding` skill for queries like "Create a new Flutter widget", the analysis shows:

1. Creating widgets requires the same boilerplate each time
2. A `templates/widget.dart` template would be helpful to store in the skill

Example: When building a `database-migration` skill, the analysis shows:

1. Migration scripts follow a standard pattern
2. A `scripts/generate_migration.py` script would be helpful

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, templates, and checklists.

### Step 3: Creating the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists. In this case, continue to the next step.

When creating a new skill from scratch:

1. Create a skill folder under `.junie/skills/` (project scope) or `~/.junie/skills/` (user scope)
2. Add a `SKILL.md` file to the skill folder
3. (Optional) Add supporting subdirectories: `scripts/`, `templates/`, `checklists/`

```
.junie/skills/my-new-skill/
├── SKILL.md
├── scripts/
├── templates/
└── checklists/
```

After creating the folder structure, customize the SKILL.md and add resources as needed.

### Step 4: Edit the Skill

When editing the skill, remember that the skill is being created for Junie to use. Include information that would be beneficial and non-obvious to Junie. Consider what procedural knowledge, domain-specific details, or reusable resources would help Junie execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `templates/`, and `checklists/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `templates/`, or documentation to store in `checklists/`.

Added scripts must be tested by actually running them to ensure there are no bugs and that the output matches what is expected. If there are many similar scripts, only a representative sample needs to be tested.

Only create resource directories that are actually required. Delete any placeholder files that are not needed.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name` (required): A unique identifier for the skill. Use hyphen-case.
- `description` (recommended): A short summary that Junie CLI uses to determine the skill's relevance to the current task.
  - Include both what the skill does and specific triggers/contexts for when to use it.
  - Include all "when to use" information here — not in the body. The body is only loaded after triggering.
  - If `description` is omitted, Junie CLI extracts the first paragraph of the body content. For best results, always provide an explicit `description`.
  - Example: "Code review skill for Kotlin projects. Use when reviewing pull requests, checking for null safety issues, naming violations, and common anti-patterns in Kotlin code."

Do not include any other fields in YAML frontmatter.

##### Body

Write instructions for using the skill and its bundled resources. Follow the recommended structure:

```markdown
---
name: my-skill-name
description: A short description of what this skill provides
---

# My Skill Name

Use this skill when [describe when Junie should use this skill].

## Key Principles
- Principle 1
- Principle 2

## Guidelines
- Guideline 1
- Guideline 2

## Examples

[Include code examples, patterns, or references to project files]

## Checklist

See `checklists/review.md` for a detailed checklist.
```

### Step 5: Validate the Skill

Once development of the skill is complete, validate the skill folder to catch basic issues early:

```bash
python scripts/quick_validate.py <path/to/skill-folder>
```

The validation script checks YAML frontmatter format, required fields, and naming rules. If validation fails, fix the reported issues and run the command again.

Alternatively, ask Junie to list its available skills to confirm the skill loaded correctly.

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Best Practices

- **Be specific and actionable** — Provide as many details as possible. Avoid vague instructions like "Write good tests." Instead, prefer: "Use the AAA pattern (Arrange, Act, Assert). One assertion concept per test."
- **Include examples** — Show the exact patterns you want Junie to follow. Skills with code examples are significantly more effective.
- **Reference project files** — Point Junie to existing code that exemplifies the desired patterns: `See src/test/kotlin/MyServiceTest.kt for a reference test implementation.`
- **Keep it focused** — Each skill should cover one domain or concern. Don't create a single monolithic skill that covers everything.
- **Use subdirectories for complex skills** — If a skill has extensive documentation, break it into multiple files. Main `SKILL.md` provides an overview and links to sub-documents in `checklists/`, `scripts/`, or `templates/`.
- **Write a clear description** — The `description` field is what Junie uses to decide whether a skill is relevant. Provide an explicit `description` so Junie can match the skill to the right tasks without ambiguity.
- **Review external skills carefully** — Junie modifies your code and executes scripts. Only use skills from sources you trust. Read the `SKILL.md` file and all supporting files carefully.
