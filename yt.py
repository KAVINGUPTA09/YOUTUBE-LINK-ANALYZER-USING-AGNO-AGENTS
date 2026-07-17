
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Groq(id="qwen/qwen3-32b"), 
        # Tools removed from here to prevent cloud IP scraping errors
        tools=[], 
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            Analyze the provided video details and text context systematically using these steps:
            
            1. Video Overview
            - Identify video type based on the title/metadata (tutorial, review, gaming highlights, lecture, etc.)
            - Note the content structure
            
            2. Content Analysis & Timeline
            - Create precise, meaningful breakdown highlights using the text context provided.
            - If a valid timestamp trace is present, format transitions cleanly: [start_time, end_time, detailed_summary]
            - If the context indicates the video has no voice track/spoken text (e.g. gameplay compilation, music video), outline the expected highlights based on the video title.
            
            Your analysis style:
            - Begin with a video overview
            - Use clear, descriptive segment titles
            - Include relevant emojis for content types:
            📚 Educational | 💻 Technical | 🎮 Gaming | 📱 Tech Review | 🎨 Creative
            
            Quality Guidelines:
            - Rely strictly on the injected context data.
            - Do not hallucinate fake details if the transcript is marked as unavailable or missing audio tracks.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
