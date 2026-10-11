import httpx
import pytest

from openf1py import APIError, OpenF1Client

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_no_results_returns_empty_list():
    # This is the real response OpenF1 sends when a query matches nothing
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "No results found."})

    assert make_client(handler).drivers.list(session_key=9158, driver_number=999) == []

def test_other_404_still_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "Something else went wrong."})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).drivers.list()

    assert exc_info.value.status_code == 404

def test_404_without_json_still_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="<html>Not Found</html>")

    with pytest.raises(APIError):
        make_client(handler).drivers.list()

def test_401_during_live_session_still_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"detail": "Live F1 session in progress."})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).drivers.list()

    assert exc_info.value.status_code == 401
