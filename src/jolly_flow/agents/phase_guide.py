from langchain_core.messages import SystemMessage
from .state import ProjectState
from .models import get_model
from pathlib import Path
import importlib.resources as pkg_resources
import datetime

def phase_guide_agent(state: ProjectState, model_id: str):
    model = get_model(model_id)
    project_path = Path(state["project_path"])
    target_phase = state.get("current_phase", "1")
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    
    # 1. Read Inputs
    roadmap_content = ""
    architecture_content = ""
    
    rm_path = project_path / "ROADMAP.md"
    if rm_path.exists():
        with open(rm_path, "r") as f:
            roadmap_content = f.read()
    else:
        roadmap_content = "No roadmap found."

    arch_path = project_path / "ARCHITECTURE.md"
    if arch_path.exists():
        with open(arch_path, "r") as f:
            architecture_content = f.read()
    else:
        architecture_content = "No architecture document found."

    # 2. Read Templates
    try:
        overview_tpl = pkg_resources.files("jolly_flow.templates").joinpath("phase-overview.md.template").read_text(encoding="utf-8")
        checklist_tpl = pkg_resources.files("jolly_flow.templates").joinpath("phase-checklist.md.template").read_text(encoding="utf-8")
        guide_tpl = pkg_resources.files("jolly_flow.templates").joinpath("phase-implementation-guide.md.template").read_text(encoding="utf-8")
    except Exception as e:
        return {"messages": [SystemMessage(content=f"Error reading templates: {e}")]}

    # 3. Build Prompt (Multi-file generation)
    system_prompt = (
        f"You are the Phase Lead for The Jolly Method. Today is {current_date}. "
        f"Your goal is to generate the detailed implementation guides for Phase {target_phase}. "
        "You must generate THREE separate markdown documents based on the Roadmap and Architecture below. "
        "Separate the documents clearly with a line containing only: ---FILE_SEPARATOR---. "
        "Structure your response exactly like this:"
        "\noverview.md"
        "\n---FILE_SEPARATOR---"
        "\nchecklist.md"
        "\n---FILE_SEPARATOR---"
        "\nimplementation-guide.md"
        "\n\n"
        "1. Analyze Phase {target_phase} in the Roadmap."
        "2. Fill out the phase-overview.md.template for this phase."
        "3. Fill out the phase-checklist.md.template with specific acceptance criteria."
        "4. Fill out the phase-implementation-guide.md.template with step-by-step tech instructions based on the Architecture."
        f"\n\n---\nPROJECT CONTEXT (from AI-CONTEXT.md):\n{state.get('ai_context', 'No context available')}"
        f"\n\n---\nROADMAP:\n{roadmap_content}"
        f"\n\n---\nARCHITECTURE:\n{architecture_content}"
        f"\n\n---\nTEMPLATE: overview\n{overview_tpl}"
        f"\n\n---\nTEMPLATE: checklist\n{checklist_tpl}"
        f"\n\n---\nTEMPLATE: guide\n{guide_tpl}"
    )
    
    # 4. Call Model
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
