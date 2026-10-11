import httpx
import pytest

from openf1py import APIError, Lap, OpenF1Client

SAMPLE_LAPS = {
    "date_start": "2023-09-16T13:59:07.606000+00:00",
    "driver_number": 63,
    "duration_sector_1": 26.966,
    "duration_sector_2": 38.657,
    "duration_sector_3": 26.12,
    "i1_speed": 307,
    "i2_speed": 277,
    "is_pit_out_lap": False,
    "lap_duration": 91.743,
    "lap_number": 8,
    "meeting_key": 1219,
    "segments_sector_1": [2049, 2049, 2049, 2051, 2049, 2051, 2049, 2049],
    "segments_sector_2": [2049, 2049, 2049, 2049, 2049, 2049, 2049, 2049],
    "segments_sector_3": [2048, 2048, 2048, 2048, 2048, 2064, 2064, 2064],
    "session_key": 9161,
    "st_speed": 298,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_laps_returns_laps_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_LAPS])

    laps = make_client(handler).laps.list(session_key=9161, driver_number=63)

    assert len(laps) == 1
    assert isinstance(laps[0], Lap)
    assert laps[0].lap_number == 8
    assert laps[0].lap_duration == 91.743

def test_list_laps_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).laps.list(session_key=9161, driver_number=63, lap_number=8)

    assert captured["path"] == "/v1/laps"
    assert captured["params"] == {"session_key": "9161", "driver_number": "63", "lap_number": "8"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_LAPS, "brand_new_field": "x"}])

    laps = make_client(handler).laps.list()

    assert laps[0].lap_number == 8

def test_list_laps_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).laps.list()

    assert exc_info.value.status_code == 500
