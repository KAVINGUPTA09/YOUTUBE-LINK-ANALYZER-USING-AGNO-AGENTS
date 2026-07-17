from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.youtube import YouTubeTools

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Groq(id="qwen/qwen3-32b"), 
        # Agno native YouTube tools ko yahan inject kiya hai
        tools=[YouTubeTools()],
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            
            Use your YouTube tools to fetch the video data and transcript for the provided link, then analyze it using these steps:
            
            1. Video Overview
            - Identify video title and type (documentary, tutorial, review, etc.)
            - Summarize the main objective and content structure.
            
            2. Language & Translation Management
            - Note the primary language of the source text.
            - If the transcript is in a foreign language (like Arabic), translate it and write the entire report clearly in English.
            
            3. Content Analysis & Timeline
            - Create precise, meaningful breakdown highlights based strictly on the transcript text.
            - Format structural checkpoints clearly using timestamps.
            
            Your analysis style:
            - Begin with a comprehensive video overview.
            - Use clear, descriptive segment titles.
            - Include relevant emojis for content types:
            📚 Educational | 💻 Technical | 🎮 Gaming | 📱 Tech Review | 🎨 Creative
            
            Quality Guidelines:
            - Rely strictly on the tool output data. Do not hallucinate or create fake details.
        """),
        add_datetime_to_context=True,
        show_tool_calls=True, # Ye dashboard par tool execution dikhayega
        markdown=True,
    )
