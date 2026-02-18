---
name: Skill Creator
description: Meta-skill for creating standardized skills in the Antigravity environment
---

# Skill Creator - The Mother of All Skills

This is the **meta-skill** that defines how all other skills should be structured and created in this project.

## Purpose

The Skill Creator ensures consistency across all skills by providing a standard format and creation process. When you need to create a new skill, reference this skill first.

## Standard Skill Format

Every skill MUST follow this structure:

### 1. YAML Frontmatter
```yaml
---
name: Skill Name
description: One-line description of what this skill does
---
```

### 2. Purpose Section
Clear statement of what problem this skill solves and when to use it.

### 3. Triggers Section
List of phrases, keywords, or scenarios that should activate this skill.

**Examples:**
- User asks about [specific topic]
- Code contains [specific pattern]
- Task involves [specific technology]

### 4. Checklist Section
Step-by-step process to execute when this skill is triggered.

**Format:**
```markdown
## Execution Checklist

- [ ] Step 1: [Action]
- [ ] Step 2: [Action]
- [ ] Step 3: [Action]
```

### 5. Patterns & Examples
Code snippets, templates, or reference implementations.

### 6. Anti-Patterns
Common mistakes to avoid when using this skill.

### 7. Integration
How this skill works with other skills or workflows.

## Skill Creation Process

When creating a new skill:

### Step 1: Define the Problem
- What recurring task or pattern does this skill address?
- Who will use it? (Developer, AI assistant, automation system)
- What's the success criteria?

### Step 2: Identify Triggers
- What words/phrases should activate this skill?
- What code patterns should trigger it?
- What project states require it?

### Step 3: Create the Checklist
- Break down the skill into atomic steps
- Each step should be actionable
- Include validation points
- Add error handling steps

### Step 4: Add Patterns & Examples
- Provide code templates
- Show before/after examples
- Include edge cases
- Document configuration options

### Step 5: Document Anti-Patterns
- What NOT to do
- Common mistakes
- Performance pitfalls
- Security concerns

### Step 6: Test Integration
- How does it work with existing skills?
- Are there dependencies?
- Can it be composed with other skills?

## Skill Storage

All skills are stored in:
```
.agent/skills/[skill-name]/SKILL.md
```

## Skill Activation

Skills are activated by:
1. **Explicit reference**: User mentions skill by name
2. **Auto-detection**: AI recognizes trigger patterns
3. **Workflow integration**: Workflows call skills
4. **Rules enforcement**: Project rules reference skills

## Quality Checklist

Before finalizing a skill, verify:

- [ ] YAML frontmatter is valid
- [ ] Description is concise and clear
- [ ] Triggers are specific and actionable
- [ ] Checklist has 3-10 steps (not too few, not too many)
- [ ] At least 2 code examples included
- [ ] At least 2 anti-patterns documented
- [ ] Integration section addresses dependencies
- [ ] File is saved in `.agent/skills/[name]/SKILL.md`

## Example Skill Template

```markdown
---
name: Example Skill
description: One-line description
---

# Example Skill

## Purpose
Why this skill exists and when to use it.

## Triggers
- User says "X"
- Code contains pattern Y
- Task involves Z

## Execution Checklist

- [ ] Step 1: Identify the context
- [ ] Step 2: Apply pattern
- [ ] Step 3: Validate result
- [ ] Step 4: Document changes

## Patterns & Examples

### Pattern 1: [Name]
\`\`\`python
# Example code
\`\`\`

### Pattern 2: [Name]
\`\`\`python
# Example code
\`\`\`

## Anti-Patterns

❌ **DON'T**: [Description]
- Reason why
- Better alternative

❌ **DON'T**: [Description]
- Reason why
- Better alternative

## Integration

- Works with: [Skill A], [Skill B]
- Requires: [Dependency]
- Conflicts with: [None]
```

## Usage Examples

### Creating a New Skill

When user says: *"Create a skill for handling API errors"*

**Response:**
1. Reference this Skill Creator
2. Define problem: Consistent error handling across API calls
3. Identify triggers: API calls, error handling, try/catch
4. Create checklist: Detect → Wrap → Log → Return
5. Add patterns: Standard error wrapper, retry logic
6. Document anti-patterns: Silent failures, generic errors
7. Save to `.agent/skills/api-error-handler/SKILL.md`

### Updating Existing Skills

When a skill needs improvement:
1. Review against this standard format
2. Add missing sections
3. Update examples with real project code
4. Ensure integration is documented
5. Validate quality checklist

## Meta-Skill Self-Application

This Skill Creator skill itself follows the format it defines:

✅ Has YAML frontmatter
✅ Clear purpose statement
✅ Defined triggers (skill creation requests)
✅ Execution checklist (skill creation process)
✅ Patterns (skill template)
✅ Anti-patterns (what makes a bad skill)
✅ Integration (how skills work together)

## Continuous Improvement

Skills are living documents. Update them when:
- New patterns are discovered
- Better examples are found
- Anti-patterns are identified
- Integration changes occur
- User feedback is received

---

**Remember**: A great skill is:
- **Specific**: Solves one problem well
- **Actionable**: Clear steps to execute
- **Reusable**: Works across multiple contexts
- **Documented**: Examples and anti-patterns
- **Integrated**: Works with existing systems
