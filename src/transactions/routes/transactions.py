from fastapi import APIRouter, HTTPException
from services.transaction_service import create_eth_transaction

router = APIRouter()

@router.get("/create_transaction")
async def create_transaction(endpoint_url:str,receiver: str, eth_value: float, gas_price: float):
    try:
        tx = await create_eth_transaction(endpoint_url,receiver, eth_value, gas_price)
        return {"tx": tx}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
