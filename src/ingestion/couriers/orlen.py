import requests


API_URL = (
    "https://api.globkurier.pl/v1/points"
    "?carrierName=Orlen%20Paczka"
    )


def is_locker(item: dict) -> bool:
    """
    Sprawdza czy punkt Orlen jest automatem paczkowym.
    """

    point_type = str(
        item.get("type", "")
    ).upper()

    name = str(
        item.get("name", "")
    ).upper()

    return (
        point_type in [
            "APM",
            "LOCKER",
            "AUTOMAT",
            "PARCEL_LOCKER"
        ]
        or "APM" in name
        or "AUTOMAT" in name
        or "LOCKER" in name
    )


def normalize_point(item: dict) -> dict:
    """
    Zamienia format Orlen na wspólny model punktu.
    """

    locker = is_locker(item)

    return {
        "operator": "Orlen Paczka",

        "external_id": item.get("id"),

        "type": (
            "AUTOMAT"
            if locker
            else "PUNKT_STACJONARNY"
        ),

        "name": item.get("name"),

        "city": item.get("city"),

        "postal_code": item.get("postCode"),

        "street": item.get("address"),

        "opening_hours": item.get("openingHours"),

        "cash_on_delivery": (
            item.get(
                "cashOnDeliveryAvailable",
                False
            )
        ),

        "latitude": item.get("latitude"),

        "longitude": item.get("longitude"),

        "orlen_type": item.get("type"),
    }


def fetch_points() -> list[dict]:
    """
    Pobiera wszystkie punkty Orlen Paczka.
    Zwraca listę punktów gotowych do zapisu w PostGIS.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7)"
        ),
        "Accept": "application/json",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return []


    return [
        normalize_point(point)
        for point in data
        if isinstance(point, dict)
    ]