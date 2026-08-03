from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql://admin:admin@localhost:5432/postgis_master_thesis"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)