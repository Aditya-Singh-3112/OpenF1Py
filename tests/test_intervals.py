import httpx
import pytest

from openf1py import APIError, Interval, OpenF1Client

SAMPLE_INTERVALS = {
    "date": "2023-09-17T13:31:02.395000+00:00",
    "driver_number": 1,
    "gap_to_leader": 41.019,
    "interval": 0.003,
    "meeting_key": 1219,
    "session_key": 9165,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_intervals_returns_intervals_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_INTERVALS])

    intervals = make_client(handler).intervals.list(session_key=9165)

    assert len(intervals) == 1
    assert isinstance(intervals[0], Interval)
    assert intervals[0].driver_number == 1
    assert intervals[0].gap_to_leader == 41.019

def test_list_intervals_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).intervals.list(session_key=9165, driver_number=1)

    assert captured["path"] == "/v1/intervals"
    assert captured["params"] == {"session_key": "9165", "driver_number": "1"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_INTERVALS, "brand_new_field": "x"}])

    intervals = make_client(handler).intervals.list()

    assert intervals[0].driver_number == 1

def test_list_intervals_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).intervals.list()

    assert exc_info.value.status_code == 500
