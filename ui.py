import streamlit as st
import re
from yt import build_youtube_agent

# Enterprise dashboard theme configuration
st.set_page_config(
    page_title="InsightTube // Advanced Video Intelligence", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom injection for sleek developer-centric styling
st.markdown("""
    <style>
        .report-card {
            background-color: #1a1c23;
            padding: 24px;
            border-radius: 12px;
            border-left: 5px solid #4f46e5;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .metric-badge {
            background: linear-gradient(135deg, #4f46e5, #06b6d4);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .section-header {
            color: #e2e8f0;
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Application Sidebar Layout
with st.sidebar:
    st.markdown("### ⚙️ Engine Control Room")
    st.markdown("---")
    st.info("**Core Model:** Groq `llama-3.3-70b-versatile`\n\n**Orchestrator:** Agno Framework AI Agent System")
    st.markdown("---")
    st.caption("Designed for production-grade textual metadata mining and analytics pipelines.")

# Primary Workspace Viewport
st.title("🎥 InsightTube")
st.caption("⚡ Advanced YouTube Content Intelligence Engine Powered by Agno Tool Integration")
st.write("")

video_url = st.text_input("Target Asset URI", placeholder="https://www.youtube.com/watch?v=...") 
button = st.button("Initialize Analytics Pipeline", type="primary") 

if video_url and button:
    if re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url):
        with st.spinner("Executing Agno automated tool loops and structural analytics synthesis..."):
            try:
                agent = build_youtube_agent()
                prompt_payload = f"Execute your operational tool pipeline loop to process and analyze this asset source link: {video_url}"
                response = agent.run(prompt_payload)
                
                st.write("")
                st.markdown("## 📊 Engine Execution Report")
                st.markdown('<span class="metric-badge">Status: Analysis Successful</span>', unsafe_allow_html=True)
                st.write("")
                
                # Render clean markdown directly within our custom container layouts
                st.markdown(f'<div class="report-card">{response.content}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Execution Engine Fault Triggered: {str(e)}")
    else:
        st.error("Validation Error: Invalid YouTube URL configuration format detected.")
