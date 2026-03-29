import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """Evaluate a maths expression."""
    return str(eval(expression))

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

agent = create_react_agent(model, tools=[calculator])

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 999 * 777?"}]
})

print(result["messages"][-1].content)