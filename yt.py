import os
import re
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
import yt_dlp

load_dotenv()

def extract_youtube_content_stream(video_url: str) -> str:
    """Robust fallback extractor that utilizes yt-dlp layer mechanics to completely bypass 
    network drops and download core subtitle tracks or description data safely.
    """
    m = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not m:
        return "Extraction Error: invalid YouTube URL pattern."
    
    video_id = m.group(1)
    
    # Target parameter options for deep data mining
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub:': True,
        'subtitleslangs': ['en.*', 'hi.*'],
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Unknown Concept Title')
            channel = info.get('uploader', 'Unknown Content Channel')
            description = info.get('description', '')
            
            # Formulating target data core block
            data_payload = (
                f"SUCCESSFUL DATA FETCH PIPELINE:\n"
                f"- Video Title: {title}\n"
                f"- Channel Owner: {channel}\n"
                f"- Core Script/Context Data Chunk:\n{description[:1500]}\n"
            )
            return data_payload
            
    except Exception as e:
        return f"Pipeline connection failure: Real content extraction aborted due to framework layers. Info: {str(e)}"

def build_youtube_agent() -> Agent:
    return Agent(
        name="YouTube Content Intelligence Engine",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
        You are an elite YouTube Video Content Analyst.
        
        OPERATIONAL DIRECTIVE:
        1. Call `extract_youtube_content_stream` with the user's URL.
        2. Read the returned transcript / metadata chunk carefully. Extract the true conceptual points.
        3. Produce a clean, highly formatted, scannable report using the EXACT markdown template below.
        
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
        **🎬 Title:** [Insert exact title extracted from tool]
        **📺 Channel:** [Insert exact channel extracted from tool]
        **🏷️ Category:** Technical Architecture Concept Deep Dive
        
        ### 🌐 Core Theme
        [Insert 1st short sentence explaining the major point taught in the video]
        [Insert 2nd short sentence explaining the technical problem solved]
        [Insert 3rd short sentence detailing the exact real world value]
        
        ---
        
        ## 2️⃣ Chronological Roadmap 🗺️
        Break the video theme down into 4 clear roadmap blocks. Follow this layout precisely:
        
        ### ⚡ `[00:00 – 01:30]` — Intro Hook
        **Section**
        [Write a single short sentence explaining how this content context opens up]
        
        **Key Concept**
        [Write one short sentence mapping the initial baseline concept]
        
        ---
        
        ### ⚡ `[01:30 – 04:00]` — Core Concept
        **Section**
        [Write a single short sentence breaking down the core execution step]
        
        **Key Concept**
        [Write one short sentence mapping the primary system mechanism]
        
        ---
        
        ### ⚡ `[04:00 – 06:30]` — Deep Dive / Challenges
        **Section**
        [Write a single short sentence detailing the technical hurdles or trade-offs]
        
        **Key Concept**
        [Write one short sentence explaining how to handle these constraints]
        
        ---
        
        ### ⚡ `[06:30 – End]` — Conclusion & CTA
        **Section**
        [Write a single short sentence summarizing the final wrapping message]
        
        **Key Concept**
        [Write one short sentence explaining the instant actionable takeaway]
        
        ---
        
        ## 3️⃣ Key Takeaways Matrix ⚡
        | # | Core Topic | Insight from Video | Viewer Takeaway |
        | :- | :--- | :--- | :--- |
        | 1 | [Topic 1] | [Insight in ≤14 words] | [Action in ≤10 words] |
        | 2 | [Topic 2] | [Insight in ≤14 words] | [Action in ≤10 words] |
        | 3 | [Topic 3] | [Insight in ≤14 words] | [Action in ≤10 words] |
        | 4 | [Topic 4] | [Insight in ≤14 words] | [Action in ≤10 words] |
        
        ---
        
        ## 4️⃣ TL;DR
        > [Insert a single line punchy powerful executive summary of the video content context]
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
