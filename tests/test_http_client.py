import time
import pytest
import requests
from unittest.mock import MagicMock
from app.http_client import Client
from app.tokens import OAuth2Token, token_from_iso

def test_client_uses_requests_session():
    c = Client()
    assert isinstance(c.session, requests.Session)

def test_token_from_iso_uses_dateutil():
    t = token_from_iso("ok", "2099-01-01T00:00:00Z")
    assert isinstance(t, OAuth2Token)
    assert t.access_token == "ok"
    assert not t.expired

def test_api_request_sets_auth_header_when_token_is_valid(monkeypatch):
    c = Client()
    # Mock the session.send so we don't actually hit the internet
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    monkeypatch.setattr(c.session, "send", lambda x: mock_response)

    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)
    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer ok"

def test_api_request_refreshes_when_token_is_missing(monkeypatch):
    c = Client()
    # Mock the session.send
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    monkeypatch.setattr(c.session, "send", lambda x: mock_response)
    
    c.oauth2_token = None
    resp = c.request("GET", "/me", api=True)

    # This confirms refresh_oauth2() was called internally
    assert resp["headers"].get("Authorization") == "Bearer fresh-token"

def test_api_request_refreshes_when_token_is_dict(monkeypatch):
    c = Client()
    # Mock the session.send
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    monkeypatch.setattr(c.session, "send", lambda x: mock_response)
    
    # Simulate the bug where oauth2_token is a dict
    c.oauth2_token = {"access_token": "stale", "expires_at": 0}
    
    # This should trigger refresh_oauth2 because it's not an OAuth2Token or it's "missing/expired"
    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"