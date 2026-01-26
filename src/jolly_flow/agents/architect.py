from langchain_core.messages import SystemMessage
from .state import ProjectState
from .models import get_model
from pathlib import Path
import importlib.resources as pkg_resources

def architect_agent(state: ProjectState, model_id: str):
    model = get_model(model_id)
    project_path = Path(state["project_path"])
    
    # 1. Read Requirements
    requirements_path = project_path / "REQUIREMENTS.md"
    requirements_content = ""
    if requirements_path.exists():
        with open(requirements_path, "r") as f:
            requirements_content = f.read()
    else:
        requirements_content = "No requirements document found."

    # 2. Read Templates
    try:
        arch_template = pkg_resources.files("jolly_flow.templates").joinpath("ARCHITECTURE.md.template").read_text(encoding="utf-8")
        tech_template = pkg_resources.files("jolly_flow.templates").joinpath("TECH-STACK.md.template").read_text(encoding="utf-8")
    except Exception as e:
        arch_template = "Error reading ARCHITECTURE.md.template"
        tech_template = "Error reading TECH-STACK.md.template"

    # 3. Build Prompt
    system_prompt = (
        "You are the System Architect for The Jolly Method. "
        "Your goal is to design the system architecture based on the provided requirements through an INTERACTIVE CONVERSATION.\n\n"
        "## RULES OF ENGAGEMENT:\n"
        "1. **Analyze First.** Read the requirements silently.\n"
        "2. **Discuss Options.** Propose 2-3 high-level approaches (e.g., Stack choices, Patterns). Ask the user which they prefer.\n"
        "3. **One Step at a Time.** Do not overwhelm the user with 50 questions.\n"
        "4. **Generate ONLY when ready.** When the user has agreed on the approach, generate the full 'ARCHITECTURE.md' and 'TECH-STACK.md' using the templates below.\n\n"
        f"---\nPROJECT CONTEXT:\n{state.get('ai_context', 'No context available')}\n\n"
        f"---\nEXISTING REQUIREMENTS:\n{requirements_content}\n\n"
        f"---\nTEMPLATE: ARCHITECTURE.md\n{arch_template}\n\n"
        f"---\nTEMPLATE: TECH-STACK.md\n{tech_template}"
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
