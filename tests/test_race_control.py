import httpx
import pytest

from openf1py import APIError, RaceControl, OpenF1Client

SAMPLE_RACE_CONTROL = {
    "category": "Flag",
    "date": "2023-06-04T14:21:01+00:00",
    "driver_number": 1,
    "flag": "BLACK AND WHITE",
    "lap_number": 59,
    "meeting_key": 1211,
    "message": "BLACK AND WHITE FLAG FOR CAR 1 (VER) - TRACK LIMITS",
    "qualifying_phase": None,
    "scope": "Driver",
    "sector": None,
    "session_key": 9102,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_race_control_returns_race_control_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_RACE_CONTROL])

    messages = make_client(handler).race_control.list(driver_number=1)

    assert len(messages) == 1
    assert isinstance(messages[0], RaceControl)
    assert messages[0].flag == "BLACK AND WHITE"
    assert messages[0].lap_number == 59

def test_list_race_control_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).race_control.list(driver_number=1, flag="BLACK AND WHITE")

    assert captured["path"] == "/v1/race_control"
    assert captured["params"] == {"driver_number": "1", "flag": "BLACK AND WHITE"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_RACE_CONTROL, "brand_new_field": "x"}])

    messages = make_client(handler).race_control.list()

    assert messages[0].flag == "BLACK AND WHITE"

def test_list_race_control_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).race_control.list()

    assert exc_info.value.status_code == 500
