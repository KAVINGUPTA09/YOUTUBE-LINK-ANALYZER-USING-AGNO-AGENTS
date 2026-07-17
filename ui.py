import streamlit as st
import re
from yt import build_youtube_agent
from agno.tools.youtube import YouTubeTools

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@st.cache_resource
def get_agent():
    return build_youtube_agent()

agent = get_agent()

video_url = st.text_input("Enter Youtube Video Link") 
button = st.button("Analyze Video") 

if video_url and button:
    video_id = extract_video_id(video_url)
    
    if not video_id:
        st.error("Invalid YouTube URL format. Please check your link.")
    else:
        with st.spinner("Analyzing video transcript details..."):
            try:
                # 1. Grab the library's official tools
                yt_tools = YouTubeTools()
                
                # 2. Call the exact method from the Agno package signature
                video_data = yt_tools.get_youtube_video_captions(url=video_url)
                
                # 3. Deliver text blocks straight into the prompt layer
                prompt_payload = (
                    f"Perform a complete analysis report on this video content. "
                    f"Video Metadata and Context: {video_data}"
                )
                
                response = agent.run(prompt_payload)
                st.markdown("### Analysis Report of Video:")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Analysis processing error: {str(e)}")
