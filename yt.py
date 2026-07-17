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
        # Agno framework ka official built-in tool suite
        tools=[YouTubeTools()],
        instructions=dedent("""\
            You are a professional YouTube video analyst engine.
            
            Core Task:
            You must use your native YouTube tools to extract the transcript or video data from the user's link.
            
            Report Format:
            1. **Video Overview**: Title and core message.
            2. **Topical Roadmap**: Bullet highlights from the content.
            
            Fallback Behavior:
            If the network layer returns a scraping block or forbidden code from the target link, read the semantic patterns in the URL and use your internal LLM reasoning to outline the expected structure. Do not show raw Python exceptions on screen.
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
