from __future__ import annotations
from typing import TYPE_CHECKING
from .model import Driver, Sessions, CarData, ChampionshipDriver, ChampionshipTeam, Interval, Lap, Location, Meeting, Overtake, Pit, Position, RaceControl, SessionResult, StartingGrid, Stint, TeamRadio, Weather

if TYPE_CHECKING:
    from .client import OpenF1Client

class DriversResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[Driver]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("drivers", **params)
        return [Driver.from_dict(d) for d in data]

class SessionsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, year: int | None = None, country_name: str | None = None, session_name: str | None = None) -> list[Sessions]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "year": year,
            "country_name": country_name,
            "session_name": session_name,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("sessions", **params)
        return [Sessions.from_dict(d) for d in data]

class CarDataResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[CarData]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("car_data", **params)
        return [CarData.from_dict(d) for d in data]

class DriverChampionshipResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[ChampionshipDriver]:
        params = {
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("championship_drivers", **params)
        return [ChampionshipDriver.from_dict(d) for d in data]

class ChampionshipTeamResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, meeting_key: int | str | None = None, team_name: str | None = None) -> list[ChampionshipTeam]:
        params = {
            "meeting_key": meeting_key,
            "team_name": team_name,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("championship_teams", **params)
        return [ChampionshipTeam.from_dict(d) for d in data]

class IntervalsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[Interval]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("intervals", **params)
        return [Interval.from_dict(d) for d in data]

class LapsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None, lap_number: int | None = None) -> list[Lap]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("laps", **params)
        return [Lap.from_dict(d) for d in data]

class LocationResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[Location]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("location", **params)
        return [Location.from_dict(d) for d in data]

class MeetingsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, meeting_key: int | str | None = None, year: int | None = None, country_name: str | None = None) -> list[Meeting]:
        params = {
            "meeting_key": meeting_key,
            "year": year,
            "country_name": country_name,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("meetings", **params)
        return [Meeting.from_dict(d) for d in data]

class OvertakesResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, overtaking_driver_number: int | None = None, overtaken_driver_number: int | None = None) -> list[Overtake]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "overtaking_driver_number": overtaking_driver_number,
            "overtaken_driver_number": overtaken_driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("overtakes", **params)
        return [Overtake.from_dict(d) for d in data]

class PitResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None, lap_number: int | None = None) -> list[Pit]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("pit", **params)
        return [Pit.from_dict(d) for d in data]

class PositionResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[Position]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("position", **params)
        return [Position.from_dict(d) for d in data]

class RaceControlResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None, category: str | None = None, flag: str | None = None) -> list[RaceControl]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
            "category": category,
            "flag": flag,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("race_control", **params)
        return [RaceControl.from_dict(d) for d in data]

class SessionResultResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[SessionResult]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("session_result", **params)
        return [SessionResult.from_dict(d) for d in data]

class StartingGridResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[StartingGrid]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("starting_grid", **params)
        return [StartingGrid.from_dict(d) for d in data]

class StintsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None, compound: str | None = None) -> list[Stint]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
            "compound": compound,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("stints", **params)
        return [Stint.from_dict(d) for d in data]

class TeamRadioResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[TeamRadio]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("team_radio", **params)
        return [TeamRadio.from_dict(d) for d in data]

class WeatherResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None) -> list[Weather]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("weather", **params)
        return [Weather.from_dict(d) for d in data]
