import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from yt import build_youtube_agent

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

# Helper function to extract the 11-character Video ID safely
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
                # ALTERNATIVE METHOD: Using list_transcripts() to extract standard data securely
                transcript_obj = YouTubeTranscriptApi.list_transcripts(video_id)
                # Automatically fetches the primary available transcript text block
                active_transcript = transcript_obj.find_transcript(['ar', 'en'])
                transcript_data = active_transcript.fetch()
                
                # Format text with its duration positioning markers
                transcript_context = " ".join([f"[{item['start']}] {item['text']}" for item in transcript_data])
            except Exception as e:
                transcript_context = f"[System Alert: Captions unavailable or non-verbal presentation: {str(e)}]"
            
            # Neatly bundle the text down for the agent prompt
            prompt_payload = f"Analyze this video link: {video_url}. Context transcript data: {transcript_context}"
            
            response = agent.run(prompt_payload)

        st.markdown("### Analysis Report of Video:")
        st.markdown(response.content)
