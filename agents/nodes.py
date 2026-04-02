import os
from langchain_groq import ChatGroq
from utils.vector_db import query_db
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from .state import AgentState

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def researcher_node(state: AgentState):
    user_query = state["messages"][-1].content
    try:
        rel_docs = query_db(user_query, k=3)
        context_text = "\n\n".join([doc.page_content for doc in rel_docs])
    except:
        context_text = "No document context available."
    return {"context": context_text}

def analyst_node(state: AgentState):
    context = state.get("context", "")
    user_query = state["messages"][-1].content
    
    # REMOVED: Hardcoded legal disclaimer
    # ADDED: Instruction to identify the domain
    system_prompt = f"""
    You are a Universal Knowledge Assistant. Use this context: {context}
    1. Provide technical, factual analysis based ONLY on the context.
    2. Include citations/references from the text.
    3. Determine the domain (Medical, Legal, IEEE/Technical, or Financial).
    """
    response = llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}])
    return {"messages": [response]}

def critic_node(state: AgentState):
    """
    Step 3: Senior Auditor pass. 
    Now includes Dynamic Disclaimer Logic based on the industry.
    """
    last_message = state["messages"][-1].content
    context = state["context"]
    
    critic_prompt = f"""
    You are a Senior Peer Reviewer and Domain Auditor. 
    Your task is to verify the response against the context and append the MANDATORY industry-specific disclaimer.

    --- DYNAMIC DISCLAIMER PROTOCOLS ---
    Identify the topic of the response and append the matching note:
    - LEGAL: "Consult a licensed attorney for specific legal matters."
    - MEDICAL: "Consult a qualified medical professional or specialist for clinical decisions."
    - IEEE/TECHNICAL: "Consult a subject matter expert or research scientist for technical implementation."
    - ECONOMICS/FINANCE: "Consult a certified financial advisor or economist for investment analysis."
    - GENERAL: "This analysis is AI-generated for informational purposes. Verify facts with a domain expert."

    --- INTERNAL AUDIT ---
    1. Verfiy hallucinations against REFERENCE CONTEXT.
    2. Remove any "AI fluff" or conversational filler.
    3. Ensure the tone matches the industry (e.g., formal for Legal, precise for IEEE).

    REFERENCE CONTEXT: {context}
    RESPONSE TO AUDIT: {last_message}

    STRICT OUTPUT RULE:
    - Return ONLY the polished answer + the specific professional disclaimer.
    - Do NOT output your internal thinking, categories, or "Audit Passed" labels.
    """
    
    response = llm.invoke([{"role": "system", "content": critic_prompt}])
    return {"messages": [response]}