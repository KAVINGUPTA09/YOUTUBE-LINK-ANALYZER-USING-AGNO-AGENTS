import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from yt import build_youtube_agent

st.set_page_config(page_title="Youtube Video Analyzer", layout="centered")
st.title("🎥 AI Youtube Video Analyzer")

def get_transcript(video_id):
    try:
        # Puraani backend dependency chhodkar direct extraction logic execution
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ar'])
        return " ".join([f"[{item['start']}] {item['text']}" for item in transcript_list])
    except Exception:
        # Fallback to search list array parsing
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        active_transcript = transcript_list.find_transcript(['en', 'ar'])
        return " ".join([f"[{item['start']}] {item['text']}" for item in active_transcript.fetch()])

video_url = st.text_input("Enter Youtube Video Link") 
button = st.button("Analyze Video") 

if video_url and button:
    video_id_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    
    if video_id_match:
        video_id = video_id_match.group(1)
        with st.spinner("Fetching and analyzing video details..."):
            try:
                transcript_text = get_transcript(video_id)
                
                agent = build_youtube_agent()
                prompt_payload = f"Analyze this video transcript text: {transcript_text}"
                response = agent.run(prompt_payload)
                
                st.markdown("### Analysis Report of Video:")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Could not extract transcript or run analysis: {str(e)}")
    else:
        st.error("Invalid YouTube URL format. Please check your link.")
