import time
import hmac
import hashlib
import requests

from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL


def get_server_time() -> dict:
    """
    Test simple API publique Bybit.
    """
    url = f"{BYBIT_BASE_URL}/v5/market/time"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_wallet_balance() -> dict:
    """
    Test simple API privée Bybit.
    """
    endpoint = "/v5/account/wallet-balance"
    url = BYBIT_BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    query_string = "accountType=UNIFIED"

    payload_to_sign = f"{timestamp}{BYBIT_API_KEY}{recv_window}{query_string}"

    signature = hmac.new(
        BYBIT_API_SECRET.encode("utf-8"),
        payload_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "X-BAPI-SIGN": signature,
    }

    response = requests.get(url, headers=headers, params={"accountType": "UNIFIED"}, timeout=10)
    response.raise_for_status()
    return response.json()