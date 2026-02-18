from __future__ import annotations
from typing import Any, Dict, Optional, Union
import requests
from .tokens import OAuth2Token

class Client:
    def __init__(self, base_url: str = "https://example.com") -> None:
        # Simplified type to avoid logic errors with dicts
        self.oauth2_token: Optional[OAuth2Token] = None
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")

    def refresh_oauth2(self) -> None:
        # In a real app, this would be a POST request to an /auth endpoint
        self.oauth2_token = OAuth2Token(access_token="fresh-token", expires_at=10**10)

    def request(
        self,
        method: str,
        path: str,
        *,
        api: bool = False,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,  # Allow passing json, params, etc.
    ) -> Dict[str, Any]:
        if headers is None:
            headers = {}

        if api:
            # Check if token is missing, not the right type, or expired
            if not isinstance(self.oauth2_token, OAuth2Token) or self.oauth2_token.expired:
                self.refresh_oauth2()
            
            # Now we are sure it's an OAuth2Token object
            if self.oauth2_token:
                headers["Authorization"] = self.oauth2_token.as_header()

        url = f"{self.base_url}{path}"
        req = requests.Request(method=method, url=url, headers=headers, **kwargs)
        prepared = self.session.prepare_request(req)
        
        # ACTUALLY send the request
        response = self.session.send(prepared)
        
        # You should probably return response.json() or the response object itself
        return {
            "status_code": response.status_code,
            "method": method,
            "path": path,
            "headers": dict(prepared.headers),
            "data": response.json() if response.ok else None
        }