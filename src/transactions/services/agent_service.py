from agent.tx_agent import TransactionAgent
from schemas.transaction_schemas import TransactionResult


async def build_transaction_service(message: str) -> TransactionResult:
    agent = TransactionAgent()
    response = await agent.process_message(message=message)
    return response
