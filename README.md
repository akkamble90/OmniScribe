# OmniScribe Auditor 

**OmniScribe Auditor** is an advanced, Multi-Agent RAG (Retrieval-Augmented Generation) system designed to analyze, teach, and audit high-stakes documents across various domains, including Legal, Medical, IEEE Technical Reports, and Economic Analysis.

Built with **LangGraph**, **Llama-3.3-70B**, and **Streamlit**, it utilizes a sophisticated "Researcher-Analyst-Critic" workflow to ensure technical depth, eliminate AI hallucinations, and provide professional-grade summaries.

---

## Key Features

- Multi-Agent Orchestration
  - Researcher Agent: Retrieves the most relevant document chunks and identifies the core "DNA" of the uploaded file from the ChromaDB vector store.
  - Analyst Agent: Generates accurate, context-grounded answers strictly based on the uploaded document.
  - Critic Agent (Auditor): Reviews responses for factual consistency, removes generic filler, and validates citations.

- Universal Document Intelligence
  - Supports a wide range of document types including legal files, technical papers, medical reports, research articles, business documents, contracts, financial statements, and more.
  - Automatically adapts its reasoning style based on the uploaded content without requiring the user to specify the domain.

- Domain-Aware Reasoning
  - Legal Documents: Understands contracts, court orders, compliance files, and case law.
  - Technical & IEEE Papers: Handles engineering concepts, circuit design, research methodology, formulas, and academic standards.
  - Medical Documents: Summarizes diagnoses, treatment plans, case reports, and includes appropriate safety disclaimers.
  - Financial & Economic Reports: Interprets brokerage reports, CAGR, forecasts, risk analysis, and market trends.

- Interactive Learning Support
  - Explains complex concepts in simpler language when the source document assumes prior knowledge.
  - Helps users understand technical, academic, or domain-specific terminology step by step.

- Professional Export Options
  - Generates structured summaries, reports, and downloadable PDF outputs for sharing or documentation.

- Enterprise-Grade Security
  - Uses localized ChromaDB vector storage for document privacy.
  - Maintains session-based audit logging for traceability and secure enterprise workflows.

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
