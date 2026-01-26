# The Workflow

The Jolly Method follows a strict "Ask, Plan, Build" lifecycle. This ensures you don't start coding until you know exactly what you're building.

## 1. Scaffold (`new-project`)

Every idea starts with a folder.

```bash
jolly-flow new-project "My SaaS Idea"
```

**What it does:**
- Creates a private **Vault** in `~/GoogleDrive/Obsidian/JollyProjects/`.
- Creates a public **Code Repo** in `~/GoogleDrive/Projects/`.
- Initializes `git` in both locations.
- Prepares `AI-CONTEXT.md` to track state.

## 2. The Interview Phase (`generate`)

This is the core of the method. You don't write documents; you answer questions.

### Step A: Requirements
**Goal:** Define *what* to build.

```bash
jolly-flow generate-requirements
```

**The Agent asks:**
- Who is this for?
- What problem does it solve?
- What are the "must-have" features?

**Result:** `REQUIREMENTS.md`

### Step B: Architecture
**Goal:** Define *how* to build it.

```bash
jolly-flow generate-architecture
```

**The Agent asks:**
- Which database fits the data model?
- Monolith or Microservices?
- Cloud or On-prem?

**Result:** `ARCHITECTURE.md` and `TECH-STACK.md`

### Step C: Roadmap
**Goal:** Define *when* to build it.

```bash
jolly-flow generate-roadmap
```

**The Agent asks:**
- What is the MVP?
- What can wait for v2?

**Result:** `ROADMAP.md` (Phased plan)

## 3. Implementation Phase (`start-phase`)

You build the project one phase at a time.

```bash
jolly-flow start-phase 1
```

**What it does:**
- Reads the Roadmap.
- Generates a detailed `checklist.md` for Phase 1.
- Generates an `implementation-guide.md` with specific commands and code snippets tailored to your Architecture.

## 4. Observability (Optional)

If you have configured LangSmith, you can see exactly what the agents "thought" during the interview process by logging into your LangSmith dashboard.
