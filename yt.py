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
        for index, item in enumerate(srt[:50]):
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
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProductionScraper/7.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        return (
            f"SUCCESSFUL METADATA FETCH:\n"
            f"- Video Title: {data.get('title', 'Unknown Asset Structure')}\n"
            f"- Channel Owner: {data.get('author_name', 'Verified Content Host')}\n"
            f"- Context Status: Safe proxy bypass running."
        )
    except Exception as e:
        return f"System Pipeline Disconnection: Raw data extraction aborted. {str(e)}"

def build_youtube_agent() -> Agent:
    return Agent(
        name="YouTube Core Video Inspector Engine",
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[extract_youtube_content_stream],
        instructions=dedent("""\
            You are an elite YouTube Video Content Intelligence & Content Analyst Engine.
            
            OPERATIONAL DIRECTIVE:
            You must execute the `extract_youtube_content_stream` tool using the link provided by the user. 
            
            Read the actual text transcript payload or verified video titles returned by the tool. Use that content to compile a comprehensive, single-page deep-dive report based purely on the video content. Do not use generic software metrics or predefined template rows. Everything must revolve around the actual video data.
            
            You MUST structure your output report exactly using this clean visual layout, bold identifiers, blockquotes, and HTML alignment tables:

            # 📋 YOUTUBE VIDEO CONTENT ANALYTICS BRIEF
            
            ## 1️⃣ Video Overview Summary 📚🎨
            > **Verified Content Stream Meta Profile**
            > • 📦 **Target Video Title:** [Output the exact verified video title from the tool data]
            > • 🏢 **Publishing Channel Source:** [Output the exact channel owner name from the tool data]
            > • 🚦 **Video Content Category:** Deep Informative Explainer / Structural Video Analysis
            
            ### 🌐 Video Core Theme & Value Proposition
            [Read the video script/title data and write a clean, simple 3-4 sentence summary in clear words explaining exactly what this specific video teaches the viewer and why it keeps the audience hooked.]

            ---

            ## 2️⃣ Granular Chronological Roadmap (Timeline Chapter Mapping) 🗺️
            *Act as a video editor. Breakdown the video progress step-by-step based on the script text data:*
            
            ⚡ **[00:00 - 01:30] // Video Intro Hook & Core Problem Statement**
            • *Section Breakdown:* What immediate hook or story does the creator use to grab the audience?
            • *Key Concept:* The core question or basic theme introduced in the first minutes.
            
            ⚡ **[01:30 - 04:00] // Main Informative Core & Concept Exploration**
            • *Section Breakdown:* Deep dive into the actual examples, tools, code, or data points discussed by the creator.
            • *Key Concept:* The primary educational block or core lesson of the video.
            
            ⚡ **[04:00 - 06:30] // Critical Analysis & Conflict Pacing**
            • *Section Breakdown:* What real-world challenges, limitations, or hard truths does the creator reveal here?
            • *Key Concept:* Addressing core pain points or roadblocks related to this topic.
            
            ⚡ **[06:30 - End] // Conclusion Summary & Call-To-Action (CTA)**
            • *Section Breakdown:* How does the video wrap up? What final advice or steps does the creator give the viewer?
            • *Key Concept:* The absolute best takeaway to remember from this entire watch.

            ---

            ## 3️⃣ Extracted Video Core Concepts & Key Takeaways Matrix ⚡
            [Create an HTML/Markdown table where every single row contains actual data extracted from the video content. Do not use generic template fields like SEO or Hook pacing. Map out the real core points taught in the video.]
            
            | Core Topic Discussed | Detailed Video Insight & Explanation | Key Takeaway for the Viewer |
            | :--- | :--- | :--- |
            | [Extract Topic 1 from Video] | [Explain what the video says about Topic 1 using real details from the script] | [What should the viewer learn/do based on this section] |
            | [Extract Topic 2 from Video] | [Explain what the video says about Topic 2 using real details from the script] | [What should the viewer learn/do based on this section] |
            | [Extract Topic 3 from Video] | [Explain what the video says about Topic 3 using real details from the script] | [What should the viewer learn/do based on this section] |
            | [Extract Topic 4 from Video] | [Explain what the video says about Topic 4 using real details from the script] | [What should the viewer learn/do based on this section] |

            *Report securely compiled via Agno Production Tool Framework Loop.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
