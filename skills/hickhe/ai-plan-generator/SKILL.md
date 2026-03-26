---
name: ai-plan-generator
description: Converts Code Archaeology analysis results into AI-executable development task lists with focus on business functionality decomposition rather than language-specific implementation.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📋","os":["darwin","linux","win32"],"requires":{"bins":["python","git","bash"]}}}
---

# AI Plan Generator

AI Plan Generator converts Code Archaeology analysis results into structured, AI-executable development task lists. It focuses on **business functionality decomposition** rather than language-specific implementation details, enabling flexible execution across different programming languages and frameworks.

## Core Philosophy

### Language-Agnostic Task Generation
- **Business logic is universal**: Business rules and workflows are independent of programming languages
- **Implementation flexibility**: AI agents can implement tasks in any language based on user requirements  
- **Focus on what, not how**: Tasks describe business functionality, not technical implementation details

### Business-Centric Task Decomposition
- **Medium-granularity tasks**: Each task represents a specific business function (e.g., "submit approval", "update customer info")
- **Complete business context**: Each task includes full business domain context for AI understanding
- **Clear validation criteria**: Success criteria based on business requirements, not technical specifications

## Priority Strategy

### Phase-Based Execution Order
1. **Phase 1: Core Business Functionality** (Highest Priority)
   - Business-critical operations that deliver immediate value
   - Examples: contract creation, customer updates, payment processing
   
2. **Phase 2: Infrastructure and Architecture** (Medium Priority)  
   - Foundational components that support business functionality
   - Examples: multi-tenant middleware, authentication systems, caching mechanisms

3. **Phase 3: Security Vulnerability Inventory** (Lowest Priority)
   - Complete security vulnerability inventory for risk assessment
   - Actual security fixes executed last to avoid blocking business delivery

## Input Processing

### Code Archaeology Results Structure
The skill processes analysis results from the following directory structure:
```
analysis_directory/
├── domains/
│   ├── contract_management.analysis.md    # Business rules and analysis
│   ├── contract_management.flows.json     # Business workflows and state transitions  
│   ├── contract_management.model.json     # Data models and entity relationships
│   └── [other business domains...]
├── memory/
│   ├── FINDINGS.jsonl                    # Security vulnerabilities (if available)
│   └── STATE.json                        # Analysis metadata
└── progress/
    └── PROGRESS.md                       # Analysis progress tracking
```

### Business Function Extraction
From each business domain, the skill extracts:
- **Core operations**: create, update, delete, view, submit, approve, reject, complete
- **Business workflows**: State transitions and process flows from `.flows.json`
- **Business rules**: Validation rules and constraints from `.analysis.md`
- **Data models**: Entity relationships and attributes from `.model.json`

## Output Formats

### Markdown Format (Primary)
- **Human-readable task list** suitable for review and collaboration
- **Organized by priority phases** with clear business function descriptions
- **Complete business context** for each task including rules and workflows
- **Vulnerability inventory** as a separate reference section

### JSON Format (Backup)  
- **Machine-processable structure** for automated execution
- **Standardized task objects** with consistent fields and formats
- **Task dependencies and relationships** for proper execution ordering
- **Validation criteria** for automated quality assurance

## Task Structure

Each generated task includes:

### Task Metadata
- **Task ID**: Unique identifier following `module_function_sequence` pattern
- **Task Type**: `feature_implementation`, `infrastructure_setup`, or `security_fix`
- **Priority**: `critical`, `high`, `medium`, or `low`
- **Phase**: `1` (core business), `2` (infrastructure), or `3` (security)

### Business Context
- **Business Rules**: Complete list of relevant business rules (language-agnostic)
- **Business Workflows**: State transitions and process flows
- **Data Models**: Entity relationships and key attributes
- **Validation Criteria**: Business-focused success criteria

### Implementation Guidelines
- **Business Function Description**: Clear description of what the task should accomplish
- **Input/Output Specifications**: Business-level data requirements (not technical formats)
- **Dependencies**: Other tasks that must be completed first
- **Quality Standards**: Business-focused validation criteria

## Usage Examples

### Basic Invocation
```
Generate AI-executable development plan from Code Archaeology results in /path/to/analysis/directory
```

### Natural Language Flexibility
The skill works with any target language or framework because it focuses on business functionality:
- User says: "Rebuild this in Java" → AI agents implement tasks in Java
- User says: "Convert to Python" → AI agents implement tasks in Python  
- User says: "Modernize with Node.js" → AI agents implement tasks in Node.js

The AI Plan Generator provides the **what** (business functionality), while AI agents determine the **how** (technical implementation).

## Integration with AI Development Tools

This skill integrates seamlessly with:
- **Code Archaeology**: Direct input processing from Code Archaeology results
- **ClawTeam**: Generated tasks can be executed by ClawTeam multi-agent teams
- **AI Development Agents**: Tasks are structured for direct AI agent consumption
- **Project Management Tools**: JSON output can integrate with external PM systems

## Best Practices

- **Review Before Execution**: Always review the generated markdown plan before AI execution
- **Business Context Preservation**: Maintain complete business context to ensure AI understanding  
- **Priority Adherence**: Follow the three-phase priority structure for optimal results
- **Language Flexibility**: Leverage the language-agnostic nature for maximum implementation flexibility