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
        "Your goal is to create a detailed, phased implementation roadmap (ROADMAP.md). "
        "1. Analyze the Requirements and Architecture below. "
        "2. Break the project down into logical phases (e.g., Phase 1: Foundation, Phase 2: MVP Core, etc.). "
        "3. For each phase, list key deliverables and success criteria. "
        "4. Identify any dependencies or risks. "
        "5. Do NOT just generate a generic list. Be specific to the features and tech stack described. "
        "6. IMPORTANT: You MUST follow the exact structure of the provided template below for the final output."
        f"\n\n---\nPROJECT CONTEXT (from AI-CONTEXT.md):\n{state.get('ai_context', 'No context available')}"
        f"\n\n---\nREQUIREMENTS:\n{requirements_content}"
        f"\n\n---\nARCHITECTURE:\n{architecture_content}"
        f"\n\n---\nTEMPLATE: ROADMAP.md\n{roadmap_template}"
    )
    
    # 4. Call Model
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
