import pytest
from pathlib import Path
from registered.stop_comparison import *

RATING_PATH = Path(__file__).parent / "support" / "stop_comparison"

def test_by_stop():

    keys = ['64','1','2','6','110']
    values = [{('01', 'Outbound')},
              {('01', 'Outbound')},
              {('01', 'Outbound')},
              {('01', 'Outbound')},
              {('01', 'Outbound')}]
    expected = dict(zip(keys, values)).items()
    rating = Rating(RATING_PATH)
    output = route_direction_by_stops(rating).items()
    assert output == expected
