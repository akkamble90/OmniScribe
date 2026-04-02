import streamlit as st
import os
import pandas as pd
from datetime import datetime
from langchain_core.messages import HumanMessage

# Import custom modules
from utils.auth_logger import init_db, log_action, get_audit_report
from utils.document_processor import process_any_format
from utils.vector_db import add_documents_to_db
from agents.graph import legal_agent_app

# INITIALIZATION: login page details  
st.set_page_config(page_title="OmniScribe", layout="wide", page_icon="⚖️")

# Ensure necessary directories exist
if not os.path.exists("data"):
    os.makedirs("data")

init_db()

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# BRANDING HELPER: Renders contact info at the bottom of the sidebar
def render_sidebar_footer():
    st.sidebar.divider()
    st.sidebar.markdown("### 📞 Contact Details")
    st.sidebar.caption("📧 **Email:** support@omniaudit.in")
    st.sidebar.caption("📱 **Phone:** +91-0712-745644")
    st.sidebar.caption("📍 COEP, Main building, Wellesely Road, Shivajinagar, Pune – 411005, Maharashtra, India")
    
    # Social Media Badges
    cols = st.sidebar.columns(4)
    with cols[0]: st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/-In-blue?logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)")
    with cols[1]: st.sidebar.markdown("[![Instagram](https://img.shields.io/badge/-IG-pink?logo=instagram&logoColor=white)](https://instagram.com/yourprofile)")
    with cols[2]: st.sidebar.markdown("[![X](https://img.shields.io/badge/-X-black?logo=x&logoColor=white)](https://twitter.com/yourprofile)")
    with cols[3]: st.sidebar.markdown("[![Site](https://img.shields.io/badge/-Site-gray?logo=google-chrome&logoColor=white)](https://omniaudit.in)")

# --- 2. AUTHENTICATION UI (HOME PAGE) ---
if not st.session_state.authenticated:
    # Display logo_solution for the login screen
    if os.path.exists("logo_solution.png"):
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            st.image("logo_solution.png", use_container_width=True)
            
    st.markdown("<h1 style='text-align: center;'> OmniScribe </h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center;'>Enter Username & Password to login</h3>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        
        if st.button("Sign In", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.authenticated = True
                st.session_state.user = user
                log_action(user, "User Login")
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
        
        st.button("Forgot Credentials?", on_click=lambda: st.info("Please contact IT at support@omniaudit.in"))
    
    render_sidebar_footer()
    st.stop()

# --- 3. DASHBOARD SIDEBAR ---
with st.sidebar:
    # Smaller, centered logo_search for the sidebar
    if os.path.exists("logo_search.png"):
        side_col1, side_col2, side_col3 = st.columns([1, 1, 1])
        with side_col2:
            st.image("logo_search.png", use_container_width=True)
            
    st.title("⚖️ Control Panel")
    st.write(f"Logged in as: **{st.session_state.user}**")
    st.divider()

    st.subheader("📁 Ingest Documents")
    upload_type = st.radio("Source Type", ["File Upload", "Web Link"])
    
    if upload_type == "File Upload":
        uploaded_file = st.file_uploader("Upload PDF, Word, or Image", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])
        if uploaded_file and st.button("Process & Index", use_container_width=True):
            with st.spinner("Analyzing document..."):
                temp_path = os.path.join("data", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                ext = uploaded_file.name.split(".")[-1].lower()
                chunks = process_any_format(temp_path, ext)
                
                if chunks:
                    add_documents_to_db(chunks)
                    log_action(st.session_state.user, "Indexed File", uploaded_file.name)
                    st.success(f"Successfully indexed {len(chunks)} snippets!")
                    os.remove(temp_path)
                else:
                    st.error("Extraction failed. Check file content or permissions.")
    else:
        url = st.text_input("Enter Web Link (URL)")
        if url and st.button("Scrape & Index", use_container_width=True):
            with st.spinner("Scraping web data..."):
                chunks = process_any_format(url, "url")
                if chunks:
                    add_documents_to_db(chunks)
                    log_action(st.session_state.user, "Indexed URL", url)
                    st.success(f"Successfully indexed {len(chunks)} snippets from the web!")
                else:
                    st.error("Web scraping failed. Ensure the URL is valid and publicly accessible.")

    st.divider()
    st.subheader("📊 System Reports")
    if st.button("Generate Access Log", use_container_width=True):
        df_logs = get_audit_report()
        st.download_button(
            label="Download CSV Report",
            data=df_logs.to_csv(index=False),
            file_name=f"legal_audit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    if st.button("Logout", use_container_width=True):
        log_action(st.session_state.user, "User Logout")
        st.session_state.authenticated = False
        st.rerun()

    render_sidebar_footer()

# --- 4. MAIN INTERFACE ---
# Centered Main Title on Dashboard
st.markdown("<h1 style='text-align: center;'> OmniScribe </h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs([" Case Analysis Chat", " Executive Summary"])

with tab1:
    # Refresh/Clear Chat button with adequate width
    col_header, col_refresh = st.columns([0.8, 0.2])
    with col_refresh:
        if st.button("🔄 Refresh Chat", help="Clear Chat history", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # logo_chat for the chat interface
    if os.path.exists("logo_chat.png"):
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
        with col_c2:
            st.image("logo_chat.png", use_container_width=True)

    st.markdown("<h3 style='text-align: center;'>Ask questions about your indexed documents</h3>", unsafe_allow_html=True)
    
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("Ex: 'Summarize the clinical findings...'"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting knowledge base..."):
                inputs = {"messages": [HumanMessage(content=prompt)]}
                result = legal_agent_app.invoke(inputs)
                response = result["messages"][-1].content
                st.markdown(response)
                
                log_action(st.session_state.user, "Chat Query", prompt[:50] + "...")
                st.session_state.chat_history.append({"role": "assistant", "content": response})

with tab2:
    # logo (original) for the summary interface
    if os.path.exists("logo.png"):
        col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
        with col_t2:
            st.image("logo.png", use_container_width=True)
            
    st.markdown("<h2 style='text-align: center;'> Auto-Generated Report</h2>", unsafe_allow_html=True)
    st.divider()
    
    if st.button("Analyze Knowledge Base Summary", use_container_width=True):
        with st.spinner("Synthesizing final report..."):
            summary_prompt = "Provide a comprehensive, professional summary of all indexed materials, categorized by key findings."
            summary_result = legal_agent_app.invoke({"messages": [HumanMessage(content=summary_prompt)]})
            
            st.session_state.current_report = summary_result["messages"][-1].content
            log_action(st.session_state.user, "Generated Summary Report")

    if "current_report" in st.session_state:
        st.markdown(st.session_state.current_report)
        
        from utils.pdf_generator import generate_pdf
        pdf_bytes = generate_pdf(st.session_state.current_report)
        
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_bytes,
            file_name=f"OmniScribe_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )