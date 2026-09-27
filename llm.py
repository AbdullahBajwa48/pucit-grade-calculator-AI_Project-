"""Groq model setup for the PUCIT GPA/CGPA conversational agent."""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY is not set. Put it in a local .env file before running the agent."
    )

llm = init_chat_model("groq:openai/gpt-oss-20b")
