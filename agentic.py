from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
load_dotenv()

def build_agent():
    return Agent(
        model=Groq(id="qwen/qwen3-32b"),
        markdown=True,#not simple text
        tools=[DuckDuckGoTools()],
        add_datetime_to_context=True,
        instructions="You are a helpful assistant and a travel expert agent",
    )


agent=build_agent()
agent.print_response("Is UAE safe to travel currently")
