from langgraph.graph import StateGraph, END
from .state import ProjectState
from .requirements import requirements_agent
from .architect import architect_agent
from .planner import planner_agent
from .phase_guide import phase_guide_agent
from .human import human_review
from .saver import save_requirements_node, save_architecture_node, save_roadmap_node

def should_continue(state: ProjectState):
    """Determine next step after human review"""
    last_message = state['messages'][-1].content
    if 'APPROVED' in last_message:
        return 'save'  # Go to save node
    return 'agent'  # Loop back to agent for revision

def create_requirements_graph(model_id: str):
    workflow = StateGraph(ProjectState)

    def agent_node(state):
        return requirements_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.add_node('save', save_requirements_node)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', 'save': 'save'})
    workflow.add_edge('save', END)
    return workflow.compile()

def create_architecture_graph(model_id: str):
    workflow = StateGraph(ProjectState)

    def agent_node(state):
        return architect_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.add_node('save', save_architecture_node)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', 'save': 'save'})
    workflow.add_edge('save', END)
    return workflow.compile()

def create_roadmap_graph(model_id: str):
    workflow = StateGraph(ProjectState)

    def agent_node(state):
        return planner_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.add_node('save', save_roadmap_node)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', 'save': 'save'})
    workflow.add_edge('save', END)
    return workflow.compile()

def create_phase_guide_graph(model_id: str):
    workflow = StateGraph(ProjectState)
    
    def agent_node(state):
        return phase_guide_agent(state, model_id)

    workflow.add_node('agent', agent_node)
    workflow.add_node('human', human_review)
    workflow.set_entry_point('agent')
    workflow.add_edge('agent', 'human')
    workflow.add_conditional_edges('human', should_continue, {'agent': 'agent', END: END})
    return workflow.compile()
