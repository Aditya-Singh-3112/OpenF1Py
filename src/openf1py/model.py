from dataclasses import dataclass, fields
from typing import TypeVar

T = TypeVar("T", bound="OpenF1Model")


class OpenF1Model:
    """Base class for all models returned by the API."""

    @classmethod
    def from_dict(cls: type[T], data: dict) -> T:
        # Unknown keys are ignored so a new API field won't crash us,
        # and missing keys become None so an absent field won't crash us either
        return cls(**{f.name: data.get(f.name) for f in fields(cls)})

@dataclass(frozen=True)
class Driver(OpenF1Model):
    driver_number: int
    broadcast_name: str
    full_name: str
    first_name: str | None
    last_name: str | None
    name_acronym: str
    team_name: str | None
    team_colour: str | None
    country_code: str | None
    headshot_url: str | None
    meeting_key: int
    session_key: int

@dataclass(frozen=True)
class Sessions(OpenF1Model):
    circuit_key: int
    circuit_short_name: str
    country_code: str | None
    country_key: int | None
    country_name: str
    date_end: str | None
    date_start: str | None
    gmt_offset: str | None
    is_cancelled: bool | None
    location: str | None
    meeting_key: int
    session_key: int
    session_name: str
    session_type: str
    year: int

@dataclass(frozen=True)
class CarData(OpenF1Model):
    brake: int | None
    date: str | None
    driver_number: int
    drs: int | None
    meeting_key: int
    n_gear: int | None
    rpm: int | None
    session_key: int
    speed: int
    throttle: int | None

@dataclass(frozen=True)
class ChampionshipDriver(OpenF1Model):
    driver_number: int
    meeting_key: int
    points_current: float
    points_start: float
    position_current: int
    position_start: int
    session_key: int

@dataclass(frozen=True)
class ChampionshipTeam(OpenF1Model):
    meeting_key: int
    points_current: float
    points_start: float
    position_current: int
    position_start: int
    session_key: int
    team_name: str

@dataclass(frozen=True)
class Interval(OpenF1Model):
    date: str
    driver_number: int
    # Seconds, "+1 LAP" if lapped, or None for the race leader
    gap_to_leader: float | str | None
    interval: float | str | None
    meeting_key: int
    session_key: int

@dataclass(frozen=True)
class Lap(OpenF1Model):
    date_start: str | None
    driver_number: int
    duration_sector_1: float | None
    duration_sector_2: float | None
    duration_sector_3: float | None
    i1_speed: int | None
    i2_speed: int | None
    is_pit_out_lap: bool
    lap_duration: float | None
    lap_number: int
    meeting_key: int
    segments_sector_1: list[int | None] | None
    segments_sector_2: list[int | None] | None
    segments_sector_3: list[int | None] | None
    session_key: int
    st_speed: int | None

@dataclass(frozen=True)
class Location(OpenF1Model):
    date: str
    driver_number: int
    meeting_key: int
    session_key: int
    x: int
    y: int
    z: int

@dataclass(frozen=True)
class Meeting(OpenF1Model):
    circuit_image: str | None
    circuit_info_url: str | None
    circuit_key: int
    circuit_short_name: str
    circuit_type: str | None
    country_code: str | None
    country_flag: str | None
    country_key: int | None
    country_name: str
    date_end: str | None
    date_start: str | None
    gmt_offset: str | None
    is_cancelled: bool | None
    location: str | None
    meeting_key: int
    meeting_name: str
    meeting_official_name: str | None
    year: int

@dataclass(frozen=True)
class Overtake(OpenF1Model):
    date: str
    meeting_key: int
    overtaken_driver_number: int
    overtaking_driver_number: int
    position: int
    session_key: int

@dataclass(frozen=True)
class Pit(OpenF1Model):
    date: str
    driver_number: int
    lane_duration: float | None
    lap_number: int
    meeting_key: int
    session_key: int
    # Only available from the 2024 US GP onwards
    stop_duration: float | None

@dataclass(frozen=True)
class Position(OpenF1Model):
    date: str
    driver_number: int
    meeting_key: int
    position: int
    session_key: int

@dataclass(frozen=True)
class RaceControl(OpenF1Model):
    category: str
    date: str
    driver_number: int | None
    flag: str | None
    lap_number: int | None
    meeting_key: int
    message: str
    qualifying_phase: int | None
    scope: str | None
    sector: int | None
    session_key: int

@dataclass(frozen=True)
class SessionResult(OpenF1Model):
    dnf: bool
    dns: bool
    dsq: bool
    driver_number: int
    # In qualifying these are lists of three values (Q1, Q2, Q3)
    duration: float | list[float | None] | None
    gap_to_leader: float | str | list[float | str | None] | None
    meeting_key: int
    number_of_laps: int | None
    position: int | None
    session_key: int

@dataclass(frozen=True)
class StartingGrid(OpenF1Model):
    driver_number: int
    lap_duration: float | None
    meeting_key: int
    position: int
    session_key: int

@dataclass(frozen=True)
class Stint(OpenF1Model):
    compound: str | None
    driver_number: int
    lap_end: int | None
    lap_start: int | None
    meeting_key: int
    session_key: int
    stint_number: int
    tyre_age_at_start: int | None

@dataclass(frozen=True)
class TeamRadio(OpenF1Model):
    date: str
    driver_number: int
    meeting_key: int
    recording_url: str
    session_key: int

@dataclass(frozen=True)
class Weather(OpenF1Model):
    air_temperature: float
    date: str
    humidity: float
    meeting_key: int
    pressure: float
    rainfall: int
    session_key: int
    track_temperature: float
    wind_direction: int
    wind_speed: float
