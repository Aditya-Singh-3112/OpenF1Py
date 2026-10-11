"""
End-to-end check of openf1py against the real OpenF1 API, written the way a user would use it.

Run:
    python examples/smoke_test.py

During a live F1 session OpenF1 restricts access to authenticated users. If you have an API key:
    OPENF1_TOKEN=your-key python examples/smoke_test.py
"""
import os
import sys
import time

from openf1py import (
    APIError, OpenF1Client, OpenF1PyException,
    CarData, ChampionshipDriver, ChampionshipTeam, Driver, Interval, Lap, Location, Meeting,
    Overtake, Pit, Position, RaceControl, SessionResult, Sessions, StartingGrid, Stint, TeamRadio, Weather,
)

# The free API allows a few requests per second, so pause between calls
DELAY_SECONDS = 0.5

results: list[tuple[str, bool, str]] = []


def check(name, call, expected_type, *conditions):
    """Run one API call, then check the result is a non-empty list of the right type and passes every condition."""
    time.sleep(DELAY_SECONDS)
    try:
        data = call()
    except OpenF1PyException as e:
        results.append((name, False, str(e)[:100]))
        return None

    if not data:
        results.append((name, False, "returned no rows"))
        return None
    if not all(isinstance(row, expected_type) for row in data):
        results.append((name, False, f"expected {expected_type.__name__} objects"))
        return None
    for description, condition in conditions:
        try:
            ok = condition(data)
        except Exception as e:
            ok, description = False, f"{description} ({type(e).__name__}: {e})"
        if not ok:
            results.append((name, False, f"failed: {description}"))
            return None

    results.append((name, True, f"{len(data)} rows, first: {str(data[0])[:70]}..."))
    return data


def main() -> int:
    token = os.environ.get("OPENF1_TOKEN")

    with OpenF1Client(token=token) as f1:

        # Can we reach the API at all? Stop early with a clear message if not
        try:
            f1.meetings.list(year=2023, country_name="Singapore")
        except APIError as e:
            if e.status_code == 401:
                print("OpenF1 is restricting access (a live F1 session is probably running).")
                print("Try again after the session, or set OPENF1_TOKEN to your API key.")
                return 2
            raise

        # --- Calendar: meetings and sessions ---
        check("meetings", lambda: f1.meetings.list(year=2023, country_name="Singapore"), Meeting,
              ("is the 2023 Singapore GP", lambda d: d[0].meeting_key == 1219 and "Singapore" in d[0].meeting_name))

        check("sessions", lambda: f1.sessions.list(meeting_key=1219), Sessions,
              ("includes the race", lambda d: any(s.session_name == "Race" and s.session_key == 9165 for s in d)))

        check("sessions: 'latest' keyword", lambda: f1.sessions.list(session_key="latest"), Sessions,
              ("returns exactly one session", lambda d: len(d) == 1))

        # --- People ---
        check("drivers", lambda: f1.drivers.list(session_key=9158, driver_number=1), Driver,
              ("is Verstappen", lambda d: d[0].name_acronym == "VER"))

        # --- Telemetry ---
        check("car_data", lambda: f1.car_data.list(session_key=9159, driver_number=55), CarData,
              ("speeds are realistic (0-400 km/h)", lambda d: all(0 <= r.speed <= 400 for r in d)),
              ("only driver 55", lambda d: all(r.driver_number == 55 for r in d)))

        check("location", lambda: f1.location.list(session_key=9161, driver_number=81), Location,
              ("has x/y/z coordinates", lambda d: all(isinstance(r.x, int) for r in d)))

        # --- Timing ---
        check("laps", lambda: f1.laps.list(session_key=9161, driver_number=63, lap_number=8), Lap,
              ("lap time matches the docs (91.743s)", lambda d: d[0].lap_duration == 91.743),
              ("mini-sectors are lists", lambda d: isinstance(d[0].segments_sector_1, list)))

        check("intervals", lambda: f1.intervals.list(session_key=9165, driver_number=1), Interval,
              ("gaps are numbers, '+N LAP' strings, or None",
               lambda d: all(isinstance(r.gap_to_leader, (int, float, str, type(None))) for r in d)))

        check("position", lambda: f1.position.list(meeting_key=1217, driver_number=40), Position,
              ("positions are 1-20", lambda d: all(1 <= r.position <= 20 for r in d)))

        check("overtakes", lambda: f1.overtakes.list(session_key=9636, overtaking_driver_number=63, overtaken_driver_number=4), Overtake,
              ("correct drivers", lambda d: all(r.overtaking_driver_number == 63 and r.overtaken_driver_number == 4 for r in d)))

        # --- Strategy ---
        check("pit (2025: has stop_duration)", lambda: f1.pit.list(session_key=9877), Pit,
              ("some stops have stop_duration", lambda d: any(r.stop_duration is not None for r in d)))

        check("pit (2023: no stop_duration yet)", lambda: f1.pit.list(session_key=9165), Pit,
              ("missing field becomes None", lambda d: all(r.stop_duration is None for r in d)))

        check("stints", lambda: f1.stints.list(session_key=9165, compound="SOFT"), Stint,
              ("all SOFT tyres", lambda d: all(r.compound == "SOFT" for r in d)))

        # --- Race control, radio, weather ---
        check("race_control", lambda: f1.race_control.list(session_key=9102, driver_number=1, flag="BLACK AND WHITE"), RaceControl,
              ("is a black and white flag", lambda d: all(r.flag == "BLACK AND WHITE" for r in d)))

        check("team_radio", lambda: f1.team_radio.list(session_key=9158, driver_number=11), TeamRadio,
              ("has mp3 recording URLs", lambda d: all(r.recording_url.endswith(".mp3") for r in d)))

        check("weather", lambda: f1.weather.list(meeting_key=1208), Weather,
              ("temperatures are realistic", lambda d: all(-10 < r.air_temperature < 60 for r in d)))

        # --- Results ---
        check("session_result", lambda: f1.session_result.list(session_key=7782), SessionResult,
              ("has a winner", lambda d: any(r.position == 1 for r in d)))

        check("starting_grid", lambda: f1.starting_grid.list(session_key=7783), StartingGrid,
              ("has pole position", lambda d: any(r.position == 1 for r in d)))

        # --- Championships ---
        check("championship drivers", lambda: f1.drivers_championship.list(meeting_key=1276, driver_number=4), ChampionshipDriver,
              ("points are numbers", lambda d: isinstance(d[0].points_current, (int, float))))

        check("championship teams", lambda: f1.teams_championship.list(meeting_key=1276, team_name="McLaren"), ChampionshipTeam,
              ("is McLaren", lambda d: d[0].team_name == "McLaren"))

        # --- Edge cases a user will hit ---
        time.sleep(DELAY_SECONDS)
        try:
            rows = f1.drivers.list(session_key=9158, driver_number=999)
            results.append(("filter that matches nothing", rows == [], f"returned {rows!r}"))
        except APIError as e:
            results.append(("filter that matches nothing", False, f"raised APIError {e.status_code} instead of returning []"))

        # OpenF1 doesn't validate filter values, so a bad one just matches nothing
        time.sleep(DELAY_SECONDS)
        try:
            rows = f1.drivers.list(session_key="not-a-number")
            results.append(("invalid filter value", rows == [], f"returned {rows!r}"))
        except APIError as e:
            results.append(("invalid filter value", False, f"raised APIError {e.status_code} instead of returning []"))

    # --- Report ---
    width = max(len(name) for name, _, _ in results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<{width}}  {detail}")

    failed = sum(not ok for _, ok, _ in results)
    print(f"\n{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
