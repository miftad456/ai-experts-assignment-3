from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from dateutil.parser import isoparse

@dataclass
class OAuth2Token:
    access_token: str
    expires_at: int  # Unix timestamp

    @property
    def expired(self) -> bool:
        # Buffer of 10 seconds to account for network latency
        buffer = 10 
        return datetime.now(tz=timezone.utc).timestamp() + buffer >= self.expires_at

    def as_header(self) -> str:
        return f"Bearer {self.access_token}"

def token_from_iso(access_token: str, expires_at_iso: str) -> OAuth2Token:
    dt = isoparse(expires_at_iso)
    
    # Ensure it's treated as UTC if no TZ is provided, 
    # but convert to UTC if another TZ is provided.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
        
    return OAuth2Token(access_token=access_token, expires_at=int(dt.timestamp()))