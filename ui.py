import streamlit as st
import re
import urllib.request
import xml.etree.ElementTree as ET
from yt import build_youtube_agent

st.set_page_config(page_title="Youtube Video Analyzer", layout="centered")
st.title("🎥 AI Youtube Video Analyzer")

def get_transcript(video_id):
    try:
        # Bypassing completely all blockable transcript libraries
        # Directly requesting YouTube's public raw timedtext track API
        api_url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(api_url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode('utf-8')
            
        if not xml_data.strip():
            raise Exception("No transcript data returned from YouTube API.")
            
        root = ET.fromstring(xml_data)
        transcript_lines = []
        
        for text_node in root.findall('text'):
            start = text_node.get('start', '0')
            text = text_node.text or ""
            # Cleaning up raw HTML entities like &#39;
            text = text.replace('&#39;', "'").replace('&quot;', '"')
            transcript_lines.append(f"[{start}] {text}")
            
        if not transcript_lines:
            raise Exception("Transcript track tracks are empty for this server node.")
            
        return " ".join(transcript_lines)
        
    except Exception as e:
        raise Exception(f"Direct XML engine bypass stream failed: {str(e)}")

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
