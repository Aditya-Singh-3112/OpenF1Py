from dataclasses import fields

import pytest

import openf1py
from openf1py import Pit
from openf1py.model import OpenF1Model

ALL_MODELS = [
    obj for obj in vars(openf1py).values()
    if isinstance(obj, type) and issubclass(obj, OpenF1Model)
]

def test_missing_fields_become_none():
    # Pit stops before the 2024 US GP have no stop_duration
    pit = Pit.from_dict({
        "date": "2023-09-17T12:52:17.818000+00:00",
        "driver_number": 1,
        "lane_duration": 21.871,
        "lap_number": 20,
        "meeting_key": 1219,
        "session_key": 9165,
    })

    assert pit.stop_duration is None
    assert pit.lane_duration == 21.871

def test_unknown_fields_are_ignored():
    pit = Pit.from_dict({"driver_number": 1, "brand_new_field": "x"})

    assert pit.driver_number == 1
    assert not hasattr(pit, "brand_new_field")

def test_all_models_are_exported():
    assert len(ALL_MODELS) == 18

@pytest.mark.parametrize("model", ALL_MODELS, ids=lambda m: m.__name__)
def test_every_model_handles_an_empty_dict(model):
    obj = model.from_dict({})

    assert all(getattr(obj, f.name) is None for f in fields(obj))
