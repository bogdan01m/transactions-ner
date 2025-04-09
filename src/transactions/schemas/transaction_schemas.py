from pydantic import BaseModel
from typing import Optional, Literal


class TransactionNER(BaseModel):
    receiver: str
    value: float


class SupervisorResponse(BaseModel):
    decision: Literal["@BuildTransaction", "@RejectTransaction"]  
    reasoning: str


class TransactionDict(BaseModel):
    to: str
    value: float


class TransactionResult(BaseModel):
    status: str
    transaction: Optional[TransactionDict] = None
    reasoning: str
