import time
import hmac
import hashlib
import requests

from config import BYBIT_BASE_URL, get_api_credentials


def _build_signature(timestamp: str, recv_window: str, query_string: str) -> str:
    api_key, api_secret = get_api_credentials()

    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY ou BYBIT_API_SECRET manquant dans le fichier .env")

    payload_to_sign = f"{timestamp}{api_key}{recv_window}{query_string}"

    return hmac.new(
        api_secret.encode("utf-8"),
        payload_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def _build_headers(timestamp: str, recv_window: str, signature: str) -> dict:
    api_key, _ = get_api_credentials()

    if not api_key:
        raise ValueError("BYBIT_API_KEY manquant dans le fichier .env")

    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "X-BAPI-SIGN": signature,
    }


def get_wallet_balance() -> dict:
    endpoint = "/v5/account/wallet-balance"
    url = BYBIT_BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    query_string = "accountType=UNIFIED"

    signature = _build_signature(timestamp, recv_window, query_string)
    headers = _build_headers(timestamp, recv_window, signature)

    response = requests.get(
        url,
        headers=headers,
        params={"accountType": "UNIFIED"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_executions(
    category: str = "linear",
    limit: int = 50,
    start_time: int | None = None,
    end_time: int | None = None
) -> dict:
    endpoint = "/v5/execution/list"
    url = BYBIT_BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    params = {
        "category": category,
        "limit": limit,
    }

    query_parts = [
        f"category={category}",
        f"limit={limit}",
    ]

    if start_time is not None and end_time is not None:
        params["startTime"] = start_time
        params["endTime"] = end_time
        query_parts.append(f"startTime={start_time}")
        query_parts.append(f"endTime={end_time}")

    query_string = "&".join(query_parts)

    signature = _build_signature(timestamp, recv_window, query_string)
    headers = _build_headers(timestamp, recv_window, signature)

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )
    response.raise_for_status()
    return response.json()