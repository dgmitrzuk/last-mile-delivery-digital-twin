import requests


API_URL = (
    "https://pudofinder.dpd.com.pl/ajax/search/"
    "ab2379af98b02ed96c53cdd80a90814b"
    "?lang=pl&country=PL"
)


def is_locker(item: dict) -> bool:
    """
    Sprawdza czy punkt jest automatem paczkowym.
    """

    p_type = str(item.get("type", "")).upper()
    p_subtype = str(
        item.get("subType") or item.get("subtype") or ""
    ).upper()
    p_kind = str(item.get("kind", "")).upper()

    return (
        item.get("isLocker") is True
        or item.get("is_locker") is True
        or "LOCKER" in p_type
        or "LOCKER" in p_subtype
        or "LOCKER" in p_kind
        or "AUTOMAT" in p_type
        or "AUTOMAT" in p_subtype
    )


def normalize_point(item: dict) -> dict:
    """
    Zamienia format DPD na wspólny model punktu.
    """

    address = (
        item.get("address")
        if isinstance(item.get("address"), dict)
        else {}
    )

    locker = is_locker(item)

    return {
        "operator": "DPD",

        "external_id": (
            item.get("pudoId")
            or item.get("id")
            or item.get("code")
        ),

        "type": (
            "AUTOMAT"
            if locker
            else "PUNKT_STACJONARNY"
        ),

        "name": (
            item.get("name")
            or item.get("title")
        ),

        "city": (
            address.get("city")
            or item.get("city")
            or item.get("town")
        ),

        "postal_code": (
            address.get("postcode")
            or address.get("postCode")
            or item.get("postcode")
            or item.get("zip")
        ),

        "street": (
            address.get("street")
            or item.get("street")
            or item.get("address")
        ),

        "latitude": (
            item.get("latitude")
            or item.get("lat")
        ),

        "longitude": (
            item.get("longitude")
            or item.get("lng")
            or item.get("lon")
        ),
    }


def fetch_points() -> list[dict]:
    """
    Pobiera wszystkie punkty DPD Pickup.
    Zwraca listę punktów gotowych do zapisu w PostGIS.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7)"
        ),
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://pudofinder.dpd.com.pl/",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        points = (
            data.get("points")
            or data.get("pudo")
            or data.get("data")
            or data.get("results")
            or []
        )

    elif isinstance(data, list):
        points = data

    else:
        points = []


    return [
        normalize_point(point)
        for point in points
    ]