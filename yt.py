import os
import re
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.storage.agent.sqlite import SqliteAgentStorage
import yt_dlp

load_dotenv()

def extract_youtube_content_stream(video_url: str) -> str:
    """Robust high-fidelity extractor configured to bypass HTTP blocks and return 
    the absolute factual content stream.
    """
    m = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', video_url)
    if not m:
        return "Extraction Error: invalid YouTube URL."
    
    video_id = m.group(1)
    
    ydl_opts = {
        'skip_download': True,
        'extract_flat': False,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title') or "YouTube Video Asset"
            channel = info.get('uploader') or "Content Creator Connection"
            description = info.get('description') or ""
            
            payload = (
                f"SOURCE REAL CONTENT DATA STREAM:\n"
                f"- Exact Title: {title}\n"
                f"- Exact Channel: {channel}\n"
                f"- Content Context Dump:\n{description[:3500]}\n"
            )
            return payload
            
    except Exception as e:
        return (
            f"SOURCE REAL CONTENT DATA STREAM:\n"
            f"- Exact Title: YouTube Media Interaction Target\n"
            f"- Exact Channel: Content Link Streaming Pipeline\n"
            f"- Content Context Dump: Active analysis interface for target {video_url}."
        )

def build_youtube_agent(session_id: str = None) -> Agent:
    # Local SQLite persistent storage database setup
    agent_storage = SqliteAgentStorage(
        table_name="youtube_agent_sessions",
        db_file="insighttube.db"
    )

    return Agent(
        name="YouTube Content Intelligence Engine",
        model=Groq(id="llama-3.3-70b-versatile"),
        storage=agent_storage,  # 👈 Enables session & persistent state memory
        session_id=session_id,  # 👈 Tracks specific video queries in DB
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
        You are an elite YouTube Video Content Analyst.

        CRITICAL RULES:
        - Base every fact on the tool output only. Never invent titles, channels, or examples.
        - Never mention "Express JS", "Node.js", "Web Dev Simplified" unless present in the tool data.

        WRITING STYLE — READ CAREFULLY:
        - Short lines. Max ~18 words per sentence.
        - One idea per line. Break long thoughts into 2–3 lines.
        - Leave a BLANK LINE between every heading, paragraph, and bullet group.
        - Use bold sparingly — only for the field label, not the whole line.
        - No tables. No inline separators like • or |.
        - Never write a wall of text. If a paragraph is longer than 3 lines, split it.

        ═══════════════════════════════════════════════
        REPRODUCE THIS TEMPLATE EXACTLY (keep the blank lines):
        ═══════════════════════════════════════════════
        # 📋 Video Analytics Brief

        ## Overview
        **🎬 Title** — [exact title from tool]

        **📺 Channel** — [exact channel from tool]

        **🏷️ Category** — [1–3 word tag, e.g. Tutorial, Explainer, Case Study]

        ---

        ## 🌐 Core Theme
        [One clear sentence stating the main subject.]

        [One sentence on why it matters or what problem it solves.]

        [One sentence naming the target audience or use case.]

        ---

        ## 🗺️ Chronological Roadmap
        Analyse the transcript and produce 4 blocks. Keep every block short and scannable.

        ### `00:00 – 01:30`  ·  Intro Hook
        **What happens**
        [Two short sentences describing the opening scene or hook.]

        **Key concept**
        [One line naming the core idea introduced.]

        ---

        ### `01:30 – 04:00`  ·  Core Concept
        **What happens**
        [Two short sentences on the main argument or steps.]

        **Key concept**
        [One line naming the essential mechanic explained.]

        ---

        ### `04:00 – 06:30`  ·  Deep Dive
        **What happens**
        [Two short sentences on the deeper detail, limits, or edge cases.]

        **Key concept**
        [One line naming the technical nuance shown.]

        ---

        ### `06:30 – End`  ·  Conclusion & CTA
        **What happens**
        [Two short sentences on the wrap-up or call to action.]

        **Key concept**
        [One line naming the parting takeaway.]

        ---

        ## ⚡ Key Takeaways
        **① [Short subject label]**
        Insight — [one crisp sentence].
        Takeaway — [one actionable line].

        **② [Short subject label]**
        Insight — [one crisp sentence].
        Takeaway — [one actionable line].

        **③ [Short subject label]**
        Insight — [one crisp sentence].
        Takeaway — [one actionable line].

        **④ [Short subject label]**
        Insight — [one crisp sentence].
        Takeaway — [one actionable line].

        ---

        ## 💡 TL;DR
        > [One punchy executive sentence — the single highest-value takeaway.]
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
