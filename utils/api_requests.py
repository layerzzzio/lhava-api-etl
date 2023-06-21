import requests
import json
import logging
from enum import Enum


class ReqType(Enum):
    GET = 'get'
    POST = 'post'


def make_request(req_type: ReqType, url: str, data: dict):
    # Make the request
    try:
        if req_type == ReqType.GET:
            response = requests.get(url)
        elif req_type == ReqType.POST:
            response = requests.post(url, json=data)
        else:
            logging.error(f"Unsupported CRUD operation: {req_type.value}")
            raise ValueError(f"Unsupported CRUD operation: {req_type.value}")

        # Check response status
        response.raise_for_status()
        result = response.json()

        # Validate JSON response
        if 'error' in result:
            logging.error(f"API responded with error: {result['error']}")
            raise ValueError("API error")

        return result

    except (requests.exceptions.RequestException, ValueError) as err:
        logging.error(f"Error occurred: {err}")
        raise SystemExit(err)
