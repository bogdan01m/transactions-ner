from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from agent.prompts import BasePrompt, TransactAIModelPrompt
from schemas.transaction_schemas import AgentState, TransactionData
from agent.llm_config import get_openai_llm
from agent.tools import build_eth_transaction
import json

class TransactionAgent:
    def __init__(self):
        self.llm = get_openai_llm()
        self.graph = self._build_graph()

    def _check_intent(self, state: dict) -> dict:
        prompt = ChatPromptTemplate.from_template(BasePrompt)
        message = state['message']
        response = self.llm.invoke(prompt.format(message=message)).content.strip()
        return {"intent_response": response}

    def _extract_entities(self, state: dict) -> dict:
        prompt = ChatPromptTemplate.from_template(TransactAIModelPrompt)
        response = self.llm.invoke(prompt.format(message=state['message'])).content.strip()

        try:
            json_data = json.loads(response)
        except:
            json_data = eval(response)
        
        tx_data = TransactionData(**json_data)
        return {"transaction_data": tx_data}

    def _build_transaction(self, state: dict) -> dict:
        tx = build_eth_transaction(state["transaction_data"], state["endpoint_url"])
        return {"tx": tx}

    def _reject(self, state: dict) -> dict:
        return {"error": "Sorry, we couldn't understand your intent."}

    def _build_graph(self):
        builder = StateGraph()

        builder.add_node("CheckIntent", self._check_intent)
        builder.add_node("ExtractEntities", self._extract_entities)
        builder.add_node("BuildTransaction", self._build_transaction)
        builder.add_node("Reject", self._reject)

        builder.set_entry_point("CheckIntent")

        def router(state):
            if "@BuildTransaction" in state["intent_response"]:
                return "ExtractEntities"
            return "Reject"

        builder.add_conditional_edges("CheckIntent", router)
        builder.add_edge("ExtractEntities", "BuildTransaction")
        builder.add_edge("BuildTransaction", END)
        builder.add_edge("Reject", END)

        return builder.compile()

    def run(self, message: str, endpoint_url: str) -> dict:
        input_state = {
            "message": message,
            "endpoint_url": endpoint_url
        }
        return self.graph.invoke(input_state)
