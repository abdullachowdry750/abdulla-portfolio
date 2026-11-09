import hashlib
import json

import pandas as pd

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    select,
    text,
    update,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

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

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    signup_date = Column(Date, nullable=False)
    record_hash = Column(String(64), nullable=True)


def create_tables():
    Base.metadata.create_all(engine)

    # Add the hash column to existing tables without losing data.
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE customers "
                "ADD COLUMN IF NOT EXISTS record_hash VARCHAR(64)"
            )
        )
        connection.execute(
            text("""
                ALTER TABLE ingestion_audit
                ADD COLUMN IF NOT EXISTS
                clickhouse_inserted INTEGER NOT NULL DEFAULT 0
            """)
        )

        connection.execute(
            text("""
                ALTER TABLE ingestion_audit
                ADD COLUMN IF NOT EXISTS
                clickhouse_updated INTEGER NOT NULL DEFAULT 0
            """)
        )

        connection.execute(
            text("""
                ALTER TABLE ingestion_audit
                ADD COLUMN IF NOT EXISTS
                clickhouse_unchanged INTEGER NOT NULL DEFAULT 0
            """)
        )


def _customer_hash(record: dict) -> str:
    """Generate a deterministic SHA-256 hash for customer data."""

    hash_payload = {
        "customer_id": int(record["customer_id"]),
        "customer_name": str(record["customer_name"]),
        "email": str(record["email"]),
        "city": str(record["city"]),
        "signup_date": pd.to_datetime(
            record["signup_date"]
        ).date().isoformat(),
    }

    serialized = json.dumps(
        hash_payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def _prepare_records(dataframe: pd.DataFrame) -> list[dict]:
    """Normalize customer records and calculate their hashes."""

    records = dataframe.to_dict(orient="records")

    for record in records:
        record["customer_id"] = int(record["customer_id"])
        record["signup_date"] = pd.to_datetime(
            record["signup_date"]
        ).date()

        record["record_hash"] = _customer_hash(record)

    return records


def upsert_customers(dataframe: pd.DataFrame) -> int:
    """
    Insert new customers or update existing customers
    using customer_id as the conflict key.
    """

    records = _prepare_records(dataframe)

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
            "record_hash": statement.excluded.record_hash,
        },
    )

    with engine.begin() as connection:
        connection.execute(statement)

    return len(records)


def sync_customers(dataframe: pd.DataFrame) -> dict:
    """
    Incrementally synchronize customers.

    New records are inserted.
    Changed records are updated.
    Unchanged records are skipped.
    """

    create_tables()

    records = _prepare_records(dataframe)

    if not records:
        return {
            "inserted": 0,
            "updated": 0,
            "unchanged": 0,
        }

    inserted = []
    updated = []
    unchanged = 0

    with engine.begin() as connection:

        # Read existing customer records.
        query = select(
            Customer.customer_id,
            Customer.customer_name,
            Customer.email,
            Customer.city,
            Customer.signup_date,
            Customer.record_hash,
        )

        existing_rows = connection.execute(query).mappings().all()

        existing_by_id = {}

        for row in existing_rows:
            existing = dict(row)
            customer_id = int(existing["customer_id"])

            # Backfill hashes for existing records.
            if not existing["record_hash"]:
                existing["record_hash"] = _customer_hash(existing)

                connection.execute(
                    update(Customer)
                    .where(Customer.customer_id == customer_id)
                    .values(record_hash=existing["record_hash"])
                )

            existing_by_id[customer_id] = existing

        # Identify new, changed and unchanged records.
        for record in records:
            customer_id = record["customer_id"]

            existing = existing_by_id.get(customer_id)

            if existing is None:
                inserted.append(record)

            elif record["record_hash"] != existing["record_hash"]:
                updated.append(record)

            else:
                unchanged += 1

        # Insert new customers.
        if inserted:
            connection.execute(
                insert(Customer.__table__),
                inserted,
            )

        # Update only changed customers.
        for record in updated:
            connection.execute(
                update(Customer)
                .where(
                    Customer.customer_id == record["customer_id"]
                )
                .values(
                    customer_name=record["customer_name"],
                    email=record["email"],
                    city=record["city"],
                    signup_date=record["signup_date"],
                    record_hash=record["record_hash"],
                )
            )

    return {
        "inserted": len(inserted),
        "updated": len(updated),
        "unchanged": unchanged,
    }

class IngestionAudit(Base):
    __tablename__ = "ingestion_audit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clickhouse_inserted = Column(
        Integer, nullable=False, default=0
    )

    clickhouse_updated = Column(
        Integer, nullable=False, default=0
    )

    clickhouse_unchanged = Column(
        Integer, nullable=False, default=0
    )

    dag_run_id = Column(
        String(250),
        nullable=False,
        unique=True,
    )

    source_file = Column(String(500), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="RUNNING",
    )

    records_read = Column(Integer, nullable=False, default=0)
    inserted = Column(Integer, nullable=False, default=0)
    updated = Column(Integer, nullable=False, default=0)
    unchanged = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    error_message = Column(Text, nullable=True)

def start_ingestion_audit(run_id: str, source_file: str):
    now = datetime.now(timezone.utc)

    statement = insert(IngestionAudit.__table__).values(
        dag_run_id=run_id,
        source_file=source_file,
        status="RUNNING",
        records_read=0,
        inserted=0,
        updated=0,
        unchanged=0,
        started_at=now,
        completed_at=None,
        error_message=None,
    )

    statement = statement.on_conflict_do_update(
        index_elements=["dag_run_id"],
        set_={
            "source_file": source_file,
            "status": "RUNNING",
            "records_read": 0,
            "inserted": 0,
            "updated": 0,
            "unchanged": 0,
            "started_at": now,
            "completed_at": None,
            "error_message": None,
        },
    )

    with engine.begin() as connection:
        connection.execute(statement)


def complete_ingestion_audit(
    run_id: str,
    records_read: int,
    sync_result: dict,
    clickhouse_result: dict | None = None,
):
    clickhouse_result = clickhouse_result or {}

    statement = (
        update(IngestionAudit)
        .where(IngestionAudit.dag_run_id == run_id)
        .values(
            status="SUCCESS",
            records_read=records_read,
            inserted=sync_result["inserted"],
            updated=sync_result["updated"],
            unchanged=sync_result["unchanged"],
            clickhouse_inserted=clickhouse_result.get("inserted", 0),
            clickhouse_updated=clickhouse_result.get("updated", 0),
            clickhouse_unchanged=clickhouse_result.get("unchanged", 0),
            completed_at=datetime.now(timezone.utc),
            error_message=None,
        )
    )

    with engine.begin() as connection:
        result = connection.execute(statement)

        if result.rowcount != 1:
            raise ValueError(
                f"Audit record not found for run: {run_id}"
            )

def fail_ingestion_audit(run_id: str, error_message: str):
    statement = (
        update(IngestionAudit)
        .where(IngestionAudit.dag_run_id == run_id)
        .values(
            status="FAILED",
            completed_at=datetime.now(timezone.utc),
            error_message=str(error_message)[:4000],
        )
    )

    with engine.begin() as connection:
        connection.execute(statement)

def verify_customer_records(dataframe: pd.DataFrame) -> dict:
    """
    Verify that every source customer exists in PostgreSQL
    with the expected record hash.
    """
    records = _prepare_records(dataframe)

    if not records:
        raise ValueError("No customer records to verify")

    customer_ids = [
        record["customer_id"]
        for record in records
    ]

    expected_hashes = {
        record["customer_id"]: record["record_hash"]
        for record in records
    }

    query = select(
        Customer.customer_id,
        Customer.record_hash,
    ).where(
        Customer.customer_id.in_(customer_ids)
    )

    with engine.connect() as connection:
        rows = connection.execute(query).all()

    actual_hashes = {
        row.customer_id: row.record_hash
        for row in rows
    }

    missing = [
        customer_id
        for customer_id in customer_ids
        if customer_id not in actual_hashes
    ]

    mismatched = [
        customer_id
        for customer_id in customer_ids
        if customer_id in actual_hashes
        and actual_hashes[customer_id] != expected_hashes[customer_id]
    ]

    if missing or mismatched:
        raise ValueError(
            f"Customer verification failed. "
            f"Missing: {missing}, mismatched: {mismatched}"
        )

    return {
        "verified": len(records),
        "missing": 0,
        "mismatched": 0,
    }