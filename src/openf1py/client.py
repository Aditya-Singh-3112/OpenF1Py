import httpx
from .exceptions import APIError
from .resources import (
    ChampionshipTeamResource, DriversResource, SessionsResource, CarDataResource, DriverChampionshipResource,
    IntervalsResource, LapsResource, LocationResource, MeetingsResource, OvertakesResource, PitResource, PositionResource,
    RaceControlResource, SessionResultResource, StartingGridResource, StintsResource, TeamRadioResource, WeatherResource,
)

class OpenF1Client:
    BASE_URL = "https://api.openf1.org/v1"

    def __init__(self, token: str | None = None, 
                 timeout: float = 30.0,
                 transport: httpx.BaseTransport | None = None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._http = httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=timeout, transport=transport)
        self.drivers = DriversResource(self)
        self.sessions = SessionsResource(self)
        self.car_data = CarDataResource(self)
        self.drivers_championship = DriverChampionshipResource(self)
        self.teams_championship = ChampionshipTeamResource(self)
        self.intervals = IntervalsResource(self)
        self.laps = LapsResource(self)
        self.location = LocationResource(self)
        self.meetings = MeetingsResource(self)
        self.overtakes = OvertakesResource(self)
        self.pit = PitResource(self)
        self.position = PositionResource(self)
        self.race_control = RaceControlResource(self)
        self.session_result = SessionResultResource(self)
        self.starting_grid = StartingGridResource(self)
        self.stints = StintsResource(self)
        self.team_radio = TeamRadioResource(self)
        self.weather = WeatherResource(self)

    def get(self, endpoint: str, **params) -> list[dict]:
        response = self._http.get(f"/{endpoint}", params=params)
        if self._is_no_results(response):
            return []
        if response.is_error:
            raise APIError(response.status_code, response.text)
        return response.json()

    @staticmethod
    def _is_no_results(response: httpx.Response) -> bool:
        # OpenF1 answers a query that matches nothing with a 404 instead of an empty list
        if response.status_code != 404:
            return False
        try:
            return response.json().get("detail") == "No results found."
        except ValueError:
            return False

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()