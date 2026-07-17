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
        # Built-in Agno native tools initialized cleanly
        tools=[YouTubeTools()],
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            
            You have access to the YouTubeTools suite. Use these tools to systematically pull the textual transcript sequence data for the given video link.
            
            Once you extract the data, process it into a structured report:
            1. Video Blueprint & Core Target Objective
            2. Detailed Segment Roadmap Breakdown
            3. Summary Checklist of Key Learnings
            
            Quality Control:
            - Write in rich, clean Markdown format.
            - If a specific video node fails due to captions configuration, extract whatever structural metadata the tool can provide.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
