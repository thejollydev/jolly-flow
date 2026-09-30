"""Where CLIProxyAPI is, and the key it expects.

Both come from the environment, so no key lives in the source:

    CLIPROXY_API_KEY   one of the api-keys in your CLIProxyAPI config
    CLIPROXY_BASE_URL  defaults to http://localhost:8317/v1
"""
import os

DEFAULT_BASE_URL = "http://localhost:8317/v1"


def base_url() -> str:
    return os.environ.get("CLIPROXY_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def api_key() -> str:
    key = os.environ.get("CLIPROXY_API_KEY")
    if not key:
        raise RuntimeError(
            "CLIPROXY_API_KEY is not set. Set it to one of the api-keys in "
            "your CLIProxyAPI config."
        )
    return key
