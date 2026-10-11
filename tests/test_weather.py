import httpx
import pytest

from openf1py import APIError, Weather, OpenF1Client

SAMPLE_WEATHER = {
    "air_temperature": 27.8,
    "date": "2023-05-07T18:42:25.233000+00:00",
    "humidity": 58,
    "meeting_key": 1208,
    "pressure": 1018.7,
    "rainfall": 0,
    "session_key": 9078,
    "track_temperature": 52.5,
    "wind_direction": 136,
    "wind_speed": 2.4,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_weather_returns_weather_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_WEATHER])

    weather_list = make_client(handler).weather.list(meeting_key=1208)

    assert len(weather_list) == 1
    assert isinstance(weather_list[0], Weather)
    assert weather_list[0].track_temperature == 52.5
    assert weather_list[0].humidity == 58

def test_list_weather_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).weather.list(meeting_key=1208, session_key=9078)

    assert captured["path"] == "/v1/weather"
    assert captured["params"] == {"meeting_key": "1208", "session_key": "9078"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_WEATHER, "brand_new_field": "x"}])

    weather_list = make_client(handler).weather.list()

    assert weather_list[0].track_temperature == 52.5

def test_list_weather_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).weather.list()

    assert exc_info.value.status_code == 500
