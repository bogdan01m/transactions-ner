from pydantic import BaseModel

class TransactionModel(BaseModel):
    to:str
    value: float
    gas: int 
    chainId: str

class BaseAIModel(BaseModel):
    response: str

class TransactionData(BaseModel):
    receiver: str
    eth_value: float

class AgentState(BaseModel):
    message: str
    endpoint_url: str
    intent_response: str | None = None
    transaction_data: TransactionData | None = None
    tx: dict | None = None