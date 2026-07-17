import streamlit as st
import re
from yt import build_youtube_agent

st.set_page_config(page_title="Youtube Video Analyzer", layout="centered")
st.title("🎥 AI Youtube Video Analyzer")

video_url = st.text_input("Enter Youtube Video Link") 
button = st.button("Analyze Video") 

if video_url and button:
    video_id_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    
    if video_id_match:
        with st.spinner("Agno Agent is running official YouTubeTools framework..."):
            try:
                agent = build_youtube_agent()
                
                # Direct call telling the agent to use its tool set
                prompt_payload = f"Use your YouTubeTools to retrieve data and analyze this video link: {video_url}"
                response = agent.run(prompt_payload)
                
                st.markdown("### Analysis Report of Video:")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Framework Exception: {str(e)}")
    else:
        st.error("Invalid YouTube URL format. Please check your link.")
