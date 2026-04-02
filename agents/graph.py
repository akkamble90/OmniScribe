# This is the Orchestrator of the applicatoin to define how agents are connected and the order in which they work
from langgraph.graph import StateGraph, END
from .state import AgentState
#To pull the python function from the node all three Agents 
from .nodes import researcher_node, analyst_node, critic_node

workflow = StateGraph(AgentState)

# 1. Add all three nodes (Agent, and fucntion)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("critic", critic_node)

# 2. Logic flow for each edge
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "critic") # Analyst hands it to Critic
workflow.add_edge("critic", END)       # Critic gives the final word
#application compilation so at the tiem of invoke it triggers the entire chain reaction
legal_agent_app = workflow.compile()