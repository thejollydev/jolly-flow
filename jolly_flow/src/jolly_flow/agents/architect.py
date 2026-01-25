from langchain_core.messages import SystemMessage, HumanMessage
from .state import ProjectState
from .models import get_model
from pathlib import Path

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

    # 2. Build Prompt
    system_prompt = (
        "You are the System Architect for The Jolly Method. "
        "Your goal is to design the system architecture based on the provided requirements. "
        "Do NOT just generate a generic architecture. "
        "1. Analyze the requirements below. "
        "2. If this is the start of the conversation, propose 2-3 distinct architectural approaches "
        "(e.g., Monolith vs. Microservices, SQL vs. NoSQL) and explain the trade-offs for THIS specific project. "
        "3. Ask the user which approach they prefer or if they have constraints. "
        "4. Once a direction is agreed upon, generate a draft of ARCHITECTURE.md and TECH-STACK.md. "
        "5. Always use the project templates structure for the final output."
        f"\n\n---\nEXISTING REQUIREMENTS:\n{requirements_content}"
    )
    
    # 3. Call Model
    # We append the conversation history (state["messages"]) to keep context
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
