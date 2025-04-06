from web3 import Web3
from schemas.transaction_schemas import TransactionData

def build_eth_transaction(data: TransactionData, endpoint_url: str):
    try: 
        w3 = Web3(Web3.HTTPProvider(endpoint_url))
        wei = w3.to_wei(data.eth_value, "ether")
    
        return {
                "to": data.receiver,
                "value": wei,
                "gas": 21000,
                "chainId": w3.eth.chain_id
            }
    except Exception as e:
        return f"не удалось обработать транзакцию: {e}" 
