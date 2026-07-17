import streamlit as st
import re
import youtube_transcript_api
from yt import build_youtube_agent

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
            
            transcript_context = ""
            try:
                # FOOLPROOF FIX: We call the standalone functional module method directly
                transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
                transcript_context = " ".join([f"[{item['start']}] {item['text']}" for item in transcript_list])
            except Exception as e:
                transcript_context = f"ERROR_FETCHING: {str(e)}"
            
            # CRITICAL CHECK: If the transcript failed to download, show the error directly to the user
            if "ERROR_FETCHING:" in transcript_context:
                st.error(f"Failed to extract transcript from YouTube: {transcript_context}")
            else:
                prompt_payload = f"Analyze this video link: {video_url}. Context transcript data: {transcript_context}"
                response = agent.run(prompt_payload)
                
                st.markdown("### Analysis Report of Video:")
                st.markdown(response.content)
