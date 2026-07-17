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
            Use simple, direct corporate words that are easy to read. 
            
            CRITICAL FORMATTING RULE: 
            Avoid huge, heavy blocks of text. Make the layout highly visual, attractive, and eye-catching by using bold labels, icons/emojis, short broken bullet lines, and clear section separators.
            
            You must format your response explicitly using these EXACT headers below so the frontend can parse the tabs correctly:

            ### 🎯 Video Blueprint & Enterprise Target Objective
            
            🔹 **CORE DOMAIN FOCUS**
            • **Main Topic:** [Write clean, bold, simple summary line]
            • **Industry Significance:** [Short bullet point mapping trends]
            • **Target Market Impact:** [One-line impact highlight]
            
            🔹 **TECHNICAL & ARCHITECTURAL DIMENSIONS**
            • **Core Framework:** [Simple technical logic breakdown]
            • **Engineering Problem:** [Identify the main roadblock discussed]
            • **System Delivery:** [Data points or tech layers utilized]
            
            🔹 **CREATIVE & ENGAGEMENT MATRIX**
            • **Audience Psychology:** [How it grabs viewer attention]
            • **Storytelling Hook:** [The primary communication style used]
            • **Retention Strategy:** [Visual pacing or structure notes]

            ### 🗺️ Detailed Conceptual Roadmap
            
            📍 **PHASE 1: FOUNDATIONAL LAYER**
            • **Baseline Concept:** [Explain the absolute basics in simple words]
            • **Core Definitions:** [What everyone needs to know first]
            
            📍 **PHASE 2: ECOSYSTEM DEPENDENCIES**
            • **Micro-Connections:** [How different parts connect together]
            • **System Feedback Loops:** [Hidden dependencies mapped clearly]
            
            📍 **PHASE 3: RISK & CHALLENGE PROFILES**
            • **Primary Threats:** [What major risks are highlighted]
            • **Secondary Externalities:** [The long-term danger or problems]
            
            📍 **PHASE 4: FUTURE STATE GOVERNANCE**
            • **Global Standards:** [How the world or industry handles this]
            • **Compliance Models:** [Actionable regulatory or system frameworks]

            ### ⚡ Actionable Enterprise Checklist
            
            🚀 **STRATEGIC PRE-REQUISITES**
            ☐ **Metric Audit:** Establish baseline analytics variables before deployment.
            ☐ **Prerequisite Scan:** Verify technical readiness and environment checks.
            
            ⚙️ **OPERATIONAL GUARDRAILS**
            ☐ **Risk Avoidance:** Set strict containment boundaries for mitigation.
            ☐ **Architecture Setup:** Deploy sustainable blueprint controls instantly.
            
            📈 **SCALE & OPTIMIZATION PIPELINES**
            ☐ **Continuous Track:** Monitor long-term compliance metrics regularly.
            ☐ **Community Scaling:** Expand ecosystem reach using structural scaling data.

            *Report securely compiled via Agno Production Tool Framework Loop.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
