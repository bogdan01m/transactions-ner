import os

import logfire
from dotenv import load_dotenv
from prompts import SupervisorPrompt, TransactAIModelPrompt
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from schemas import (
    SupervisorResponse,
    TransactionDict,
    TransactionNER,
    TransactionResult,
)

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
            retries=3,
            instrument=True,
        )
        self.ner_agent = Agent(
            self.model,
            result_type=TransactionNER,
            system_prompt=TransactAIModelPrompt,
            retries=3,
            instrument=True,
        )

    def process_message(self, message: str):
        decision = self.supervisor.run_sync(user_prompt=message).data

        if decision.decision == "@BuildTransaction":
            ner = self.ner_agent.run_sync(user_prompt=message).data
            transaction = TransactionDict(to=ner.receiver, value=ner.value)
            return TransactionResult(
                status="Build", transaction=transaction, reasoning=decision.reasoning
            )

        else:
            return TransactionResult(status="Reject", reasoning=decision.reasoning)


agent = TransactionAgent()
msg = "отправь моему другу Ивану Иванову 0001 ETH"
res = agent.process_message(msg)
print(res)
print({"to": res.transaction.to, "value": res.transaction.value})
