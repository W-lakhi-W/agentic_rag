from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is sunny and 72°F."

# Initialize the Groq chat model
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0,api_key=api_key)

# Bind tools to the model
# model_with_tools = model.bind_tools([get_weather])

