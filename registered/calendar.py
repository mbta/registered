"""
CLI tool to output the calendar for each garage
"""

import sys
import argparse
from registered.rating import Rating
from registered.parser import CalendarDate


def calculate_garage_bases(garages, services, day_types, day_type):
    """
    Find the most commonly used service for all garages for a given day type: 
    (Weekday, Saturday, Sunday).
    """
    dates = {date for date in day_types if day_types[date] == day_type}
    garage_bases = {}

    for garage in garages:
        base = max(
            services.values(),
            key=lambda schedule, g=garage: sum(
                1
                for date in dates
                if services[(date, g)] == schedule
            ),
        )
        garage_bases[garage] = base
    return garage_bases

def calendar(rating):
    """
    Generate the calendar for a given rating.
    """
    cal = rating["cal"]
    garages = set()
    dates = set()
    services = {}
    day_types = {}
    for record in cal:
        if not isinstance(record, CalendarDate):
            continue
        garages.add(record.garage)
        dates.add(record.date)
        key = (record.date, record.garage)
        services[key] = record.service_key
        day_types[record.date] = record.day_type

    garages = sorted(garages)
    weekday_bases = calculate_garage_bases(garages, services, day_types, "Weekday")
    yield ["date", *garages]

    for date in sorted(dates):
        date_str = date.strftime("%Y-%m-%d")
        garage_values = (
            weekday_bases.get(garage, "")
            if services.get((date, garage), "") == "l31"
            else services.get((date, garage), "")
            for garage in garages
        )
        yield [date_str, *garage_values]

def main_combine(path, file=sys.stdout):
    """
    Print the output from the calendar function.

    Optionally takes a file to write to (default: stdout)
    """
    for row in calendar(Rating(path)):
        print(",".join(row), file=file)


def main(args):
    """
    Entrypoint for the CLI tool.
    """
    path = args.DIR
    main_combine(path)


parser = argparse.ArgumentParser(
    description="Print the calendar from the HASTUS export files (post-merge)"
)
parser.add_argument("DIR", help="The Combine directory where all the files live")

if __name__ == "__main__":
    main(parser.parse_args())
