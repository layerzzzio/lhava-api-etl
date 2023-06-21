from tenacity import retry, stop_after_attempt, wait_fixed
from blockchain.solana.lib.config import SOLANA_API_URL
from utils.api_requests import make_request, ReqType


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_signatures_for_address(mint_address):
    # Data parameters
    data = {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "getSignaturesForAddress",
      "params": [
          mint_address
      ]
    }

    return make_request(ReqType.POST, SOLANA_API_URL, data)['result']


def extract_signatures(signatures_data):
    return [tx['signature'] for tx in signatures_data]
