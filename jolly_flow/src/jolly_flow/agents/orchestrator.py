from langgraph.graph import StateGraph, END
from .state import ProjectState
from .requirements import requirements_agent
from .architect import architect_agent
from .human import human_review

def should_continue(state: ProjectState):
    last_message = state['messages'][-1].content
    if 'APPROVED' in last_message:
        return END
    return 'agent'

def create_requirements_graph(model_id: str):
    workflow = StateGraph(ProjectState)
    
    def agent_node(state):
        return requirements_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', END: END})
    return workflow.compile()

def create_architecture_graph(model_id: str):
    workflow = StateGraph(ProjectState)
    
    def agent_node(state):
        return architect_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', END: END})
    return workflow.compile()
