from langchain_core.messages import SystemMessage
from .state import ProjectState
from .models import get_model
from pathlib import Path
import importlib.resources as pkg_resources

def planner_agent(state: ProjectState, model_id: str):
    model = get_model(model_id)
    project_path = Path(state["project_path"])
    
    # 1. Read Inputs
    requirements_content = ""
    architecture_content = ""
    
    req_path = project_path / "REQUIREMENTS.md"
    if req_path.exists():
        with open(req_path, "r") as f:
            requirements_content = f.read()
    else:
        requirements_content = "No requirements document found."

    arch_path = project_path / "ARCHITECTURE.md"
    if arch_path.exists():
        with open(arch_path, "r") as f:
            architecture_content = f.read()
    else:
        architecture_content = "No architecture document found."

    # 2. Read Template
    try:
        roadmap_template = pkg_resources.files("jolly_flow.templates").joinpath("ROADMAP.md.template").read_text(encoding="utf-8")
    except Exception as e:
        roadmap_template = "Error reading ROADMAP.md.template"

    # 3. Build Prompt
    system_prompt = (
        "You are the Technical Project Planner for The Jolly Method. "
        "Your goal is to create a detailed implementation roadmap through an INTERACTIVE CONVERSATION.\n\n"
        "## RULES OF ENGAGEMENT:\n"
        "1. **Propose a Strategy.** Based on the Requirements and Architecture, suggest a high-level phasing strategy (e.g., 'Foundation -> MVP -> Polish').\n"
        "2. **Ask for Feedback.** Ask the user if this timeline aligns with their priorities.\n"
        "3. **Refine.** Adjust based on user input.\n"
        "4. **Generate ONLY when ready.** When the strategy is agreed upon, generate the full 'ROADMAP.md' using the template below.\n\n"
        f"---\nPROJECT CONTEXT:\n{state.get('ai_context', 'No context available')}\n\n"
        f"---\nREQUIREMENTS:\n{requirements_content}\n\n"
        f"---\nARCHITECTURE:\n{architecture_content}\n\n"
        f"---\nTEMPLATE: ROADMAP.md\n{roadmap_template}"
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
