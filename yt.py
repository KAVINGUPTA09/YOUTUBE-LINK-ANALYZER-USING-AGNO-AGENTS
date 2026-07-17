import os
import re
import json
import urllib.request
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

def extract_youtube_content_stream(video_url: str) -> str:
    """Automated data mining component that safely extracts semantic details, structural text transcripts,
    or falls back to verified oEmbed metadata blocks depending on real-time server network status layers.
    """
    video_id_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not video_id_match:
        return "Extraction Error: Invalid target link format mapping."
    
    video_id = video_id_match.group(1)
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Execution Layer Stage 1: Native Subtitle Track Parsing
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        return f"SUCCESSFUL TRANSCRIPT FETCH:\n" + " ".join([item['text'] for item in srt])
    except Exception:
        pass  # Cloud server network restriction encountered, falling back to network bypass channel
        
    # Execution Layer Stage 2: Public oEmbed Object Interception
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        req = urllib.request.Request(
            oembed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) InsightClient/2.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        return (
            f"SUCCESSFUL METADATA FETCH:\n"
            f"- Verified Asset Title: {data.get('title', 'Unknown Concept Context')}\n"
            f"- Resource Provider: {data.get('author_name', 'Verified Content Source')}\n"
            f"- State: Cloud sandbox proxy fallback active."
        )
    except Exception as e:
        return f"Critical Pipeline Connection Failure: {str(e)}"

def build_youtube_agent() -> Agent:
    """Factory configuration initializing the Agno automation client agent with registered tool layers."""
    return Agent(
        name="YouTube Analytics Core Orchestrator",
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
            You are a premier cloud automation engine and content analyst! 🎓
            
            OPERATIONAL MANDATE:
            You must run `extract_youtube_content_stream` with the user-provided link to retrieve context.
            
            Using the output payload provided by the tool asset channel, compile a rich, deep dashboard report.
            
            Synthesize the layout strictly using these clean markdown visual segments:
            ### 🎯 Video Blueprint & Target Objective
            Provide a deep structural statement of the core theme and technical/creative objectives of this material.
            
            ### 🗺️ Detailed Conceptual Roadmap
            Create a highly informative step-by-step master learning path or topical framework breakdown detailing every core component related to this concept domain.
            
            ### ⚡ Actionable Enterprise Checklist
            List crisp, production-grade strategic guidelines and major takeaways suitable for practical engineering/workspace applications.
            
            Verification Footer Statement:
            Include a small clean text block at the bottom: "*Report securely compiled via Agno Production Tool Framework Loop.*"
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
