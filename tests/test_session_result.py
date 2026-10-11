import httpx
import pytest

from openf1py import APIError, SessionResult, OpenF1Client

SAMPLE_SESSION_RESULT = {
    "dnf": False,
    "dns": False,
    "dsq": False,
    "driver_number": 1,
    "duration": 77.565,
    "gap_to_leader": 0,
    "number_of_laps": 24,
    "meeting_key": 1143,
    "position": 1,
    "session_key": 7782,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_session_result_returns_session_result_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_SESSION_RESULT])

    results = make_client(handler).session_result.list(session_key=7782)

    assert len(results) == 1
    assert isinstance(results[0], SessionResult)
    assert results[0].position == 1
    assert results[0].duration == 77.565

def test_list_session_result_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).session_result.list(session_key=7782, driver_number=1)

    assert captured["path"] == "/v1/session_result"
    assert captured["params"] == {"session_key": "7782", "driver_number": "1"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_SESSION_RESULT, "brand_new_field": "x"}])

    results = make_client(handler).session_result.list()

    assert results[0].position == 1

def test_list_session_result_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).session_result.list()

    assert exc_info.value.status_code == 500
