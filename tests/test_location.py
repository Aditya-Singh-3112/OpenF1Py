import httpx
import pytest

from openf1py import APIError, Location, OpenF1Client

SAMPLE_LOCATION = {
    "date": "2023-09-16T13:03:35.292000+00:00",
    "driver_number": 81,
    "meeting_key": 1219,
    "session_key": 9161,
    "x": 567,
    "y": 3195,
    "z": 187,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_location_returns_location_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_LOCATION])

    locations = make_client(handler).location.list(session_key=9161, driver_number=81)

    assert len(locations) == 1
    assert isinstance(locations[0], Location)
    assert locations[0].driver_number == 81
    assert locations[0].x == 567

def test_list_location_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).location.list(session_key=9161, driver_number=81)

    assert captured["path"] == "/v1/location"
    assert captured["params"] == {"session_key": "9161", "driver_number": "81"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_LOCATION, "brand_new_field": "x"}])

    locations = make_client(handler).location.list()

    assert locations[0].driver_number == 81

def test_list_location_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).location.list()

    assert exc_info.value.status_code == 500
