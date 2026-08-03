import time
import requests


API_URL = "https://api-pl-points.easypack24.net/v1/points"


def normalize_point(item: dict) -> dict:
    """
    Zamienia format API InPost na wspólny model punktu.
    """

    loc = item.get("location") or {}
    addr = item.get("address") or {}
    det = item.get("address_details") or {}

    return {
        "operator": "InPost",
        "external_id": item.get("name"),

        "name": item.get("display_name"),
        "type": ", ".join(item.get("type") or []),

        "latitude": loc.get("latitude"),
        "longitude": loc.get("longitude"),

        "city": det.get("city"),
        "province": det.get("province"),
        "postal_code": det.get("post_code"),

        "street": det.get("street"),
        "building_number": det.get("building_number"),

        "status": item.get("status"),

        "opening_hours": item.get("opening_hours"),
    }


def fetch_points(
    status="Operating",
    delay=0.25
):
    """
    Pobiera wszystkie punkty InPost.
    Zwraca listę słowników gotowych do zapisu w bazie.
    """

    session = requests.Session()
    session.headers["Accept"] = "application/json"

    params = {
        "per_page": 500,
        "page": 1,
        "status": status
    }

    points = []

    response = session.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    pages = data.get("total_pages", 1)

    points.extend(
        normalize_point(p)
        for p in data.get("items", [])
    )


    for page in range(2, pages + 1):

        time.sleep(delay)

        params["page"] = page

        response = session.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        items = response.json().get("items", [])

        points.extend(
            normalize_point(p)
            for p in items
        )


    return points