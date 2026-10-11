import httpx
import pytest

from openf1py import APIError, TeamRadio, OpenF1Client

SAMPLE_TEAM_RADIO = {
    "date": "2023-09-15T09:40:43.005000+00:00",
    "driver_number": 11,
    "meeting_key": 1219,
    "recording_url": "https://livetiming.formula1.com/static/2023/2023-09-17_Singapore_Grand_Prix/2023-09-15_Practice_1/TeamRadio/SERPER01_11_20230915_104008.mp3",
    "session_key": 9158,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_team_radio_returns_team_radio_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_TEAM_RADIO])

    radios = make_client(handler).team_radio.list(session_key=9158)

    assert len(radios) == 1
    assert isinstance(radios[0], TeamRadio)
    assert radios[0].driver_number == 11
    assert radios[0].recording_url == "https://livetiming.formula1.com/static/2023/2023-09-17_Singapore_Grand_Prix/2023-09-15_Practice_1/TeamRadio/SERPER01_11_20230915_104008.mp3"

def test_list_team_radio_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).team_radio.list(session_key=9158, driver_number=11)

    assert captured["path"] == "/v1/team_radio"
    assert captured["params"] == {"session_key": "9158", "driver_number": "11"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_TEAM_RADIO, "brand_new_field": "x"}])

    radios = make_client(handler).team_radio.list()

    assert radios[0].driver_number == 11

def test_list_team_radio_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).team_radio.list()

    assert exc_info.value.status_code == 500
