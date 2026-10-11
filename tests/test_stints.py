import httpx
import pytest

from openf1py import APIError, Stint, OpenF1Client

SAMPLE_STINTS = {
    "compound": "SOFT",
    "driver_number": 16,
    "lap_end": 20,
    "lap_start": 1,
    "meeting_key": 1219,
    "session_key": 9165,
    "stint_number": 1,
    "tyre_age_at_start": 3,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_stints_returns_stints_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_STINTS])

    stints = make_client(handler).stints.list(session_key=9165)

    assert len(stints) == 1
    assert isinstance(stints[0], Stint)
    assert stints[0].compound == "SOFT"
    assert stints[0].stint_number == 1

def test_list_stints_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).stints.list(session_key=9165, compound="SOFT")

    assert captured["path"] == "/v1/stints"
    assert captured["params"] == {"session_key": "9165", "compound": "SOFT"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_STINTS, "brand_new_field": "x"}])

    stints = make_client(handler).stints.list()

    assert stints[0].compound == "SOFT"

def test_list_stints_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).stints.list()

    assert exc_info.value.status_code == 500
