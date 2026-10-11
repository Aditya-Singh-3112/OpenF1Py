import httpx
import pytest

from openf1py import APIError, ChampionshipDriver, OpenF1Client

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

SAMPLE_DRIVER_CHAMPIONSHIP = {
    "driver_number": 4,
    "meeting_key": 1276,
    "points_current": 423.0,
    "points_start": 408.0,
    "position_current": 1,
    "position_start": 1,
    "session_key": 9839
  }

def test_list_driver_championship_returns_driver_championship_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_DRIVER_CHAMPIONSHIP])

    driver_championships = make_client(handler).drivers_championship.list(driver_number=4, meeting_key=1276)

    assert len(driver_championships) == 1
    assert isinstance(driver_championships[0], ChampionshipDriver)
    assert driver_championships[0].meeting_key == 1276
    assert driver_championships[0].driver_number == 4

def test_list_driver_championship_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).drivers_championship.list(driver_number=4, meeting_key=1276)

    assert captured["path"] == "/v1/championship_drivers"
    assert captured["params"] == {"driver_number": "4", "meeting_key": "1276"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_DRIVER_CHAMPIONSHIP, "brand_new_field": "x"}])

    driver_championships = make_client(handler).drivers_championship.list()

    assert driver_championships[0].meeting_key == 1276
    assert driver_championships[0].driver_number == 4

def test_list_driver_championship_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    client = make_client(handler)
    with pytest.raises(APIError):
        client.drivers_championship.list()