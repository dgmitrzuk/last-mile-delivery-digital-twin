import requests


API_URL = "https://parcelshop.dhl.pl/mapa/points"


def is_locker(item: dict) -> bool:
    """
    Sprawdza czy punkt DHL jest automatem.
    """

    point_type = str(
        item.get("P_TYPE")
        or item.get("type")
        or ""
    ).lower()

    return (
        "box" in point_type
        or "locker" in point_type
        or "automat" in point_type
        or point_type == "ecobox"
    )


def normalize_point(item: dict) -> dict:
    """
    Zamienia format DHL na wspólny model punktu.
    """

    locker = is_locker(item)

    return {
        "operator": "DHL",

        "external_id": str(
            item.get("ID")
            or item.get("id")
            or ""
        ),

        "type": (
            "AUTOMAT"
            if locker
            else "PUNKT_STACJONARNY"
        ),

        "name": (
            item.get("NAME")
            or item.get("name")
        ),

        "city": (
            item.get("CITY")
            or item.get("city")
        ),

        "street": (
            item.get("STREET")
            or item.get("street")
        ),

        "postal_code": (
            item.get("POSTCODE")
            or item.get("postcode")
        ),

        "latitude": (
            item.get("SZ_GEOGRAFICZNA")
            or item.get("lat")
        ),

        "longitude": (
            item.get("DL_GEOGRAFICZNA")
            or item.get("lng")
        ),

        "dhl_type": (
            item.get("P_TYPE")
            or item.get("type")
        )
    }


def fetch_points() -> list[dict]:
    """
    Pobiera wszystkie punkty DHL Parcel Polska.
    Zwraca listę punktów gotowych do zapisu w PostGIS.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7)"
        ),
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://parcelshop.dhl.pl/mapa",
    }


    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()


    if isinstance(data, list):
        points = data

    elif isinstance(data, dict):
        points = (
            data.get("response")
            or data.get("points")
            or data.get("data")
            or []
        )

    else:
        points = []


    return [
        normalize_point(point)
        for point in points
        if isinstance(point, dict)
    ]