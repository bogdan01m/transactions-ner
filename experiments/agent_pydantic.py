from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os 
from dotenv import load_dotenv

load_dotenv()

model = OpenAIModel(
    model_name=os.getenv("DEEPSEEK"),
    provider=OpenAIProvider(   
    base_url=os.getenv("LLM_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),)
)

agent = Agent(model)
result = agent.run_sync('Привет, а сколько у тебя параметров, сколько языков ты знаешь и что ты за модель?')
print(result.data)