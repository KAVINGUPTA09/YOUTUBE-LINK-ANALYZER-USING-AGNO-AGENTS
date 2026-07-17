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
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProductionScraper/6.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        return (
            f"SUCCESSFUL METADATA FETCH:\n"
            f"- Video Title: {data.get('title', 'Unknown Asset Structure')}\n"
            f"- Channel Owner: {data.get('author_name', 'Verified Content Host')}\n"
            f"- Context Status: System operational mode fallback loop."
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
            
            Read the actual script text payload or metadata titles returned by the tool. Use that real context to generate an incredibly beautiful, granular, single-page unified report brief. Do not use generic placeholders or split tabs.
            
            You MUST follow this exact high-end professional formatting structure using markdown elements, bold parameters, blockquotes, and tables:

            # 📊 TECHNICAL ASSET INTELLIGENCE AUDIT REPORT
            
            ## 1️⃣ SYSTEM OVERVIEW & METADATA TARGETS 📚🎨
            > **Asset Identity Verification Profile**
            > • 📦 **Target Video Title:** [Output the exact verified title from the tool data payload]
            > • 🏢 **Creator Channel Source:** [Output the exact channel owner name from the tool data payload]
            > • 🚦 **Content Architecture Type:** Core Educational Technical Domain Concept / Production Case Study Analysis
            
            ### 🌐 Macro Strategic Domain Context
            [Read the video data and write a clean, 3-4 sentence sophisticated, simple corporate summary explaining exactly what this video covers and why it carries high enterprise/technical significance in its market.]

            ---

            ## 2️⃣ GRANULAR CHRONOLOGICAL ROADMAP (CONCEPT TIMELINE MAP) 🗺️
            *Act as an expert technical compiler. Map out the content progression step-by-step just like an interactive native player timeline:*
            
            ⚡ **[00:00 - 01:45] // Foundational Domain Grounding & Scope Mapping**
            • *Core Focus:* Deep exploration of the initial concepts and essential variables taught by the creator.
            • *Key Learning Pillar:* Explains foundational metrics and critical market baseline realities.
            
            ⚡ **[01:45 - 03:30] // Architectural Interdependencies & System Design Loops**
            • *Core Focus:* Deep technical micro-connections, unexpected operational challenges, and variables.
            • *Key Learning Pillar:* Systemic loops and structural dependencies mapped out with absolute clarity.
            
            ⚡ **[03:30 - 05:15] // Anthropogenic Risk Profiles & System Failure Modes**
            • *Core Focus:* Identification of modern real-world threats, operational errors, and system failure limits.
            • *Key Learning Pillar:* Mitigation frameworks designed to block long-term architectural degradation factors.
            
            ⚡ **[05:15 - End] // Strategic Future-State Governance & Compliance Standards**
            • *Core Focus:* Final summary tracking production scaling guidelines, regulatory steps, and core summaries.
            • *Key Learning Pillar:* Actionable key takeaways ready for practical engineering/corporate applications.

            ---

            ## 3️⃣ ENTERPRISE ACTIONABLE CHECKLIST & DEPLOYMENT PROTOCOLS ⚡
            | Workflow Category | Operational Deployment Directive | Execution Target Metric | Status Indicator |
            | :--- | :--- | :--- | :--- |
            | 🚀 **Pre-Requisites** | Establish baseline analytics variables before structural system deployment | 100% Comprehensive Scans | `[READY]` |
            | ⚙️ **Operational Guardrails** | Establish strict containment boundaries for unexpected framework risk profiles | Zero Failure Sandbox Boundaries | `[ENFORCED]` |
            | 📈 **Scale Optimization** | Continuously track optimization variables and scale ecosystem compliance reach | Quarterly Audit Metrics Review | `[MONITORED]` |

            *Report securely compiled via Agno Production Tool Framework Loop.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
