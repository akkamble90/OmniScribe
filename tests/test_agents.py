import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from agents.nodes import researcher_node, analyst_node

# --- Mocking the Data ---

@pytest.fixture
def mock_state():
    """Provides a standard starting state for testing nodes."""
    return {
        "messages": [HumanMessage(content="What is the notice period?")],
        "context": ""
    }

# --- Tests ---

def test_researcher_node_structure(mock_state):
    """
    Verifies that the researcher node queries the DB 
    and updates the 'context' key.
    """
    # We patch the query_db function to avoid needing a real ChromaDB during tests
    with patch('agents.nodes.query_db') as mock_query:
        # Simulate finding one document snippet
        mock_doc = MagicMock()
        mock_doc.page_content = "Termination requires 30 days notice."
        mock_query.return_value = [mock_doc]
        
        result = researcher_node(mock_state)
        
        assert "context" in result
        assert "30 days notice" in result["context"]

def test_analyst_node_requirements(mock_state):
    """
    Verifies that the analyst node produces a message 
    and includes the mandatory legal disclaimer.
    """
    # Add context to the state as if the researcher already ran
    mock_state["context"] = "Section 5: 30 days notice required."
    
    with patch('agents.nodes.llm.invoke') as mock_llm:
        # Simulate LLM response
        mock_llm.return_value = AIMessage(
            content="The notice period is 30 days. Source: Section 5. Consult an attorney."
        )
        
        result = analyst_node(mock_state)
        
        assert "messages" in result
        assert isinstance(result["messages"][0], AIMessage)
        # Check if the disclaimer logic is present in the output
        assert "Consult an attorney" in result["messages"][0].content

def test_graph_compilation():
    """
    Ensures the LangGraph compiles without circular 
    dependency or missing node errors.
    """
    from agents.graph import legal_agent_app
    assert legal_agent_app is not None