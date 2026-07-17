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
    """Fetch transcript with timestamps, fallback to oEmbed metadata."""
    m = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not m:
        return "Extraction Error: invalid YouTube URL."
    
    video_id = m.group(1)
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        srt = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en', 'en-US', 'en-GB', 'hi', 'es']
        )
        lines = []
        for item in srt[:80]:
            mnt = int(item['start'] // 60)
            sec = int(item['start'] % 60)
            lines.append(f"[{mnt}:{sec:02d}] {item['text']}")
        return "SUCCESSFUL TRANSCRIPT FETCH WITH TIMESTAMPS:\n" + "\n".join(lines)
    except Exception:
        pass
        
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        return (
            "SUCCESSFUL METADATA FETCH:\n"
            f"- Video Title: {data.get('title', 'Unknown')}\n"
            f"- Channel Owner: {data.get('author_name', 'Unknown')}\n"
        )
    except Exception as e:
        return f"Pipeline error: {e}"

def build_youtube_agent() -> Agent:
    return Agent(
        name="YouTube Content Intelligence Engine",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
        You are an elite YouTube Video Content Analyst.
        
        OPERATIONAL DIRECTIVE:
        1. Call `extract_youtube_content_stream` with the user's URL.
        2. Read the returned transcript / metadata carefully.
        3. Produce a clean, scannable report using the EXACT markdown template below.
        
        FORMATTING RULES (STRICT — the UI depends on this):
        - Every field goes on its OWN line. Never join fields with `•` on the same line.
        - Use short lines (max ~18 words). Break long thoughts across bullets.
        - Leave one blank line between every timeline block and every section.
        - Never wrap bold labels around long paragraphs — keep labels short.
        - Use plain markdown tables. No inline HTML.
        
        ═══════════════════════════════════════════════
        TEMPLATE — reproduce this structure exactly:
        ═══════════════════════════════════════════════
        # 📋 YouTube Video Analytics Brief
        
        ## 1️⃣ Overview
        **🎬 Title:** <exact title>
        **📺 Channel:** <exact channel>
        **🏷️ Category:** <one short phrase>
        
        ### 🌐 Core Theme
        <3 short sentences. Each sentence on its own line.>
        
        ---
        
        ## 2️⃣ Chronological Roadmap 🗺️
        Break the video into 4 timeline blocks. Use this EXACT shape per block (note the line breaks — do NOT collapse fields onto one line):
        
        ### ⚡ `[00:00 – 01:30]` — Intro Hook
        **Section**
        <one-sentence description of what happens in this segment>
        
        **Key Concept**
        <one short sentence naming the main idea introduced>
        
        ---
        
        ### ⚡ `[01:30 – 04:00]` — Core Concept
        **Section**
        <…>
        
        **Key Concept**
        <…>
        
        ---
        
        ### ⚡ `[04:00 – 06:30]` — Deep Dive / Challenges
        **Section**
        <…>
        
        **Key Concept**
        <…>
        
        ---
        
        ### ⚡ `[06:30 – End]` — Conclusion & CTA
        **Section**
        <…>
        
        **Key Concept**
        <…>
        
        ---
        
        ## 3️⃣ Key Takeaways Matrix ⚡
        | # | Core Topic | Insight from Video | Viewer Takeaway |
        | :- | :--- | :--- | :--- |
        | 1 | <topic> | <insight in ≤14 words> | <action in ≤10 words> |
        | 2 | <topic> | <…> | <…> |
        | 3 | <topic> | <…> | <…> |
        | 4 | <topic> | <…> | <…> |
        
        ---
        
        ## 4️⃣ TL;DR
        > <one-line punchy summary of the whole video>
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
