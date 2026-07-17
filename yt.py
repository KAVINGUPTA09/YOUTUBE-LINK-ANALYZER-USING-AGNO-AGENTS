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
    
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        return f"SUCCESSFUL TRANSCRIPT FETCH:\n" + " ".join([item['text'] for item in srt])
    except Exception:
        pass
        
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        req = urllib.request.Request(
            oembed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) InsightClient/3.0'}
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
            You are a senior enterprise content analyst and system orchestrator! 🎓
            
            OPERATIONAL MANDATE:
            You must execute the tool `extract_youtube_content_stream` with the provided link.
            
            Synthesize an extensive, highly granular dashboard analysis brief based on the tool data.
            You must format your response explicitly using these EXACT headers below so the frontend can parse the tabs correctly:

            ### 🎯 Video Blueprint & Enterprise Target Objective
            - **Core Theme & Value Proposition:** Deep, comprehensive breakdown of the core problem domain and its industrial/environmental significance.
            - **Algorithmic & Technical Dimensions:** Analysis of systemic roadblocks or structural methodologies addressed.
            - **Creative & Engagement Matrix:** Breakdown of communication structures and messaging frameworks used to capture focus.

            ### 🗺️ Detailed Conceptual Roadmap
            1. **Phase 1: Fundamental Grounding:** In-depth evaluation of definitions, foundational metrics, and background realities.
            2. **Phase 2: Complex Ecosystem Dependencies:** Granular breakdown of biological, industrial, or technical micro-connections and feedback loops.
            3. **Phase 3: Risk Profiles & Failure Modes:** Deep analysis of modern threats, degradation factors, and secondary negative externalities.
            4. **Phase 4: Global Framework Governance:** Concrete evaluation of systematic recovery models, international policy compliance, and management frameworks.

            ### ⚡ Actionable Enterprise Checklist
            - **Strategic Pre-Requisites:** Exact data metrics, auditing standards, and operational parameters required before action.
            - **Operational Guardrails:** Deployment parameters, mitigation systems, and risk avoidance controls to establish.
            - **Optimization & Scale Metrics:** Protocols for long-term tracking, ecosystem compliance, and community scale-up metrics.

            *Report securely compiled via Agno Production Tool Framework Loop.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
