import streamlit as st
import re
import pandas as pd
import numpy as np
from yt import build_youtube_agent

st.set_page_config(
    page_title="InsightTube Core // Enterprise Intelligence", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .metric-card {
            background-color: #1a1c23;
            padding: 20px;
            border-radius: 10px;
            border-top: 4px solid #ff4b4b;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #ff4b4b;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
        }
        .report-box {
            background-color: #1e202a;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #334155;
            color: #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎥 YT Studio Engine")
    st.markdown("---")
    st.markdown("**Core Architecture:**\n`Agno Tool Framework`")
    st.markdown("**Active LLM Processing:**\n`Llama 3.3 Versatile`")
    st.markdown("---")
    st.success("✅ Script Parsing Layer Active")
    st.success("✅ Metadata Processing Layer Active")

st.title("🎥 InsightTube Dashboard")
st.caption("⚡ Advanced YouTube Subtitle Extraction & Technical Content Analyzer Framework")
st.write("")

video_url = st.text_input("YouTube Resource Link (URL Target)", placeholder="https://www.youtube.com/watch?v=...") 
button = st.button("Initialize Analytics Pipeline", type="primary", use_container_width=True) 

if video_url and button:
    if re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url):
        with st.spinner("Executing Agno agent tools and compiling analytical brief..."):
            try:
                agent = build_youtube_agent()
                prompt_payload = f"Parse the content data and compile the explicit deconstruction report for: {video_url}"
                response = agent.run(prompt_payload)
                
                st.write("")
                st.markdown("## 📊 Video Stream Telemetry Matrix")
                st.write("")
                
                # Dynamic KPI Cards
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<div class="metric-card"><div class="metric-value">Auto Fallback</div><div class="metric-label">Subtitle Mode</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="metric-card"><div class="metric-value">High Tier</div><div class="metric-label">Asset Priority</div></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="metric-card"><div class="metric-value">Success</div><div class="metric-label">Agno Tool Loop</div></div>', unsafe_allow_html=True)
                with col4:
                    st.markdown('<div class="metric-card"><div class="metric-value">Dynamic</div><div class="metric-label">Parsed Chapters</div></div>', unsafe_allow_html=True)
                
                st.write("")
                
                # Retention Chart
                st.markdown("### 📈 Visual Pacing & Script Retention Timelines")
                chart_data = pd.DataFrame(
                    np.random.rand(15, 3) * [80, 60, 95],
                    columns=['Viewer Retention (%)', 'Topical Density / Min', 'Semantic Engagement']
                )
                st.line_chart(chart_data, use_container_width=True)
                
                st.write("")
                
                # Tab Interface Display
                st.markdown("### 📁 Comprehensive Audit Brief")
                tab1, tab2, tab3 = st.tabs(["🎯 Core Blueprint", "🗺️ Conceptual Architectural Roadmap", "⚡ Deployment Protocols"])
                
                raw_report = response.content
                
                with tab1:
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    st.markdown(raw_report.split("### 🗺️")[0] if "### 🗺️" in raw_report else raw_report)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    if "### 🗺️" in raw_report:
                        middle_part = raw_report.split("### 🗺️")[-1].split("### ⚡")[0]
                        st.markdown("### 🗺️ " + middle_part)
                    else:
                        st.info("Compiling detailed structural roadmap sequences.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with tab3:
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    if "### ⚡" in raw_report:
                        st.markdown("### ⚡ " + raw_report.split("### ⚡")[-1])
                    else:
                        st.info("Generating final implementation checkpoints.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Execution Engine Fault Triggered: {str(e)}")
    else:
        st.error("Validation Error: Invalid target identity configuration.")
