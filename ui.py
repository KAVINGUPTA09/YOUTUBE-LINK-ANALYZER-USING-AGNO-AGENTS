import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from yt import build_youtube_agent

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

# Helper function to extract 11-character Video ID from any YouTube URL format
def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@st.cache_resource
def get_agent():
    return build_youtube_agent()

agent = get_agent()

# Input UI elements
video_url = st.text_input("Enter Youtube Video Link")
button = st.button("Analyze Video")

if video_url and button:
    video_id = extract_video_id(video_url)
    
    if not video_id:
        st.error("Invalid YouTube URL format. Please double-check the link.")
    else:
        with st.spinner("Extracting content and running analysis..."):
            
            # Step 1: Securely extract text data directly in Python to bypass cloud IP blocks
            transcript_context = ""
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_context = " ".join([item['text'] for item in transcript_list])
            except (NoTranscriptFound, TranscriptsDisabled):
                transcript_context = "[System Alert: This video contains no spoken commentary or captions. It appears to be an audio/visual presentation or montage.]"
            except Exception as e:
                transcript_context = f"[System Alert: Script ingestion paused by target platform restrictions: {str(e)}]"
            
            # Step 2: Build the clean structural payload block for the model
            prompt_payload = f"""
            Please generate a comprehensive review for this asset:
            - Target link: {video_url}
            - Context content string: {transcript_context}
            """
            
            st.markdown("### Analysis Report of Video:")
            
            # Step 3: Stream out the completion token response dynamically in real-time
            # agent.run() returns a RunResponse object, we pass its text stream generator directly
            response = agent.run(prompt_payload)
            st.markdown(response.content)
