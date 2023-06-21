from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List
import time
from blockchain.solana.lib.config import SOLANA_API_URL
from utils.api_requests import make_request, ReqType


def get_transaction_details(signatures: List[str]):
    transactions = []
    for signature in signatures:
        transaction = _get_transaction(signature)
        if transaction is not None:
            transactions.append(transaction)
        # Sleep for a short amount of time to avoid hitting rate limits
        time.sleep(1)
    return transactions


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def _get_transaction(signature: str):
    # Data parameters
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"maxSupportedTransactionVersion": 0}],
    }

    return make_request(ReqType.POST, SOLANA_API_URL, data)['result']
