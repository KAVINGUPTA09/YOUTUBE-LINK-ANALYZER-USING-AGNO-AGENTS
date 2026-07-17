import streamlit as st
import re
import youtube_transcript_api # Import module cleanly to fix the attribute error
from yt import build_youtube_agent

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

# Helper function to extract the 11-character Video ID from any YouTube URL format
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
        st.error("Invalid YouTube URL format. Please double-check the link.")
    else:
        with st.spinner("Extracting content and running analysis..."):
            
            transcript_context = ""
            try:
                # FIXED PATH: Accessing the class explicitly through the imported module path
                transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
                transcript_context = " ".join([item['text'] for item in transcript_list])
            except Exception as e:
                # Catching any missing transcript or structural exception safely
                transcript_context = f"[System Alert: This video might not have spoken captions, or processing was paused: {str(e)}]"
            
            prompt_payload = f"""
            Please generate a comprehensive review for this asset:
            - Target link: {video_url}
            - Context content string: {transcript_context}
            """
            
            st.markdown("### Analysis Report of Video:")
            response = agent.run(prompt_payload)
            st.markdown(response.content)
