import streamlit as st
import re
from yt import build_youtube_agent

st.set_page_config(
    page_title="Youtube Video Analyzer", 
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

video_url = st.text_input("Enter Youtube Video Link") 
button = st.button("Analyze Video") 

if video_url and button:
    # URL basic format checking
    video_id_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    
    if video_id_match:
        with st.spinner("Agent is running tools to analyze the video..."):
            try:
                # Direct safe instantiation per dynamic execution block
                agent = build_youtube_agent()
                
                # Direct link handoff to the Agno Agent layer
                prompt_payload = f"Please extract the transcript and analyze this video: {video_url}"
                response = agent.run(prompt_payload)
                
                st.markdown("### Analysis Report of Video:")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Analysis processing error: {str(e)}")
    else:
        st.error("Invalid YouTube URL format. Please check your link.")
