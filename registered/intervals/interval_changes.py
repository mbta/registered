"""
CLI tool to identify unique intervals from stops. Takes stop_comparison output as input.
"""

from collections import defaultdict
import argparse
import pandas as pd
from pyproj import Geod
from registered.parser import Pattern, PatternStop, PatternRevenueType
from registered.rating import Rating

GEOD = Geod(ellps="WGS84")

def get_intervals_from_stops(rating, stops):
    """
    Given a Rating and a list of stops, return a list of unique intervals 
    with an associated revenue route variant. 
    """
    this_route = None
    from_stop = None
    from_stop_name = None
    interval_pairs = defaultdict(set)
    intervals = set()
    all_stops = {stop.stop_id: stop for stop in rating["nde"]}
    for record in rating["pat"]:
        if isinstance(record, Pattern):
            if record.revenue_type == PatternRevenueType.REVENUE:
                this_route = record.route_id + " " +record.direction_name + " " + record.pattern_id
            else: this_route = None
            from_stop = None
            from_stop_name = None
            continue
        if isinstance(record, PatternStop):
            to_stop = record.stop_id
            to_stop_name = all_stops[to_stop].name
            if all([this_route, from_stop]) and (to_stop in stops or from_stop in stops):
                this_interval = (from_stop, to_stop)
                if this_interval not in intervals:
                    interval_pairs[(from_stop, to_stop, from_stop_name, to_stop_name)] = this_route
                    intervals.add(this_interval)
            from_stop = to_stop
            from_stop_name = to_stop_name
    by_route = sorted(interval_pairs.items(), key=lambda x: x[1])
    return by_route

def print_by_route(by_route):
    """
    Print interval information in a csv format. 
    """
    print("route_variant,from_stop,from_stop_name,to_stop,to_stop_name")
    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        print(
            f"{route_direction},{from_stop},{from_stop_name},{to_stop},{to_stop_name}"
        )

def process_stop_changes_excel(file_path, sheet_name):
    """
    Read StopChanges excel into dataframe and check 
    columns "Needs interval change? " and "stopID" exists 
    """
    excel = pd.read_excel(file_path, sheet_name = sheet_name)
    if "Needs interval change? " not in excel.columns or "stopID" not in excel.columns:
        raise RuntimeError('Excel needs columns "Needs interval change? " and "stopID"')
    return excel

def main(args):
    """
    Entrypoint for the CLI tool.
    """
    excel = process_stop_changes_excel(args.STOP_CHANGES, sheet_name = args.SHEET_NAME)
    next_rating = Rating(args.NEXT)
    stops = excel.loc[excel["Needs interval change? "] != ""]["stopID"].astype(str).unique()
    by_route = get_intervals_from_stops(next_rating, stops)
    print_by_route(by_route)



parser = argparse.ArgumentParser(
    description="Use stopChanges.xlsx and the next rating to get a list of interval changes."
)
parser.add_argument(
    "STOP_CHANGES", help="The path to the stopChanges excel for the rating."
)
parser.add_argument(
    "SHEET_NAME", help="The sheet name of the stopChanges sheet."
)
parser.add_argument(
    "NEXT", help="The Combine directory where the next rating files live"
)

if __name__ == "__main__":
    import sys

    sys.exit(main(parser.parse_args()))
