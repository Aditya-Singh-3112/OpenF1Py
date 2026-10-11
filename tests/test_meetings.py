import httpx
import pytest

from openf1py import APIError, Meeting, OpenF1Client

SAMPLE_MEETINGS = {
    "circuit_key": 61,
    "circuit_info_url": "https://api.multiviewer.app/api/v1/circuits/61/2026",
    "circuit_image": "https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Singapore%20carbon.png",
    "circuit_short_name": "Singapore",
    "circuit_type": "Temporary - Street",
    "country_code": "SGP",
    "country_flag": "https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/Flags%2016x9/singapore-flag.png",
    "country_key": 157,
    "country_name": "Singapore",
    "date_end": "2026-10-11T14:00:00+00:00",
    "date_start": "2026-10-09T09:30:00+00:00",
    "gmt_offset": "08:00:00",
    "is_cancelled": False,
    "location": "Marina Bay",
    "meeting_key": 1296,
    "meeting_name": "Singapore Grand Prix",
    "meeting_official_name": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2026",
    "year": 2026,
}

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))

def test_list_meetings_returns_meetings_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_MEETINGS])

    meetings = make_client(handler).meetings.list(year=2026)

    assert len(meetings) == 1
    assert isinstance(meetings[0], Meeting)
    assert meetings[0].meeting_name == "Singapore Grand Prix"
    assert meetings[0].circuit_short_name == "Singapore"

def test_list_meetings_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).meetings.list(year=2026, country_name="Singapore")

    assert captured["path"] == "/v1/meetings"
    assert captured["params"] == {"year": "2026", "country_name": "Singapore"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_MEETINGS, "brand_new_field": "x"}])

    meetings = make_client(handler).meetings.list()

    assert meetings[0].meeting_name == "Singapore Grand Prix"

def test_list_meetings_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    with pytest.raises(APIError) as exc_info:
        make_client(handler).meetings.list()

    assert exc_info.value.status_code == 500
