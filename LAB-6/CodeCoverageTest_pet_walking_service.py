import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars


def test_single_standard_30_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [
                {
                    "num_pets": 1,
                    "aggression_alert": False,
                    "needs_meds": False
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"


def test_standard_60_walk():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [
                {
                    "num_pets": 2,
                    "aggression_alert": False,
                    "needs_meds": False
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 45.0
    assert result["status"] == "COMPLETED"


def test_express_15_with_medication_and_weekend():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "express_15",
            "is_weekend": True,
            "walks": [
                {
                    "num_pets": 1,
                    "aggression_alert": False,
                    "needs_meds": True
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 30.0
    assert result["status"] == "COMPLETED"


def test_more_than_three_pets():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [
                {
                    "num_pets": 4,
                    "aggression_alert": False,
                    "needs_meds": False
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 48.6
    assert result["status"] == "COMPLETED"


def test_aggression_standard_60():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_60",
            "is_weekend": False,
            "walks": [
                {
                    "num_pets": 1,
                    "aggression_alert": True,
                    "needs_meds": False
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_invalid_session_type():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "invalid_session",
            "is_weekend": False,
            "walks": []
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_invalid_number_of_pets():
    routes = [
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "is_weekend": False,
            "walks": [
                {
                    "num_pets": 0,
                    "aggression_alert": False,
                    "needs_meds": False
                }
            ]
        }
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_invalid_input():
    with pytest.raises(ValueError):
        process_walking_routes("not a list", 5.0)


def test_incident_audit():
    routes = [
        {"route_confirmed": True, "session_type": "invalid_session", "walks": []},
        {"route_confirmed": True, "session_type": "invalid_session", "walks": []},
        {"route_confirmed": True, "session_type": "invalid_session", "walks": []},
        {"route_confirmed": True, "session_type": "invalid_session", "walks": []},
        {"route_confirmed": True, "session_type": "invalid_session", "walks": []}
    ]

    result = process_walking_routes(routes, 5.0)
    assert result["status"] == "INCIDENT_AUDIT"


def test_gps_no_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_online():
    collar_matrix = [
        [50, 45, 60],
        [30, 35, 40]
    ]

    assert inspect_gps_collars(collar_matrix) == "ONLINE"


def test_gps_lost_signal():
    collar_matrix = [
        [50, 10, 15]
    ]

    assert inspect_gps_collars(collar_matrix) == "LOST_SIGNAL_ALERT"