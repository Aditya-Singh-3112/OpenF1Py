import httpx
import pytest

from openf1py import APIError, Driver, OpenF1Client

SAMPLE_DRIVER = {
    "broadcast_name": "M VERSTAPPEN",
    "country_code": "NED",
    "driver_number": 1,
    "first_name": "Max",
    "full_name": "Max VERSTAPPEN",
    "headshot_url": "https://example.com/max.png",
    "last_name": "Verstappen",
    "meeting_key": 1219,
    "name_acronym": "VER",
    "session_key": 9158,
    "team_colour": "3671C6",
    "team_name": "Red Bull Racing",
}


def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))


def test_list_drivers_returns_driver_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_DRIVER])

    drivers = make_client(handler).drivers.list(session_key=9158)

    assert len(drivers) == 1
    assert isinstance(drivers[0], Driver)
    assert drivers[0].full_name == "Max VERSTAPPEN"
    assert drivers[0].driver_number == 1


def test_list_drivers_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).drivers.list(session_key=9158, driver_number=1)

    assert captured["path"] == "/v1/drivers"
    assert captured["params"] == {"session_key": "9158", "driver_number": "1"}


def test_unknown_fields_are_ignored():
    def handler(request):
        return httpx.Response(200, json=[{**SAMPLE_DRIVER, "brand_new_field": "x"}])

    drivers = make_client(handler).drivers.list()

    assert drivers[0].name_acronym == "VER"


def test_api_error_raises_custom_exception():
    def handler(request):
        return httpx.Response(500, text="server exploded")

    with pytest.raises(APIError) as exc_info:
        make_client(handler).drivers.list()

    assert exc_info.value.status_code == 500
