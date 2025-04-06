import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_openai_llm():
    return ChatOpenAI(
        base_url=os.getenv("LLM_URL","https://openrouter.ai/api/v1"),
        api_key=os.getenv("LLM_API_KEY"),
        model=os.getenv("LLM_MODEL","deepseek/deepseek-chat"),
        temperature=0.5
    )
