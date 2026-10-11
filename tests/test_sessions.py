import httpx
import pytest

from openf1py import APIError, Sessions, OpenF1Client

SAMPLE_SESSION = {
    "circuit_key": 7,
    "circuit_short_name": "Spa-Francorchamps",
    "country_code": "BEL",
    "country_key": 16,
    "country_name": "Belgium",
    "date_end": "2023-07-29T15:35:00+00:00",
    "date_start": "2023-07-29T15:05:00+00:00",
    "gmt_offset": "02:00:00",
    "is_cancelled": False,
    "location": "Spa-Francorchamps",
    "meeting_key": 1216,
    "session_key": 9140,
    "session_name": "Sprint Qualifying",
    "session_type": "Sprint Qualifying",
    "year": 2023
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_sessions_returns_session_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json = [SAMPLE_SESSION])

    sessions = make_client(handler).sessions.list(meeting_key = 1216)

    assert len(sessions) == 1
    assert isinstance(sessions[0], Sessions)
    assert sessions[0].session_name == "Sprint Qualifying"
    assert sessions[0].session_key == 9140

def test_list_sessions_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).sessions.list(meeting_key=1216, year=2023, country_name="Belgium", session_name="Sprint Qualifying")

    assert captured["path"] == "/v1/sessions"
    assert captured["params"] == {"meeting_key": "1216", "year": "2023", "country_name": "Belgium", "session_name": "Sprint Qualifying"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_SESSION, "brand_new_field": "x"}])

    sessions = make_client(handler).sessions.list()

    assert sessions[0].session_name == "Sprint Qualifying"

def test_list_sessions_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    client = make_client(handler)
    with pytest.raises(APIError):
        client.sessions.list()