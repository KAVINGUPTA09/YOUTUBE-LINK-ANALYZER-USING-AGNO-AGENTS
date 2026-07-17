from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
load_dotenv()
from rich.pretty import pprint

db = SqliteDb(db_file="agno.db")

def build_agent():
    return Agent(
        model=Groq(id="qwen/qwen3-32b"),
        db=db,
        markdown=True,
        enable_user_memories=True,
        add_history_to_context=True
    )

user_id = "guptakavin6@gmail.com"
agent = build_agent()

# Pass a unique session_id along with the user_id to preserve the active session history context
session_id = "kavin_travel_session"

agent.print_response("I am Kavin Gupta a Data Scientist", user_id=user_id, session_id=session_id)
agent.print_response("Who am I?", user_id=user_id, session_id=session_id)

print("\nMemories:")
user_memories = agent.memory_manager.get_user_memories(user_id=user_id)
pprint(user_memories)