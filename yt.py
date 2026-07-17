
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
        tools=[YouTubeTools()],  # Explicitly added tool tracking here
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            Use your integrated YouTubeTools to look up video details and transcript metadata.
            
            Analyze the provided video details systematically using these steps:
            
            1. Video Overview
            - Identify video title and type (documentary, tutorial, review, gaming, etc.)
            - Note the content structure.
            
            2. Language & Translation Management
            - The text context might occasionally contain foreign language scripts (e.g. Arabic, Spanish). 
            - If it is in a foreign language, automatically translate it and write your entire report clearly in English.
            
            3. Content Analysis & Timeline
            - Create precise, meaningful breakdown highlights based on the context text.
            - Format structural checkpoints clearly using timestamps in this format: [HH:MM:SS] or [MM:SS].
            
            Your analysis style:
            - Begin with a comprehensive video overview.
            - Use clear, descriptive segment titles.
            - Include relevant emojis for content types:
            📚 Educational | 💻 Technical | 🎮 Gaming | 📱 Tech Review | 🎨 Creative
            
            Quality Guidelines:
            - Rely strictly on the injected context data.
            - Do not hallucinate fake details.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
