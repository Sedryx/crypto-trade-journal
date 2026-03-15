"""Thin wrappers around the Bybit REST API."""

import hashlib
import hmac
import time

import requests

from config import BYBIT_BASE_URL, get_api_credentials


def _build_signature(timestamp: str, recv_window: str, query_string: str) -> str:
    """Build the HMAC signature required by Bybit private endpoints."""
    api_key, api_secret = get_api_credentials()

    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY ou BYBIT_API_SECRET manquant dans le fichier .env")

    payload_to_sign = f"{timestamp}{api_key}{recv_window}{query_string}"
    return hmac.new(
        api_secret.encode("utf-8"),
        payload_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _build_headers(timestamp: str, recv_window: str, signature: str) -> dict:
    """Return authenticated headers for a private Bybit call."""
    api_key, _ = get_api_credentials()

    if not api_key:
        raise ValueError("BYBIT_API_KEY manquant dans le fichier .env")

    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "X-BAPI-SIGN": signature,
    }


def _build_query_string(params: dict) -> str:
    """Serialize query params exactly as expected by the signature payload."""
    parts = []
    for key, value in params.items():
        if value is None:
            continue
        parts.append(f"{key}={value}")
    return "&".join(parts)


def _perform_get(url: str, headers: dict, params: dict, context: str) -> dict:
    """Run one GET request and raise a readable desktop-friendly error on failure."""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as error:
        raise RuntimeError(f"{context}: request timed out.") from error
    except requests.HTTPError as error:
        response = error.response
        details = ""
        if response is not None:
            try:
                payload = response.json()
                details = payload.get("retMsg") or payload.get("message") or ""
            except ValueError:
                details = response.text.strip()
        raise RuntimeError(
            f"{context}: HTTP {response.status_code if response is not None else 'error'}"
            + (f" - {details}" if details else "")
        ) from error
    except requests.RequestException as error:
        raise RuntimeError(f"{context}: network error.") from error


def get_wallet_balance() -> dict:
    """Fetch the unified account wallet payload."""
    endpoint = "/v5/account/wallet-balance"
    url = BYBIT_BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    params = {"accountType": "UNIFIED"}
    query_string = _build_query_string(params)

    signature = _build_signature(timestamp, recv_window, query_string)
    headers = _build_headers(timestamp, recv_window, signature)
    return _perform_get(url, headers, params, "Bybit wallet balance")


def get_executions(
    category: str = "linear",
    limit: int = 50,
    start_time: int | None = None,
    end_time: int | None = None,
    cursor: str | None = None,
) -> dict:
    """Fetch one execution page for a given Bybit category."""
    endpoint = "/v5/execution/list"
    url = BYBIT_BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    params = {
        "category": category,
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time,
        "cursor": cursor,
    }
    query_string = _build_query_string(params)

    signature = _build_signature(timestamp, recv_window, query_string)
    headers = _build_headers(timestamp, recv_window, signature)
    return _perform_get(url, headers, params, f"Bybit executions [{category}]")
