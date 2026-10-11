from dataclasses import dataclass, fields

@dataclass(frozen=True)
class Driver:
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

    @classmethod
    def from_dict(cls, data: dict) -> "Driver":
        # Keep only keys that we know about, so a new field added by the API won't crash us
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})

@dataclass(frozen=True)
class Sessions:
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

    @classmethod
    def from_dict(cls, data: dict) -> "Sessions":
        # Keep only keys that we know about, so a new field added by the API won't crash us
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})

@dataclass(frozen=True)
class CarData:
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

    @classmethod
    def from_dict(cls, data: dict) -> "CarData":
        # Keep only keys that we know about, so a new field added by the API won't crash us
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})