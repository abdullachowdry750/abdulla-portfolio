import pandas as pd
import pytest

from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import URL

import src.storage.postgres as postgres
from src.config import settings


@pytest.fixture
def test_db(monkeypatch):
    """Use an isolated PostgreSQL test database."""

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database="enterprise_data_test",
    )

    test_engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    # Route storage operations to the test database.
    monkeypatch.setattr(postgres, "engine", test_engine)

    # Reset only tables in the dedicated test database.
    postgres.Base.metadata.drop_all(test_engine)
    postgres.create_tables()

    yield test_engine

    postgres.Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture
def customers():
    return pd.DataFrame({
        "customer_id": [101, 102, 103],
        "customer_name": [
            "Aarav Sharma",
            "Sara Khan",
            "Rahul Verma",
        ],
        "email": [
            "aarav.test@example.com",
            "sara.test@example.com",
            "rahul.test@example.com",
        ],
        "city": [
            "Bengaluru",
            "Mumbai",
            "Delhi",
        ],
        "signup_date": [
            "2026-01-10",
            "2026-01-12",
            "2026-01-15",
        ],
    })


def test_insert_new_customers(test_db, customers):
    result = postgres.sync_customers(customers)

    assert result == {
        "inserted": 3,
        "updated": 0,
        "unchanged": 0,
    }

    with test_db.connect() as connection:
        count = connection.execute(
            select(func.count()).select_from(postgres.Customer)
        ).scalar_one()

    assert count == 3


def test_unchanged_customers_are_skipped(test_db, customers):
    postgres.sync_customers(customers)

    result = postgres.sync_customers(customers)

    assert result == {
        "inserted": 0,
        "updated": 0,
        "unchanged": 3,
    }


def test_modified_customer_is_updated(test_db, customers):
    postgres.sync_customers(customers)

    modified = customers.copy()
    modified.loc[0, "city"] = "Hyderabad"

    result = postgres.sync_customers(modified)

    assert result == {
        "inserted": 0,
        "updated": 1,
        "unchanged": 2,
    }

    with test_db.connect() as connection:
        city = connection.execute(
            select(postgres.Customer.city).where(
                postgres.Customer.customer_id == 101
            )
        ).scalar_one()

    assert city == "Hyderabad"


def test_partial_batch_verification(test_db, customers):
    postgres.sync_customers(customers)

    subset = customers.head(2)

    result = postgres.verify_customer_records(subset)

    assert result == {
        "verified": 2,
        "missing": 0,
        "mismatched": 0,
    }


def test_missing_customer_fails_verification(test_db, customers):
    postgres.sync_customers(customers)

    missing_customer = pd.DataFrame([{
        "customer_id": 999,
        "customer_name": "Missing Customer",
        "email": "missing.test@example.com",
        "city": "Bengaluru",
        "signup_date": "2026-02-01",
    }])

    with pytest.raises(
        ValueError,
        match="Customer verification failed",
    ):
        postgres.verify_customer_records(missing_customer)


def test_successful_ingestion_audit(test_db):
    run_id = "integration-test-success"

    postgres.start_ingestion_audit(
        run_id=run_id,
        source_file="customers_test.csv",
    )

    postgres.complete_ingestion_audit(
        run_id=run_id,
        records_read=3,
        sync_result={
            "inserted": 2,
            "updated": 1,
            "unchanged": 0,
        },
    )

    with test_db.connect() as connection:
        audit = connection.execute(
            select(
                postgres.IngestionAudit.status,
                postgres.IngestionAudit.records_read,
                postgres.IngestionAudit.inserted,
                postgres.IngestionAudit.updated,
                postgres.IngestionAudit.unchanged,
            ).where(
                postgres.IngestionAudit.dag_run_id == run_id
            )
        ).mappings().one()

    assert audit["status"] == "SUCCESS"
    assert audit["records_read"] == 3
    assert audit["inserted"] == 2
    assert audit["updated"] == 1
    assert audit["unchanged"] == 0

def test_failed_ingestion_audit(test_db):
    run_id = "integration-test-failure"

    postgres.start_ingestion_audit(
        run_id=run_id,
        source_file="invalid_customers.csv",
    )

    postgres.fail_ingestion_audit(
        run_id=run_id,
        error_message="Simulated ingestion failure",
    )

    with test_db.connect() as connection:
        audit = connection.execute(
            select(
                postgres.IngestionAudit.status,
                postgres.IngestionAudit.error_message,
                postgres.IngestionAudit.completed_at,
            ).where(
                postgres.IngestionAudit.dag_run_id == run_id
            )
        ).mappings().one()

    assert audit["status"] == "FAILED"
    assert audit["error_message"] == "Simulated ingestion failure"
    assert audit["completed_at"] is not None
