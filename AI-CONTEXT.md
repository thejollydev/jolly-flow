# AI Context - The Jolly Method Project

**Last Updated:** 2026-01-21
**Project:** The Jolly Method Framework
**Current Phase:** Phase 0 Complete → Starting Phase 1

---

## Project Status

**What is this project?**
Building "The Jolly Method" - a subscription-first, LangGraph-orchestrated AI project framework.

**Current state:**
- ✅ Phase 0 (Design & Planning) - COMPLETE
- 🔄 Phase 1 (Core Infrastructure) - NEXT
- ⏳ Phases 2-10 - Pending

**Repository locations:**
- Code: `/home/joseph/GoogleDrive/Projects/the-jolly-method/`
- Framework vault: `/home/joseph/GoogleDrive/Obsidian/TheJollyMethod/`
- Projects vault: `/home/joseph/GoogleDrive/Obsidian/JollyProjects/`

---

## What's Been Accomplished

### Phase 0: Foundation & Design ✅
1. Researched 6 different LLMs for recommendations
2. Synthesized Claude + Gemini sessions
3. Finalized architecture:
   - Subscription-first model (Claude Pro + Google AI Pro)
   - CLIProxyAPI as unified model gateway
   - LangGraph for orchestration with human-in-the-loop
   - Open WebUI + Cline for interfaces
   - Manual model selection to avoid quota exhaustion
4. Created vault structures:
   - TheJollyMethod (framework docs, templates)
   - JollyProjects (project planning)
5. Created project folder: `~/GoogleDrive/Projects/the-jolly-method/`
6. Generated documentation:
   - README.md
   - ROADMAP.md (10 phases)
   - ARCHITECTURE.md (complete system design)
   - This AI-CONTEXT.md file

---

## Next Steps (Phase 1)

**Phase 1: Core Infrastructure** - Install and configure all components

### High Priority:
1. **Install CLIProxyAPI**
   - Clone repository
   - Configure claude-code CLI
   - Configure gemini-cli
   - Add ollama models
   - Test API endpoints

2. **Set up Open WebUI**
   - Install via Docker
   - Configure CLIProxyAPI as provider
   - Test model switching

3. **Configure Cline**
   - Install extension in VS Code
   - Point to CLIProxyAPI
   - Test file access to vaults

4. **Install AionUi** (Optional)
   - For beautiful native UI

**Success criteria for Phase 1:**
- All models accessible from Cline and Open WebUI
- Can switch between Claude, Gemini, and Ollama
- Subscription limits work (not API costs)

---

## Open Questions

*None at this time - all design questions resolved*

---

## Decisions Made

### Key Architectural Decisions:
1. **Subscription-first billing** - Use Claude Pro + Google AI Pro ($40/mo fixed)
2. **CLIProxyAPI** - Wrap claude-code, gemini-cli, ollama as unified API
3. **LangGraph only** - No CrewAI (too black box)
4. **Manual model selection** - User chooses model per agent to control quotas
5. **Context continuity** - AI-CONTEXT.md passed between all agents
6. **Open WebUI for planning** - Better than LM Studio (Ollama support, pipelines)
7. **Cline for coding** - VS Code extension with file access
8. **Three vaults** - TheJollyMethod (framework), JollyProjects (projects), ai-vault (archive)

### Tech Stack:
- **Orchestration:** LangGraph
- **Model Gateway:** CLIProxyAPI
- **Planning UI:** Open WebUI
- **Coding UI:** Cline (VS Code)
- **CLI Tool:** jolly-flow (custom Python)
- **Local Models:** Ollama
- **Observability:** LangSmith (free tier)

---

## Recent Changes

**2026-01-21:**
- Created all vault structures
- Created project folder structure
- Generated README, ROADMAP, ARCHITECTURE docs
- Finalized all design decisions
- Ready to begin implementation

---

## For LLM Agents

**If you're working on this project:**

1. **Read this file FIRST** to understand current state
2. **Check ROADMAP.md** to see what phase we're in
3. **Reference ARCHITECTURE.md** for system design details
4. **Follow standards** from TheJollyMethod/standards/ (when created)
5. **Update this file** after completing any tasks

**Current focus:** Phase 1 - Core Infrastructure Setup

**Models to use:**
- Planning/design: Claude Opus 4.5 or Gemini 3 Pro
- Code implementation: Any model (switch based on quota)
- Code review: Use different model than primary (cross-check)

---

## Known Issues

*None yet - project just started*

---

## Resources

**Documentation:**
- [ROADMAP.md](ROADMAP.md) - Implementation phases
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [README.md](README.md) - Public-facing overview

**External Links:**
- CLIProxyAPI: https://github.com/router-for-me/CLIProxyAPI
- Open WebUI: https://github.com/open-webui/open-webui
- Cline: https://github.com/cline/cline
- LangGraph: https://github.com/langchain-ai/langgraph

**Design Documents (ai-vault):**
- `/home/joseph/GoogleDrive/Obsidian/ai-vault/current-docs/`

---

**Status:** ✅ Foundation complete, ready to build!
