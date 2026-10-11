import httpx
import pytest

from openf1py import APIError, Position, OpenF1Client

SAMPLE_POSITION = {
    "date": "2023-08-26T09:30:47.199000+00:00",
    "driver_number": 40,
    "meeting_key": 1217,
    "position": 2,
    "session_key": 9144,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_position_returns_position_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_POSITION])

    positions = make_client(handler).position.list(meeting_key=1217)

    assert len(positions) == 1
    assert isinstance(positions[0], Position)
    assert positions[0].driver_number == 40
    assert positions[0].position == 2

def test_list_position_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).position.list(meeting_key=1217, driver_number=40)

    assert captured["path"] == "/v1/position"
    assert captured["params"] == {"meeting_key": "1217", "driver_number": "40"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_POSITION, "brand_new_field": "x"}])

    positions = make_client(handler).position.list()

    assert positions[0].driver_number == 40

def test_list_position_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).position.list()

    assert exc_info.value.status_code == 500
