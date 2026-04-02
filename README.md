# OmniScribe Auditor 

**OmniScribe Auditor** is an advanced, Multi-Agent RAG (Retrieval-Augmented Generation) system designed to analyze, teach, and audit high-stakes documents across various domains, including Legal, Medical, IEEE Technical Reports, and Economic Analysis.

Built with **LangGraph**, **Llama-3.3-70B**, and **Streamlit**, it utilizes a sophisticated "Researcher-Analyst-Critic" workflow to ensure technical depth, eliminate AI hallucinations, and provide professional-grade summaries.

---

##  Key Features

- **Multi-Agent Orchestration:** - 🔍 **Researcher:** Precisely retrieves document "DNA" from a ChromaDB vector store.
  -  **Analyst:** Synthesizes complex answers grounded strictly in the provided context.
  -  **Critic (The Auditor):** Performs a "Senior Peer Review" pass to flag generic filler and verify citations.
- **Universal Domain Awareness:** Specialized protocols for:
  - **Legal:** Court orders, contracts, and case law.
  - **IEEE/Technical:** High-pass filters, circuit design, and academic peer-review standards.
  - **Medical:** Management of clinical cases (e.g., Retinoblastoma) with safety disclaimers.
  - **Economics:** Brokerage reports, CAGR, and market trend verification.
- **Interactive Teaching:** Bridges the gap for users missing fundamental concepts within technical papers.
- **Professional Exports:** Generate and download auto-summarized reports in PDF format.
- **Enterprise Security:** Localized vector storage (ChromaDB) and session-based audit logging.

---

##  System Architecture

The system follows an **Agentic RAG** workflow:
1. **Ingestion:** Documents (PDF, Docx, Images) are processed and indexed into a persistent ChromaDB.
2. **Query:** User asks a question via the Streamlit interface.
3. **Graph Execution:**
   - The **Researcher** finds the 5 most relevant document chunks.
   - The **Analyst** drafts a response based on those chunks.
   - The **Critic** audits the draft against domain-specific protocols.
4. **Output:** The user receives a verified, hallucination-free answer.



---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/OmniScribe-Auditor.git](https://github.com/your-username/OmniScribe-Auditor.git)
cd OmniScribe-Auditor