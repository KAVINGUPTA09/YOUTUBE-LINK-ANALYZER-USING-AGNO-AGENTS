from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.team import Team

load_dotenv()
eng_agent=Agent(name="English Agent",role="You are the questions in English")
hindi_agent=Agent(name="Hindi Agent",role="You are the questions in Hindi")
Chinese_agent=Agent(name="Chinese Agent",role="You are the questions in Chinese")

team_leader=Team(
    name="Answer and translation team",
    members=[eng_agent,hindi_agent,Chinese_agent],
    model=Groq(id="qwen/qwen3-32b"),
    markdown=True,
    
    instructions="""All members agent should respon to the query in there specific language,
                    Donot route to just one agent.
                    Output the respone of all agents.
                """

)

team_leader.print_response("What is the capital of India?")
