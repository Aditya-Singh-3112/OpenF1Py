import httpx
import pytest
from openf1py import APIError, ChampionshipTeam, OpenF1Client

SAMPLE_TEAM_CHAMPIONSHIP =   {
    "meeting_key": 1276,
    "points_current": 833.0,
    "points_start": 800.0,
    "position_current": 1,
    "position_start": 1,
    "session_key": 9839,
    "team_name": "McLaren"
  }

def make_client(handler) -> OpenF1Client:
    return OpenF1Client(transport=httpx.MockTransport(handler))


def test_list_team_championship_returns_team_championship_objects():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[SAMPLE_TEAM_CHAMPIONSHIP])

    team_championships = make_client(handler).teams_championship.list(meeting_key=1276)

    assert len(team_championships) == 1
    assert isinstance(team_championships[0], ChampionshipTeam)
    assert team_championships[0].meeting_key == 1276
    assert team_championships[0].team_name == "McLaren"

def test_list_team_championship_sends_only_given_filters():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    make_client(handler).teams_championship.list(meeting_key=1276)

    assert captured["path"] == "/v1/championship_teams"
    assert captured["params"] == {"meeting_key": "1276"}

def test_unknown_fields_are_ignored():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{**SAMPLE_TEAM_CHAMPIONSHIP, "brand_new_field": "x"}])

    team_championships = make_client(handler).teams_championship.list()

    assert team_championships[0].meeting_key == 1276
    assert team_championships[0].team_name == "McLaren"

def test_list_team_championship_raises_api_error_on_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    client = make_client(handler)
    with pytest.raises(APIError):
        client.teams_championship.list()