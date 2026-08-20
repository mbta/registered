import pytest
from pathlib import Path
from registered.intervals import interval_changes
from registered.rating import Rating
import argparse

RATING_PATH = Path(__file__).parent / "support" / "rating" / "Combine"

next_rating = Rating(RATING_PATH)

def test_one_stop_multiple_routes():
    different_stop_locations = {'522'}
    expected_intervals = set([('520', '522'),
                              ('522', '10522')]) 

    by_route = interval_changes.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()
    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 2
    assert intervals == expected_intervals

def test_multiple_stops_one_route():
    different_stop_locations = {'5642', '5640'}
    expected_intervals = set([('5640', '5642'),
                              ('5638', '5640'),
                              ('5642', '5643'),
                              ('5640', '5566')])
    
    by_route = interval_changes.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()

    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 4
    assert intervals == expected_intervals

def test_stop_intervals():
    different_stop_locations = {'522', '5642', '5640', '5887', '1049'}
    expected_intervals = set([('5640', '5642'),
                              ('5638', '5640'),
                              ('5642', '5643'),
                              ('5640', '5566'),
                              ('520', '522'),
                              ('522', '10522'),
                              ('5886', '5887'),
                              ('5887', '5888'),
                              ('1046', '1049'),
                              ('1049', '1589')])
    
    by_route = interval_changes.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()

    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 10
    assert intervals == expected_intervals

def test_multiple_stops_multiple_routes():
    different_stop_locations = {'3627', '3629', '3633', '3635'}
    expected_intervals = set([('3626','3627'),
                              ('3627','3629'),
                              ('3629','3630'),
                              ('3632','3633'),
                              ('3633','3634'), 
                              ('3634','3635'),
                              ('3635','3638'),]) 

    by_route = interval_changes.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()
    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 7
    assert intervals == expected_intervals

def test_read_excel_valid():
    excel = Path(__file__).parent / "support" / "interval_change" / "valid" / "valid_stop_comparison.xlsx"
    excel_df = interval_changes.process_stop_changes_excel(excel, 'Sheet1')

    assert "Needs interval change? " in excel_df.columns
    assert "stopID" in excel_df.columns

def test_read_excel_missing_columns():
    excel_1 = Path(__file__).parent / "support" / "interval_change" / "invalid" / "missing_needs_interval.xlsx"
    excel_2 = Path(__file__).parent / "support" / "interval_change" / "invalid" / "missing_stop_id.xlsx"
    with pytest.raises(RuntimeError):
        excel_1_df = interval_changes.process_stop_changes_excel(excel_1, 'Sheet1')
    with pytest.raises(RuntimeError):
        excel_2_df = interval_changes.process_stop_changes_excel(excel_2, 'Sheet1')


