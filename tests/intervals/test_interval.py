from shapely.geometry import Point
from registered.intervals.interval import Stop, Interval, IntervalType


class TestStop:
    def test_from_tuple(self):
        actual = Stop(("-1", "-2"), id="123", description="hi")
        assert actual.id == "123"
        assert actual.description == "hi"
        assert actual.wkt == "POINT (-1 -2)"
        assert actual.x == -1
        assert actual.y == -2
        assert repr(actual) == "Stop(Point(-1.0, -2.0), id='123', description='hi')"

    def test_from_point(self):
        actual = Stop(Point((2, 3)), id="456")
        assert actual.id == "456"
        assert actual.description is None
        assert actual.wkt == "POINT (2 3)"
        assert actual.x == 2
        assert actual.y == 3


class TestInterval:
    def test_from_row(self):
        row = {
            "issueid": "1",
            "routeversionid": "138.2",
            "IntervalId": "1234",
            "IntervalType": "0",
            "FromStopNumber": "5774",
            "FromStopDescription": "Revere St @ Sagamore St",
            "FromStopLatitude": "42.418574",
            "FromStopLongitude": "-70.99272",
            "ToStopNumber": "15795",
            "ToStopDescription": "Wonderland Busway",
            "ToStopLatitude": "42.413385",
            "ToStopLongitude": "-70.99205",
            "IntervalDescription": "116-Outbound-116-4",
        }
        expected = Interval(
            id=1234,
            type=IntervalType.REVENUE,
            from_stop=Stop(
                (-70.992792, 42.418574),
                id="5774",
                description="Revere St @ Sagamore St",
            ),
            to_stop=Stop(
                (-70.99205, 42.413385), id="15795", description="Wonderland Busway"
            ),
            description="116-Outbound-116-4",
        )
        actual = Interval.from_row(row)
        assert expected == actual
