from langchain_core.messages import SystemMessage
from .state import ProjectState
from .models import get_model

def requirements_agent(state: ProjectState, model_id: str):
    model = get_model(model_id)

    system_prompt = (
        "You are the Requirements Analyst for The Jolly Method. "
        "Your goal is to gather project requirements through an INTERACTIVE CONVERSATION with the user.\n\n"
        "## RULES OF ENGAGEMENT:\n"
        "1. **ASK ONE QUESTION AT A TIME.** Do not overwhelm the user with a list.\n"
        "2. **Be Conversational.** Treat this like a chat, not a survey.\n"
        "3. **Wait for the answer.** Ask your question, then stop. The user will reply.\n"
        "4. **Iterate.** Use the user's answers to ask follow-up questions.\n"
        "5. **Generate the Document ONLY when ready.** When you have a clear picture of the Users, Goals, and Features, "
        "output the full 'REQUIREMENTS.md' content in markdown format.\n\n"
        "## Current Project Context:\n"
        f"{state.get('ai_context', 'No context available')}\n"
    )

    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    response = model.invoke(messages)
    return {"messages": [response]}

