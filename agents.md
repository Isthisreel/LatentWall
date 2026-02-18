# Anti-Gravity Framework: 3-Layer Architecture

> **Version**: Pro Configuration v1.0  
> **Last Updated**: 2026-01-29  
> **Architecture Paradigm**: Directive → Orchestration → Execution

---

## 🎯 Layer 1: Directive (Strategic Intent)

**Purpose**: Define project goals, inputs, and strategic parameters that guide the entire system.

### Core Responsibilities
- **Goal Definition**: Articulate high-level objectives and desired outcomes
- **Input Specification**: Define what data, context, and resources enter the system
- **Constraint Management**: Establish boundaries, requirements, and success criteria
- **Strategic Alignment**: Ensure all downstream activities align with business objectives

### Key Components
- Project vision and mission statements
- User requirements and acceptance criteria
- Performance targets and KPIs
- Budget and resource constraints
- Timeline and milestone definitions

---

## 🧠 Layer 2: Orchestration (Intelligent Coordination)

**Purpose**: Serve as the intelligent agent that interprets directives, manages task decomposition, and coordinates execution.

### Agent Responsibilities
- **Directive Interpretation**: Parse Layer 1 goals into actionable task sequences
- **Task Decomposition**: Break complex objectives into manageable execution units
- **Resource Allocation**: Assign appropriate tools, skills, and strategies to tasks
- **Quality Assurance**: Monitor execution and validate outputs against directives
- **Adaptive Planning**: Adjust strategies based on execution feedback and changing conditions

### Orchestration Protocols
1. **Intake Protocol**: Receive and validate directives from Layer 1
2. **Planning Protocol**: Generate execution roadmaps with clear milestones
3. **Dispatch Protocol**: Assign tasks to Layer 3 execution units with precise instructions
4. **Monitoring Protocol**: Track progress and collect execution telemetry
5. **Validation Protocol**: Ensure outputs meet Layer 1 acceptance criteria

### Available Tools (Skills Library)

The Orchestration Layer has access to specialized skills stored in `.agent/skills/`. Each skill provides domain-specific capabilities that the agent can leverage to accomplish tasks.

#### Core Skills

1. **[Skill Creator](file:///.agent/skills/skill-creator/SKILL.md)** (Meta-Skill)
   - Creates new skills following standardized format
   - Ensures consistency across skill library
   - Defines format: YAML frontmatter, triggers, checklists, patterns

2. **[Brand Design System](file:///.agent/skills/brand-design/SKILL.md)**
   - Enforces visual consistency across all UI components
   - Provides design tokens: colors, typography, spacing, effects
   - Prevents ad-hoc styling that breaks brand identity
   - Auto-triggers on: UI creation, styling tasks, image generation

3. **[Brainstorming & Planning](file:///.agent/skills/brainstorming-planning/SKILL.md)**
   - Forces structured planning before coding
   - Breaks complex tasks into architectural steps
   - Prevents "code-first" mistakes and technical debt
   - Auto-triggers on: Complex features, new systems, major refactoring

4. **[Troubleshooting & Error Handling](file:///.agent/skills/troubleshooting/SKILL.md)**
   - Systematic debugging methodology
   - Error handling patterns (try/catch, logging, retry logic)
   - Fixes bugs efficiently and prevents recurrence
   - Auto-triggers on: Errors, bugs, failing tests, unexpected behavior

5. **[NotebookLM Deep Research](file:///.agent/skills/notebooklm-research/SKILL.md)**
   - Queries connected NotebookLM notebooks for documentation
   - Extracts implementation patterns and code examples
   - Verifies feature availability before coding
   - Auto-triggers on: New technology, "how to" questions, API research
   - **Connected Notebooks**:
     - Odyssey ML dev (`f1b09888-005d-444f-8a4f-0db1a2fc1929`)

6. **[Script Runner & Automation](file:///.agent/skills/automation/SKILL.md)**
   - Executes Python scripts directly within environment
   - Automates testing, validation, and batch operations
   - Safety-first approach (SafeToAutoRun flag)
   - Auto-triggers on: Script execution, automation, batch tasks

7. **[Odyssey ML SDK](file:///.agent/skills/odyssey-ml/SKILL.md)** (Domain-Specific)
   - Expert guidance for Odyssey video generation API
   - Streaming, simulation, and headless processing patterns
   - Image-to-video, batch generation, recording management
   - Auto-triggers on: Video generation, Odyssey API usage

#### Skill Selection Logic

The agent automatically:
- **Detects triggers**: Keywords, code patterns, task context
- **Loads relevant skills**: Multiple skills can be composed together
- **Follows checklists**: Executes step-by-step processes from skills
- **Applies patterns**: Uses verified code examples from skills
- **Avoids anti-patterns**: Prevents common mistakes documented in skills

#### Skill Composition Examples

**Example 1**: Building a video dashboard
- Planning Skill: Create architecture and task breakdown
- Brand Design Skill: Apply design tokens to UI
- Odyssey ML Skill: Implement video generation logic
- Troubleshooting Skill: Add error handling patterns

**Example 2**: Researching new API
- NotebookLM Skill: Query documentation notebook
- Planning Skill: Create implementation plan based on research
- Troubleshooting Skill: Add error handling for API errors
- Automation Skill: Create test scripts to validate integration

---

## ⚙️ Layer 3: Execution (Code & Output Generation)

**Purpose**: Generate actual code files, documentation, and deliverables as specified by Layer 2 orchestration.

### Execution Characteristics
- **Deterministic Output**: Code and files produced according to precise specifications
- **Quality Standards**: All outputs adhere to established coding standards and best practices
- **Artifact Generation**: Produce structured, versioned, and documented deliverables
- **Performance Optimization**: Efficient execution with minimal resource waste

### Output Types
- Application source code
- Configuration files
- Documentation and specifications
- Test suites and validation scripts
- Deployment artifacts
- Data pipelines and processing scripts

---

## 🔄 Self-Annealing Protocol (Self-Healing System)

> [!CAUTION]
> **STRICT RULE**: If an error is encountered during execution, the system MUST automatically analyze the error, propose a fix, and retry the execution without waiting for user prompting.

### Self-Healing Workflow

1. **Error Detection**
   - Capture all execution errors with full stack traces
   - Log error context including input parameters, system state, and environment

2. **Automated Analysis**
   - Parse error messages and identify root cause
   - Cross-reference against known error patterns and solutions
   - Classify error severity (recoverable vs. critical)

3. **Solution Generation**
   - Propose specific fix based on error analysis
   - Generate corrected code or configuration
   - Document the proposed change

4. **Automatic Retry**
   - Apply the proposed fix
   - Re-execute the failed operation
   - Validate the outcome

5. **Escalation (if needed)**
   - If retry fails after 3 attempts, log detailed diagnostics
   - Notify user with comprehensive error report and recommendations
   - Preserve system state for manual intervention

### Self-Annealing Best Practices
- **Fail Fast**: Detect errors immediately, don't propagate bad state
- **Log Everything**: Maintain detailed audit trails of all self-healing actions
- **Learn Patterns**: Build knowledge base of common errors and solutions
- **Validate Fixes**: Always verify that the fix resolves the issue without side effects
- **User Transparency**: Keep user informed of self-healing actions taken

---

## 📋 Architecture Governance

### Separation of Concerns
- **Layer 1** defines "WHAT" and "WHY"
- **Layer 2** determines "HOW" and "WHEN"
- **Layer 3** implements "THE ACTUAL WORK"

### Information Flow
```
Directive → Orchestration → Execution
   ↓             ↓              ↓
Goals      Task Plans      Deliverables
   ↑             ↑              ↑
Feedback ← Validation ← Monitoring
```

### Quality Gates
- Each layer validates inputs from the previous layer
- Execution outputs are validated against orchestration specifications
- Orchestration plans are validated against directives
- Continuous feedback loop ensures alignment

---

## 🛠️ Integration with Project Structure

### Directory Mapping
- **`.agent/skills/`**: Skills library (Orchestration Layer tools)
- **`.agent/workflows/`**: Automated workflows and procedures
- **`.agent/rules.md`**: Project-specific coding standards
- **`context/`**: Project documentation and requirements (Directive Layer storage)
- **`src/`**: Application source code (Execution Layer outputs)
- **`examples/`**: Reference implementations and demos
- **`outputs/`**: Generated artifacts, videos, recordings

### Workflow Example
1. User defines goal: "Build video generation dashboard" (Layer 1)
2. Agent activates Planning Skill, creates `implementation_plan.md` (Layer 2)
3. Agent loads Brand Design and Odyssey ML skills (Layer 2)
4. Agent generates code files in `src/` and UI components (Layer 3)
5. Agent validates outputs, updates `task.md` tracking (Layer 2)
6. If errors occur, Troubleshooting Skill + Self-Annealing Protocol activate

---

**End of Architecture Definition**
