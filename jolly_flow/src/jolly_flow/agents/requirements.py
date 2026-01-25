from langchain_core.messages import SystemMessage, HumanMessage
from .state import ProjectState
from .models import get_model

def requirements_agent(state: ProjectState, model_id: str):
    model = get_model(model_id)
    
    system_prompt = (
        "You are the Requirements Analyst for The Jolly Method. "
        "Your goal is to gather project requirements through an interactive conversation. "
        "Based on the project name and any previous context, ask clarifying questions or "
        "generate a draft of REQUIREMENTS.md if you have enough information."
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = model.invoke(messages)
    return {"messages": [response]}
