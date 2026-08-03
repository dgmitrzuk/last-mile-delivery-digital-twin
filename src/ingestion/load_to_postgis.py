from sqlalchemy import text

from src.database.connection import engine


INSERT_QUERY = """

INSERT INTO operations.delivery_points
(
    operator,
    external_id,
    type,
    name,
    city,
    postal_code,
    street,
    opening_hours,
    cash_on_delivery,
    latitude,
    longitude,
    geometry
)

VALUES
(
    :operator,
    :external_id,
    :type,
    :name,
    :city,
    :postal_code,
    :street,
    :opening_hours,
    :cash_on_delivery,
    :latitude,
    :longitude,

    ST_SetSRID(
        ST_Point(
            :longitude,
            :latitude
        ),
        4326
    )
)

"""


def prepare_point(point: dict) -> dict:
    return {
        "operator": point.get("operator"),
        "external_id": point.get("external_id"),
        "type": point.get("type"),

        "name": point.get("name"),
        "city": point.get("city"),
        "postal_code": point.get("postal_code"),
        "street": point.get("street"),

        "opening_hours": point.get("opening_hours"),

        "cash_on_delivery": point.get(
            "cash_on_delivery",
            False
        ),

        "latitude": point.get("latitude"),
        "longitude": point.get("longitude"),
    }


def load_points(points: list[dict]):

    if not points:
        print("Brak danych do załadowania.")
        return


    points = [
        prepare_point(point)
        for point in points
    ]


    with engine.begin() as connection:

        connection.execute(
            text(INSERT_QUERY),
            points
        )


    print(
        f"Załadowano {len(points)} punktów do PostGIS"
    )