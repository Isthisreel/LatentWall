---
name: NotebookLM Deep Research
description: Query connected NotebookLM MCP to extract data and generate code based on research
---

# NotebookLM Deep Research Skill

## Purpose

This skill enables **AI-powered research** by querying your NotebookLM notebooks to extract information, find implementation patterns, and generate code based on comprehensive documentation without consuming excessive tokens.

## Triggers

- Need to understand a new technology or API
- User asks "how to" implement something
- Looking for code examples or patterns
- Need to verify feature availability
- User mentions "research", "documentation", "notebook"
- Starting work with unfamiliar API (like Odyssey ML)

## Available Notebooks

### Odyssey ML dev
**Notebook ID**: 

**Sources** (16 total):
- Odyssey API documentation
- Python SDK reference
- AntiGravity tutorials (YouTube)
- Implementation patterns
- Error handling guides

**Use for**:
- Odyssey API questions
- SDK method signatures
- Video generation patterns
- Troubleshooting Odyssey errors

## Execution Checklist

### Phase 1: Research Planning
- [ ] **Define Question**: What specific information do you need?
- [ ] **Identify Notebook**: Which notebook contains relevant sources?
- [ ] **Formulate Query**: Create precise, focused question
- [ ] **Verify Context**: What have you already tried?

### Phase 2: Query Execution
- [ ] **Query Notebook**: Use `mcp_notebook-lm_notebook_query` tool
- [ ] **Extract Key Info**: Identify relevant patterns/examples
- [ ] **Validate Accuracy**: Cross-reference with multiple sources
- [ ] **Note Citations**: Track which sources provided info

### Phase 3: Application
- [ ] **Adapt to Context**: Modify examples for current project
- [ ] **Verify Compatibility**: Check versions, dependencies
- [ ] **Implement Pattern**: Apply research findings
- [ ] **Document Source**: Note where info came from

### Phase 4: Validation
- [ ] **Test Implementation**: Does it work as documented?
- [ ] **Handle Edge Cases**: What wasn't in the docs?
- [ ] **Update Knowledge**: If docs are wrong, note corrections
- [ ] **Share Findings**: Update project docs with learnings

## Patterns & Examples

### Pattern 1: Feature Verification Query

```python
# Question: "Does Odyssey SDK support image-to-video?"

# Query NotebookLM
response = await mcp_notebook-lm_notebook_query(
    notebook_id="f1b09888-005d-444f-8a4f-0db1a2fc1929",
    query="""
    Does Odyssey SDK support image-to-video generation? 
    Provide specific code examples, parameter names, and 
    method signatures that prove this capability exists.
    """
)

# Result: Verified with exact signatures
# start_stream(prompt, image="/path/to/image.jpg")
```

### Pattern 2: Implementation Pattern Query

```python
# Question: "How to handle Odyssey errors?"

response = await mcp_notebook-lm_notebook_query(
    notebook_id="f1b09888-005d-444f-8a4f-0db1a2fc1929",
    query="""
    What are best practices for error handling with Odyssey SDK?
    Include specific exception types, retry logic, and 
    resource cleanup patterns.
    """
)

# Extract patterns and implement in code
```

### Pattern 3: Batch Research Query

```python
# Multiple related questions

queries = [
    "What are the exact method signatures for Odyssey Python SDK?",
    "What are the limitations of the Odyssey SDK?",
    "Show working code examples from the documentation"
]

results = []
for query in queries:
    response = await mcp_notebook-lm_notebook_query(
        notebook_id="f1b09888-005d-444f-8a4f-0db1a2fc1929",
        query=query
    )
    results.append(response)

# Synthesize findings
```

### Pattern 4: Describe Source

```python
# Get AI summary of a specific source

response = await mcp_notebook-lm_source_describe(
    source_id="54f98d0e-a762-4bb6-973f-45891dbf9f24"
)

# Returns: summary with keywords
print(response['summary'])
print(response['keywords'])
```

## Query Best Practices

### ✅ Good Queries (Specific & Actionable)

```
"What are the EXACT method names and signatures for the Odyssey 
Python SDK? Include start_stream, simulate, connect, disconnect 
with actual parameters and return types."
```

```
"Does Odyssey SDK support image-to-video generation? Provide 
specific code examples, parameter names, and method signatures 
that prove this capability exists."
```

```
"What are the known limitations, constraints, and requirements 
of the Odyssey SDK? What doesn't work or what are common issues?"
```

### ❌ Bad Queries (Vague & Generic)

```
"Tell me about Odyssey"
```

```
"How does the SDK work?"
```

```
"Explain everything"
```

## Anti-Patterns

❌ **DON'T** assume features exist without verification
```python
# BAD: Just guessing the API exists
await client.transform_video()  # Does this exist?
```

✅ **DO** verify with NotebookLM first
```python
# GOOD: Query notebook to verify
response = await query_notebook("Does Odyssey have transform_video method?")
# Result: No, it doesn't. Use simulate API instead.
```

❌ **DON'T** make up code examples
```python
# BAD: Fabricated example
client.generate(prompt="cat", style="anime", duration=60)
# Parameters might not exist!
```

✅ **DO** use verified examples from docs
```python
# GOOD: From NotebookLM query
await client.start_stream(
    prompt="cat",
    portrait=True,
    image="/path/to/image.jpg"
)
# Verified parameters from actual docs
```

❌ **DON'T** query for general knowledge
```python
# BAD: Google-able information
query = "What is Python asyncio?"
```

✅ **DO** query for project-specific info
```python
# GOOD: Specific to your notebooks
query = "How does Odyssey SDK use asyncio? Show patterns."
```

## Integration

### With Planning Skill
- Research technology before creating implementation plan
- Verify features exist before designing architecture
- Find reference implementations from docs

### With Troubleshooting Skill
- Query for error codes and solutions
- Find debugging patterns from documentation
- Verify expected behavior vs actual behavior

### With Brand Design Skill
- Research design inspiration from saved sources
- Find UI/UX patterns that match brand
- Extract color schemes from examples

### With Odyssey ML
- All Odyssey implementation should query notebook first
- Verify method signatures before writing code
- Check for limitations and constraints

## Research Workflow

### Scenario: Implementing New Feature

```markdown
1. **Define Goal**: "Implement batch video generation"

2. **Research Questions**:
   - Does Odyssey support batch operations?
   - What is the API for batch processing?
   - Are there code examples?
   - What are the limits (concurrent jobs, etc.)?

3. **Query Notebook**:
   ```python
   query = "Explain Odyssey simulate API for batch processing"
   ```

4. **Extract Patterns**:
   - SimulationScript format
   - Job status polling
   - Result retrieval

5. **Implement**:
   - Create SimulationManager class
   - Use patterns from docs
   - Add error handling from research

6. **Validate**:
   - Test against documented behavior
   - Handle edge cases not in docs
   - Document any discrepancies
```

## NotebookLM MCP Tools

### Core Tools

```python
# List notebooks
await mcp_notebook-lm_notebook_list(max_results=100)

# Get notebook details
await mcp_notebook-lm_notebook_get(notebook_id="...")

# Query notebook
await mcp_notebook-lm_notebook_query(
    notebook_id="...",
    query="Your question",
    source_ids=None  # Optional: specific sources
)

# Get AI summary
await mcp_notebook-lm_notebook_describe(notebook_id="...")

# Describe source
await mcp_notebook-lm_source_describe(source_id="...")

# Get source content
await mcp_notebook-lm_source_get_content(source_id="...")
```

### Advanced Research

```python
# Add new sources
await mcp_notebook-lm_notebook_add_url(
    notebook_id="...",
    url="https://docs.example.com"
)

# Generate study guides
await mcp_notebook-lm_report_create(
    notebook_id="...",
    report_format="Study Guide",
    confirm=True
)

# Create flashcards
await mcp_notebook-lm_flashcards_create(
    notebook_id="...",
    difficulty="medium",
    confirm=True
)
```

## Research Checklist

Before implementing anything new:

- [ ] Have you queried NotebookLM for documentation?
- [ ] Have you verified the feature actually exists?
- [ ] Have you found code examples from official sources?
- [ ] Have you checked for limitations or constraints?
- [ ] Have you noted any version requirements?
- [ ] Have you found error handling patterns?
- [ ] Have you documented sources in code comments?

## Documentation Citation

When using research in code:

```python
# Source: Odyssey ML dev notebook, query 2026-01-29
# Feature: Image-to-video generation
# Verified: start_stream() supports image parameter
# Formats: JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF, AVIF
# Max size: 25 MB
async def generate_from_image(image_path: str, prompt: str):
    await client.start_stream(
        prompt=prompt,
        image=image_path
    )
```

---

**Remember**: "Research first, code second. Verify everything."
