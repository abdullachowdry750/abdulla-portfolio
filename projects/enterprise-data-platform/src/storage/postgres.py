import pandas as pd

from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

from src.config import settings


# Database connection
database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


# SQLAlchemy ORM foundation
Base = declarative_base()


# Customer table
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
    )

    customer_name = Column(
        String(150),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    city = Column(
        String(100),
        nullable=False,
    )

    signup_date = Column(
        Date,
        nullable=False,
    )


def create_tables():
    Base.metadata.create_all(engine)


def upsert_customers(dataframe: pd.DataFrame) -> int:
    """
    Insert new customers or update existing customers
    using customer_id as the conflict key.
    """
    records = dataframe.to_dict(orient="records")

    if not records:
        return 0

    statement = insert(Customer.__table__).values(records)

    statement = statement.on_conflict_do_update(
        index_elements=["customer_id"],
        set_={
            "customer_name": statement.excluded.customer_name,
            "email": statement.excluded.email,
            "city": statement.excluded.city,
            "signup_date": statement.excluded.signup_date,
        },
    )

    with engine.begin() as connection:
        connection.execute(statement)

    return len(records)