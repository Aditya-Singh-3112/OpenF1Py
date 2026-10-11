# openf1py

A Python client for the [OpenF1 API](https://openf1.org): free, real-time and historical Formula 1 data.

```python
from openf1py import OpenF1Client

with OpenF1Client() as f1:
    for driver in f1.drivers.list(session_key="latest"):
        print(driver.name_acronym, driver.team_name)
```

Each API record becomes a typed Python object, so you can write `driver.team_name` instead of `driver["team_name"]` and your editor can autocomplete it.

## Installation

Requires Python 3.10 or later.

openf1py is not on PyPI yet. Install it from a local copy of the source:

```bash
git clone <repository-url>
cd OpenF1
pip install -e .
```

The only dependency is [httpx](https://www.python-httpx.org/).

## Usage

### Creating a client

Use the client as a context manager so its connection closes automatically:

```python
from openf1py import OpenF1Client

with OpenF1Client() as f1:
    ...
```

If you don't use `with`, call `f1.close()` when you're done.

The client takes three optional arguments:

| Argument | Default | Description |
|---|---|---|
| `token` | `None` | Your OpenF1 API key, sent as a Bearer token. Not needed for most use. |
| `timeout` | `30.0` | How many seconds to wait for a response. |
| `transport` | `None` | A custom httpx transport, mainly used for testing. |

### Querying an endpoint

Every endpoint is an attribute on the client, and each one has a `list()` method. Filters are keyword arguments, and any filter you leave out isn't sent:

```python
with OpenF1Client() as f1:
    # All sessions of the 2023 Singapore Grand Prix
    sessions = f1.sessions.list(year=2023, country_name="Singapore")

    for s in sessions:
        print(s.session_key, s.session_name, s.date_start)
```

`list()` always returns a Python `list` of model objects. Filters must be passed by name: `f1.drivers.list(session_key=9158)` works, but `f1.drivers.list(9158)` raises an error.

### The `"latest"` keyword

Pass `"latest"` to `session_key` or `meeting_key` to get the current or most recent session or meeting:

```python
with OpenF1Client() as f1:
    latest = f1.sessions.list(session_key="latest")[0]
    print(f"{latest.country_name}: {latest.session_name}")
```

## Examples

### Find a race and its drivers

```python
from openf1py import OpenF1Client

with OpenF1Client() as f1:
    race = f1.sessions.list(year=2024, country_name="Monaco", session_name="Race")[0]

    for d in f1.drivers.list(session_key=race.session_key):
        print(f"#{d.driver_number:<3} {d.full_name:<25} {d.team_name}")
```

### Fastest lap of a driver

```python
with OpenF1Client() as f1:
    laps = f1.laps.list(session_key=9161, driver_number=63)
    timed = [lap for lap in laps if lap.lap_duration is not None]
    fastest = min(timed, key=lambda lap: lap.lap_duration)

    print(f"Lap {fastest.lap_number}: {fastest.lap_duration:.3f}s")
```

### Tyre strategy

```python
with OpenF1Client() as f1:
    for stint in f1.stints.list(session_key=9165, driver_number=1):
        print(f"Stint {stint.stint_number}: {stint.compound} from lap {stint.lap_start} to {stint.lap_end}")
```

### Pit stops

```python
with OpenF1Client() as f1:
    for stop in f1.pit.list(session_key=9877):
        # stop_duration is only recorded from the 2024 US GP onwards; older stops have None
        stationary = f"{stop.stop_duration}s" if stop.stop_duration is not None else "n/a"
        print(f"Car {stop.driver_number}, lap {stop.lap_number}: pit lane {stop.lane_duration}s, stationary {stationary}")
```

### Race control messages

```python
with OpenF1Client() as f1:
    for msg in f1.race_control.list(session_key=9165, category="Flag"):
        print(msg.date, msg.flag, msg.message)
```

### Championship standings after a race

```python
with OpenF1Client() as f1:
    standings = f1.drivers_championship.list(meeting_key=1276)

    for row in sorted(standings, key=lambda r: r.position_current):
        print(f"P{row.position_current}  #{row.driver_number}  {row.points_current} pts")
```

### Load into pandas

The models are dataclasses, so they convert to a DataFrame easily (pandas is not a dependency; install it separately):

```python
from dataclasses import asdict

import pandas as pd
from openf1py import OpenF1Client

with OpenF1Client() as f1:
    car_data = f1.car_data.list(session_key=9159, driver_number=55)

df = pd.DataFrame([asdict(row) for row in car_data])
print(df[["date", "speed", "rpm", "n_gear"]].describe())
```

## Endpoints

| Client attribute | Returns | Filters |
|---|---|---|
| `f1.car_data` | `CarData` | `session_key`, `meeting_key`, `driver_number` |
| `f1.drivers` | `Driver` | `session_key`, `meeting_key`, `driver_number` |
| `f1.drivers_championship` | `ChampionshipDriver` | `meeting_key`, `driver_number` |
| `f1.intervals` | `Interval` | `session_key`, `meeting_key`, `driver_number` |
| `f1.laps` | `Lap` | `session_key`, `meeting_key`, `driver_number`, `lap_number` |
| `f1.location` | `Location` | `session_key`, `meeting_key`, `driver_number` |
| `f1.meetings` | `Meeting` | `meeting_key`, `year`, `country_name` |
| `f1.overtakes` | `Overtake` | `session_key`, `meeting_key`, `overtaking_driver_number`, `overtaken_driver_number` |
| `f1.pit` | `Pit` | `session_key`, `meeting_key`, `driver_number`, `lap_number` |
| `f1.position` | `Position` | `session_key`, `meeting_key`, `driver_number` |
| `f1.race_control` | `RaceControl` | `session_key`, `meeting_key`, `driver_number`, `category`, `flag` |
| `f1.session_result` | `SessionResult` | `session_key`, `meeting_key`, `driver_number` |
| `f1.sessions` | `Sessions` | `session_key`, `meeting_key`, `year`, `country_name`, `session_name` |
| `f1.starting_grid` | `StartingGrid` | `session_key`, `meeting_key`, `driver_number` |
| `f1.stints` | `Stint` | `session_key`, `meeting_key`, `driver_number`, `compound` |
| `f1.team_radio` | `TeamRadio` | `session_key`, `meeting_key`, `driver_number` |
| `f1.teams_championship` | `ChampionshipTeam` | `meeting_key`, `team_name` |
| `f1.weather` | `Weather` | `session_key`, `meeting_key` |

For what each field means, see the [OpenF1 API documentation](https://openf1.org/docs).

### Things to know about the data

- **Fields can be `None`.** If the API sends `null` or leaves a field out, the model's value is `None`. Check for `None` before doing arithmetic on optional values such as `Lap.lap_duration` or `Pit.stop_duration`.
- **Some fields mix types.**
  - `Interval.gap_to_leader` and `Interval.interval` are seconds as a `float`, the string `"+1 LAP"` for a lapped car, or `None` for the leader.
  - In qualifying, `SessionResult.duration` and `SessionResult.gap_to_leader` are lists of three values (Q1, Q2, Q3).
- **Dates are strings** in ISO 8601 format, for example `"2023-09-17T13:31:02.395000+00:00"`. Use `datetime.fromisoformat()` to turn them into `datetime` objects.
- **High-frequency endpoints are large.** `car_data` and `location` record several samples per second, so filter by `session_key` and `driver_number` to keep responses manageable.
- **New API fields are ignored.** If OpenF1 adds a field, your code keeps working; the field just isn't available on the model until the library adds it.
- **No matches means an empty list.** OpenF1 answers a query that matches nothing with a `404 "No results found."`; openf1py turns that into `[]`. OpenF1 doesn't validate filter values either, so a typo such as `country_name="Singpore"` also returns `[]` rather than an error.

## Error handling

Every error raised by openf1py inherits from `OpenF1PyException`. When the API returns an error response, you get an `APIError` with the HTTP status code:

```python
from openf1py import APIError, OpenF1Client

with OpenF1Client() as f1:
    try:
        drivers = f1.drivers.list(session_key=9158)
    except APIError as e:
        print(f"OpenF1 returned {e.status_code}: {e}")
```

Network problems such as no internet connection or a timeout are raised as `httpx` exceptions (for example `httpx.ConnectError`); they aren't wrapped in `OpenF1PyException`.

### Access during live sessions

While an F1 session is live, OpenF1 limits **all** unauthenticated access, including historical data from past seasons, and requests fail with `APIError` status `401`. You can either wait for the session to end, or pass an API key:

```python
import os

with OpenF1Client(token=os.environ["OPENF1_TOKEN"]) as f1:
    ...
```

Read the key from an environment variable rather than writing it in your code.

## Development

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

### Unit tests

```bash
pytest -v
```

The unit tests never call the real API. They use `httpx.MockTransport` with sample responses from the OpenF1 docs, so they run offline in under a second.

### Smoke test against the live API

[examples/smoke_test.py](examples/smoke_test.py) uses the library the way a user would, calling every endpoint on the real API and checking that the results make sense:

```bash
python examples/smoke_test.py
OPENF1_TOKEN=your-key python examples/smoke_test.py   # during a live session
```

It exits with `0` if every check passes, `1` if any check fails, and `2` if the API is restricting access.

### Project layout

```
src/openf1py/
    client.py       OpenF1Client: HTTP connection and endpoint attributes
    resources.py    One resource class per endpoint, each with list() and its filters
    model.py        One dataclass per endpoint, built on the OpenF1Model base class
    exceptions.py   OpenF1PyException and APIError
tests/              One unit test file per endpoint, plus test_model.py
examples/           smoke_test.py
```

### Adding an endpoint

1. Open the endpoint's URL in a browser and copy a real response record.
2. Add a dataclass to `model.py` that inherits from `OpenF1Model`, with field names that match the JSON keys exactly.
3. Add a resource class to `resources.py` with a `list()` method and its filters.
4. Register it in `OpenF1Client.__init__` and export the model from `__init__.py`.
5. Add `tests/test_<endpoint>.py`, using the real record from step 1 as the sample data.

## Acknowledgements

Data is provided by [OpenF1](https://openf1.org). This project is not affiliated with OpenF1, Formula 1, or the FIA.
