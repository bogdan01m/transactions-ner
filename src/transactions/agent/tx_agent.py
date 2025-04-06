from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from schemas.transaction_schemas import (
    TransactionNER,
    SupervisorResponse,
    TransactionResult,
    TransactionDict,
)
from agent.prompts import SupervisorPrompt, TransactionNERPrompt
import os
from dotenv import load_dotenv
import logfire

load_dotenv()

logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
logfire.instrument()


class TransactionAgent:
    def __init__(self):

        self.model = MistralModel(
            model_name=os.getenv("MISTRAL"),
            provider=MistralProvider(
                # base_url=os.getenv("LLM_URL"),
                api_key=os.getenv("MISTRAL_API_KEY"),
            ),
        )

        self.supervisor = Agent(
            self.model,
            result_type=SupervisorResponse,
            system_prompt=SupervisorPrompt,
            retries=5,
            instrument=True,
        )
        self.ner_agent = Agent(
            self.model,
            result_type=TransactionNER,
            system_prompt=TransactionNERPrompt,
            retries=5,
            instrument=True,
        )

    async def process_message(self, message: str):
        decision_response = await self.supervisor.run(user_prompt=message)
        decision = decision_response.data

        if decision.decision == "@BuildTransaction":
            ner_response = await self.ner_agent.run(user_prompt=message)
            ner = ner_response.data
            transaction = TransactionDict(to=ner.receiver, value=ner.value)
            return TransactionResult(
                status="Build", transaction=transaction, reasoning=decision.reasoning
            )
        else:
            return TransactionResult(status="Reject", reasoning=decision.reasoning)
