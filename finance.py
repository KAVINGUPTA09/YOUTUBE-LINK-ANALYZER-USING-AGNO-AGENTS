from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
load_dotenv()

def build_agent():
    return Agent(
        model=Groq(id="qwen/qwen3-32b"),
        markdown=True,
        tools=[
            YFinanceTools(all=True), 
            DuckDuckGoTools(backend="api")
        ],
        add_datetime_to_context=True,
        debug_mode=True,
        description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=[
            "Use the tools provided to gather information about stock prices, analyst recommendations, and stock fundamentals.",
            "CRITICAL: Always check YFinanceTools first for core stock details, analyst targets, and recommendations.",
            "When asked for currency conversion (like USD to INR), pull the ticker 'INR=X' via YFinanceTools to fetch the live exchange rate instead of relying on web searches.",
            "Provide a comprehensive analysis based on the data you collect."
        ],
    )

agent = build_agent()
agent.print_response("Share the MSFT stock price in INR and analyst recommendation")