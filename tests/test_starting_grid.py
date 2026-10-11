import httpx
import pytest

from openf1py import APIError, StartingGrid, OpenF1Client

SAMPLE_STARTING_GRID = {
    "position": 1,
    "driver_number": 1,
    "lap_duration": 76.732,
    "meeting_key": 1143,
    "session_key": 7783,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_starting_grid_returns_starting_grid_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_STARTING_GRID])

    grid = make_client(handler).starting_grid.list(session_key=7783)

    assert len(grid) == 1
    assert isinstance(grid[0], StartingGrid)
    assert grid[0].position == 1
    assert grid[0].lap_duration == 76.732

def test_list_starting_grid_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).starting_grid.list(session_key=7783, driver_number=1)

    assert captured["path"] == "/v1/starting_grid"
    assert captured["params"] == {"session_key": "7783", "driver_number": "1"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_STARTING_GRID, "brand_new_field": "x"}])

    grid = make_client(handler).starting_grid.list()

    assert grid[0].position == 1

def test_list_starting_grid_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).starting_grid.list()

    assert exc_info.value.status_code == 500
