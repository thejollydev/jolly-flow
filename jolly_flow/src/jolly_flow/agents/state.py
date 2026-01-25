from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ProjectState(TypedDict):
    # add_messages allows us to append to the list rather than overwrite
    messages: Annotated[List[BaseMessage], add_messages]
    project_name: str
    project_path: str
    current_phase: str
    instructions: str
