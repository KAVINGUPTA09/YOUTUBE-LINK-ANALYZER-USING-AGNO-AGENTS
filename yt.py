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
    """Advanced technical content scraper that targets transcripts with exhaustive multi-language fallback 
    protocols or extracts public structural oEmbed schemas to prevent tool blocks.
    """
    video_id_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not video_id_match:
        return "Extraction Error: Target URL parameters contain invalid mapping geometry."
    
    video_id = video_id_match.group(1)
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB', 'hi', 'es'])
        full_text = []
        for index, item in enumerate(srt[:50]): # Pulling solid dynamic script blocks
            start_min = int(item['start'] // 60)
            start_sec = int(item['start'] % 60)
            full_text.append(f"[{start_min}:{start_sec:02d}] {item['text']}")
            
        return f"SUCCESSFUL TRANSCRIPT FETCH WITH TIMESTAMPS:\n" + "\n".join(full_text)
    except Exception:
        pass
        
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        req = urllib.request.Request(
            oembed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProductionScraper/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        return (
            f"SUCCESSFUL METADATA FETCH:\n"
            f"- Video Title: {data.get('title', 'Unknown Asset Structure')}\n"
            f"- Channel Owner: {data.get('author_name', 'Verified Content Host')}\n"
            f"- Context Status: Sandbox bypass mode initialized."
        )
    except Exception as e:
        return f"System Pipeline Disconnection: Raw data extraction aborted. {str(e)}"

def build_youtube_agent() -> Agent:
    return Agent(
        name="YouTube Core Video Inspector Engine",
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
            You are a senior YouTube Content Intelligence & Asset Deconstruction Engine.
            
            OPERATIONAL DIRECTIVE:
            You must execute the `extract_youtube_content_stream` tool with the provided link.
            
            Read the actual text or title metadata returned by the tool. Use that real context to generate an incredibly beautiful, granular, single-page unified report. Do not divide the text into multi-tab frameworks or templates.
            
            You MUST follow this exact visualization styling layout using clean emojis, standard Markdown markdown, clear tables, and crisp bullet alignments:

            # 📋 Technical Asset Audit Report
            
            ## 1️⃣ Video Overview Summary 📚🎨
            * **Target Video:** [Output the exact verified title from the tool]
            * **Creator Channel:** [Output the exact channel owner name from the tool]
            * **Content Archetype:** 🚀 Educational Engineering & Technical Deep Dive / Nature Documentary
            
            ### High-Level Content Architecture:
            • 🎬 **Cinematic Segment:** Introduction to the core problem and why this domain sector matters.
            • 🧩 **Structural Core Blocks:** Step-by-step breakdown of specialized topic parameters.
            • 🧪 **Engineering Breakdown:** Deep analysis of modern failure modes and technical implementation details.
            • 📈 **System Summary:** Final call-to-action, future optimization trends, and ecosystem conclusions.

            ---

            ## 2️⃣ Granular Conceptual Roadmap (Chronological Breakdown) 🗺️
            [Create an explicit, beautiful step-by-step sequence based directly on the video text context. Format each milestone exactly like this, making it extremely easy to scan]:
            
            * **[0:00 - 1:30] // System Core Initialization Hook** 🎯
              *Explains the immediate basic concepts and maps the background data baseline parameters.*
              
            * **[1:30 - 3:45] // Ecosystem Dependencies & Interconnected Design** 🧬
              *Dives into technical micro-connections, unexpected architectural variables, and live loop mechanics.*
              
            * **[3:45 - 6:00] // Failure Modes & Risk Mitigation Barriers** ⚠️
              *Identifies structural threats, external vulnerabilities, and continuous operational limitations.*
              
            * **[6:00 - End] // Global Standards Framework & Scaled Governance** 🎓
              *Details production guidelines, enterprise wiki setups, and strategic long-term takeaways.*

            ---

            ## 3️⃣ Actionable Enterprise Execution Checklist ⚡
            | Category | Deployment Directive Protocol | Action Target Metric |
            | :--- | :--- | :--- |
            | 🚀 Pre-Requisites | Establish baseline analytics metrics before structural deployment | 100% Audit Scans |
            | ⚙️ Guardrails | Establish strict containment boundaries for unexpected system risks | Zero Failure State |
            | 📈 Scale Operations | Continuously track optimization variables and expand ecosystem reach | Quarterly Compliance |
            
            *Report securely compiled via Agno Production Tool Framework Loop.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
