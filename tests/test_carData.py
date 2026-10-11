import httpx
import pytest

from openf1py import APIError, CarData, OpenF1Client

SAMPLE_CAR_DATA = {
    "brake": 0,
    "date": "2023-09-15T13:08:19.923000+00:00",
    "driver_number": 55,
    "drs": 12,
    "meeting_key": 1219,
    "n_gear": 8,
    "rpm": 11141,
    "session_key": 9159,
    "speed": 315,
    "throttle": 99
  }

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_car_data_returns_car_data_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_CAR_DATA])

    car_data_list = make_client(handler).car_data.list(session_key=9159)

    assert len(car_data_list) == 1
    assert isinstance(car_data_list[0], CarData)
    assert car_data_list[0].session_key == 9159
    assert car_data_list[0].driver_number == 55

def test_list_car_data_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).car_data.list(session_key=9158, driver_number=55)

    assert captured["path"] == "/v1/car_data"
    assert captured["params"] == {"session_key": "9158", "driver_number": "55"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_CAR_DATA, "brand_new_field": "x"}])

    car_data_list = make_client(handler).car_data.list()

    assert car_data_list[0].session_key == 9159
    assert car_data_list[0].driver_number == 55

def test_list_car_data_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    client = make_client(handler)

    with pytest.raises(APIError) as exc_info:
        client.car_data.list(session_key=9159)

    assert exc_info.value.status_code == 500
    assert "Internal Server Error" in str(exc_info.value)