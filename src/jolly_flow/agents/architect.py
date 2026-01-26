from langchain_core.messages import SystemMessage, HumanMessage
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
        "Your goal is to design the system architecture based on the provided requirements. "
        "Do NOT just generate a generic architecture. "
        "1. Analyze the requirements below. "
        "2. If this is the start of the conversation, propose 2-3 distinct architectural approaches "
        "(e.g., Monolith vs. Microservices, SQL vs. NoSQL) and explain the trade-offs for THIS specific project. "
        "3. Ask the user which approach they prefer or if they have constraints. "
        "4. Once a direction is agreed upon, generate a draft of ARCHITECTURE.md and TECH-STACK.md. "
        "5. IMPORTANT: You MUST follow the exact structure of the provided templates below for the final output."
        f"\n\n---\nPROJECT CONTEXT (from AI-CONTEXT.md):\n{state.get('ai_context', 'No context available')}"
        f"\n\n---\nEXISTING REQUIREMENTS:\n{requirements_content}"
        f"\n\n---\nTEMPLATE: ARCHITECTURE.md\n{arch_template}"
        f"\n\n---\nTEMPLATE: TECH-STACK.md\n{tech_template}"
    )
    
    # 4. Call Model
    # We append the conversation history (state["messages"]) to keep context
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
