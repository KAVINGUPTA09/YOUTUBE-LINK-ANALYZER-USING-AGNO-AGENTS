from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Groq(id="llama-3.3-70b-versatile"), 
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            
            Analyze the provided transcript text data systematically using these steps:
            
            1. Video Overview
            - Summarize the main objective and content structure.
            
            2. Language & Translation Management
            - If the transcript contains foreign languages, translate them cleanly into English.
            
            3. Content Analysis & Timeline
            - Create precise, meaningful breakdown highlights based strictly on the text.
            
            Quality Guidelines:
            - Rely strictly on the injected context data. Do not hallucinate.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
