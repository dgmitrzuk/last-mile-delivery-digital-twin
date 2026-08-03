from src.ingestion.load_to_postgis import load_points


points = [
    {
        "operator": "TEST",
        "external_id": "123",
        "type": "AUTOMAT",
        "name": "Test Locker",
        "city": "Warszawa",
        "postal_code": "00-001",
        "street": "Marszałkowska",
        "opening_hours": None,
        "cash_on_delivery": False,
        "latitude": 52.2297,
        "longitude": 21.0122
    }
]


load_points(points)