import httpx
import pytest

from openf1py import APIError, Pit, OpenF1Client

SAMPLE_PIT = {
    "date": "2025-10-26T20:46:37.358000+00:00",
    "driver_number": 16,
    "lane_duration": 22.215,
    "lap_number": 31,
    "meeting_key": 1272,
    "session_key": 9877,
    "stop_duration": 2.2,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_pit_returns_pit_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_PIT])

    pit_stops = make_client(handler).pit.list(session_key=9877)

    assert len(pit_stops) == 1
    assert isinstance(pit_stops[0], Pit)
    assert pit_stops[0].driver_number == 16
    assert pit_stops[0].stop_duration == 2.2

def test_list_pit_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).pit.list(session_key=9877, driver_number=16, lap_number=31)

    assert captured["path"] == "/v1/pit"
    assert captured["params"] == {"session_key": "9877", "driver_number": "16", "lap_number": "31"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_PIT, "brand_new_field": "x"}])

    pit_stops = make_client(handler).pit.list()

    assert pit_stops[0].driver_number == 16

def test_list_pit_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).pit.list()

    assert exc_info.value.status_code == 500
