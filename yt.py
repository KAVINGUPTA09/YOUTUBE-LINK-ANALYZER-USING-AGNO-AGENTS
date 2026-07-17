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
    """Advanced technical pipeline that extracts the absolute raw transcript dump in bulk 
    to provide high-density context variables to the downstream LLM processing block.
    """
    m = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not m:
        return "Extraction Error: Invalid target link architecture syntax."
    
    video_id = m.group(1)
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Primary Data Stream Layer: Bulk Transcript Mining Channel
    try:
        srt = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en', 'en-US', 'en-GB', 'hi', 'es']
        )
        bulk_lines = []
        for item in srt:
            mnt = int(item['start'] // 60)
            sec = int(item['start'] % 60)
            bulk_lines.append(f"[{mnt}:{sec:02d}] {item['text']}")
        
        # Pulling the entire available script block for complete textual transparency
        return "SUCCESSFUL BULK TRANSCRIPT STREAM FETCH:\n" + "\n".join(bulk_lines)
    except Exception:
        pass
        
    # Secondary Target Recovery Pipeline: Structural Metadata Scraper Bypass
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProductionBrief/8.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        return (
            "SUCCESSFUL METADATA RECOVERY NODE:\n"
            f"- Video Title: {data.get('title', 'Unknown Concept Profile')}\n"
            f"- Channel Owner: {data.get('author_name', 'Verified Creator Node')}\n"
            f"- Notice: Script tracks restricted. Deconstruct the global concept based entirely on this direct metadata payload context."
        )
    except Exception as e:
        return f"Critical Data Pipe Failure: Extraction interface broken. Detail: {str(e)}"

def build_youtube_agent() -> Agent:
    return Agent(
        name="YouTube Heavy Content Intelligence Engine",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
        You are a high-fidelity Senior YouTube Content Dissection Specialist.
        
        CRITICAL OPERATIONAL RULES:
        - NEVER output generic placeholder text like "No description available", "Ecosystem analysis begins", or "Protect the environment".
        - You must review the absolute raw transcript dump or titles provided by the tool call. Extract dense, real-world granular details.
        - If the script talks about specific codebase parameters, framework tools, animal species, technical numbers, or scientific data, you must document them explicitly. 
        - Provide extreme density of text. Fill out the report with heavy, comprehensive factual knowledge extracted directly from the text block.
        
        FORMATTING RULES (STRICT FOR THE LOVABLE UI):
        - Every field goes on its OWN line. Never combine values using bullet points on the same line string.
        - Leave one blank line between every timeline block and every section.
        - Use standard markdown matrix tables. No inline HTML injection allowed.
        
        ═══════════════════════════════════════════════
        TEMPLATE — reproduce this structure exactly:
        ═══════════════════════════════════════════════
        # 📋 YouTube Video Analytics Brief
        
        ## 1️⃣ Overview
        **🎬 Title:** [Insert exact full asset title parsed from the tool response]
        **📺 Channel:** [Insert exact corporate channel name parsed from the tool response]
        **🏷️ Category:** High-Density Asset Content Structure Analysis
        
        ### 🌐 Core Theme
        [Detailed factual statement 1 tracking the explicit background reality taught in this script]
        [Detailed factual statement 2 explaining the deep mechanics/variables demonstrated by the creator]
        [Detailed factual statement 3 summarizing the exact practical final execution outcome]
        
        ---
        
        ## 2️⃣ Chronological Roadmap 🗺️
        Analyze the bulk text and extract 4 heavy, comprehensive chronological roadmap blocks. Do NOT use short placeholder phrases.
        
        ### ⚡ `[00:00 – 01:30]` — Intro Hook
        **Section**
        [Write a deep, multi-word descriptive sentence explaining the exact opening context sequence or direct example shown by the creator]
        
        **Key Concept**
        [The absolute primary core technical/scientific topic or precise variable introduced here]
        
        ---
        
        ### ⚡ `[01:30 – 04:00]` — Core Concept
        **Section**
        [Write a heavy, detailed breakdown sentence tracking the main system process, code logic, or primary operational behavior explained next]
        
        **Key Concept**
        [The exact structural mechanism, dynamic workflow, or factual reality detailed in this block]
        
        ---
        
        ### ⚡ `[04:00 – 06:30]` — Deep Dive / Challenges
        **Section**
        [Write a comprehensive sentence detailing the specific system limitations, environmental threats, failure modes, or real-world friction metrics covered here]
        
        **Key Concept**
        [The precise roadblock variables, data points, or performance costs described by the speaker]
        
        ---
        
        ### ⚡ `[06:30 – End]` — Conclusion & CTA
        **Section**
        [Write a clean, informative sentence outlining how the video concludes its narrative arc, system testing, or long-term guidance loops]
        
        **Key Concept**
        [The exact, concrete real-world actionable takeaway or deployment benchmark left behind for the viewer]
        
        ---
        
        ## 3️⃣ Key Takeaways Matrix ⚡
        | # | Core Topic | Insight from Video | Viewer Takeaway |
        | :- | :--- | :--- | :--- |
        | 1 | [Factual Subject 1] | [Detailed specific observation mapping exact script realities in ≤14 words] | [Actionable workflow metric step in ≤10 words] |
        | 2 | [Factual Subject 2] | [Detailed specific observation mapping exact script realities in ≤14 words] | [Actionable workflow metric step in ≤10 words] |
        | 3 | [Factual Subject 3] | [Detailed specific observation mapping exact script realities in ≤14 words] | [Actionable workflow metric step in ≤10 words] |
        | 4 | [Factual Subject 4] | [Detailed specific observation mapping exact script realities in ≤14 words] | [Actionable workflow metric step in ≤10 words] |
        
        ---
        
        ## 4️⃣ TL;DR
        > [Insert a single line punchy, extremely powerful executive summary packing the absolute highest-value takeaway from the entire transcript payload]
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
