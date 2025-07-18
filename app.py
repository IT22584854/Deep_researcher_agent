import streamlit as st
from agents import DeepResearcherAgent
import time
import base64

st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔎",
)


    # Create title with embedded images
title_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; padding: 32px 0 24px 0;">
        <h1 style="margin: 0; padding: 0; font-size: 2.5rem; font-weight: bold;">
            <span style="font-size:2.5rem;">🔎</span> Deep Research Agent </h1>           
    </div>
    """
st.markdown(title_html, unsafe_allow_html=True)

with st.sidebar:

    st.header("About")
    st.markdown(
        """
    This application is powered by a `DeepResearcherAgent` which leverages multiple AI agents for a comprehensive research process:
    - **Searcher**: Finds and extracts information from the web.
    - **Analyst**: Synthesizes and interprets the research findings.
    - **Writer**: Produces a final, polished report.
    """
    )

# Chat input at the bottom
user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    try:
        agent = DeepResearcherAgent()
        with st.status("Executing research plan...", expanded=True) as status:
            # PHASE 1: Researching
            phase1_msg = "🧠 **Phase 1: Researching** - Finding and extracting relevant information from the web..."
            status.write(phase1_msg)
            research_content = agent.searcher.run(user_input)

            # PHASE 2: Analyzing
            phase2_msg = "🔬 **Phase 2: Analyzing** - Synthesizing and interpreting the research findings..."
            status.write(phase2_msg)
            analysis = agent.analyst.run(research_content.content)

            # PHASE 3: Writing Report
            phase3_msg = (
                "✍️ **Phase 3: Writing Report** - Producing a final, polished report..."
            )
            status.write(phase3_msg)
            report_iterator = agent.writer.run(analysis.content, stream=True)

        # Move report display outside of status block
        full_report = ""
        report_container = st.empty()
        for chunk in report_iterator:
            if chunk.content:
                full_report += chunk.content
                report_container.markdown(full_report)

    except Exception as e:
        st.error(f"An error occurred: {e}")