from langchain_groq import ChatGroq
from typing import TypedDict

from rag.tools.tools import retrieve_chunks
from rag.prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
import os
from langchain.agents import create_agent

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# Initialize the Groq chat model
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0,api_key=api_key)


class AgentContext(TypedDict):
    user_id: int


agent = create_agent(
    model=model,
    tools=[retrieve_chunks],
    system_prompt=SYSTEM_PROMPT,
    context_schema=AgentContext,
)


def extract_agent_response_content(agent_response: dict) -> str:
    messages = agent_response.get("messages", [])
    if not messages:
        return ""

    content = getattr(messages[-1], "content", messages[-1])
    # if isinstance(content, list):
    #     return "\n".join(
    #         part.get("text", str(part)) if isinstance(part, dict) else str(part)
    #         for part in content
    #     )

    return str(content)

