from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.youtube import YouTubeTools

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[YouTubeTools()],
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            
            Use your YouTube tools to fetch the video data and transcript for the provided link, then analyze it using these steps:
            
            1. Video Overview
            - Identify video title and type (documentary, tutorial, review, etc.)
            
            2. Content Analysis & Timeline
            - Create precise, meaningful breakdown highlights based strictly on the text.
            
            Important Layer Rules:
            - If your internal YouTube tools return a network error or block status, use your inner knowledge framework to analyze the topic suggested by the URL title string. Do not crash or display an error message.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
