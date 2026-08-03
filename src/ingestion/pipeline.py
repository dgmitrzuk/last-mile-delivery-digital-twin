from src.ingestion.couriers.inpost import fetch_points
from src.ingestion.load_to_postgis import load_points


def run():

    print("Pobieranie InPost...")

    points = fetch_points()

    print(
        f"Pobrano {len(points)} punktów"
    )

    load_points(points)


if __name__ == "__main__":
    run()