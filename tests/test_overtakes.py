import httpx
import pytest

from openf1py import APIError, Overtake, OpenF1Client

SAMPLE_OVERTAKES = {
    "date": "2024-11-03T15:50:07.565000+00:00",
    "meeting_key": 1249,
    "overtaken_driver_number": 4,
    "overtaking_driver_number": 63,
    "position": 1,
    "session_key": 9636,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_overtakes_returns_overtakes_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_OVERTAKES])

    overtakes = make_client(handler).overtakes.list(session_key=9636)

    assert len(overtakes) == 1
    assert isinstance(overtakes[0], Overtake)
    assert overtakes[0].overtaking_driver_number == 63
    assert overtakes[0].overtaken_driver_number == 4

def test_list_overtakes_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).overtakes.list(session_key=9636, overtaking_driver_number=63, overtaken_driver_number=4)

    assert captured["path"] == "/v1/overtakes"
    assert captured["params"] == {"session_key": "9636", "overtaking_driver_number": "63", "overtaken_driver_number": "4"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_OVERTAKES, "brand_new_field": "x"}])

    overtakes = make_client(handler).overtakes.list()

    assert overtakes[0].overtaking_driver_number == 63

def test_list_overtakes_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).overtakes.list()

    assert exc_info.value.status_code == 500
