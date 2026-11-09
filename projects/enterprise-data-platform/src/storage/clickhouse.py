import logging
from datetime import datetime, timezone

import clickhouse_connect
import pandas as pd

from sqlalchemy import select

from src.config import settings
from src.storage.postgres import (
    Customer,
    engine as postgres_engine,
    _prepare_records,
)


logger = logging.getLogger(__name__)

TABLE_NAME = "customers_analytics"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS customers_analytics
(
    customer_id UInt64,
    customer_name String,
    email String,
    city String,
    signup_date Date,
    record_hash FixedString(64),
    version UInt64,
    synced_at DateTime64(6, 'UTC')
)
ENGINE = ReplacingMergeTree(version)
ORDER BY customer_id
"""


def get_clickhouse_client():
    """Create an authenticated ClickHouse client."""

    return clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DATABASE,
    )


def create_analytics_tables():
    """Create the analytical customer table if it doesn't exist."""

    client = get_clickhouse_client()

    try:
        client.command(CREATE_TABLE_SQL)
        logger.info("ClickHouse analytics table is ready")
    finally:
        client.close()


def sync_customers_to_clickhouse(dataframe: pd.DataFrame) -> dict:
    """
    Synchronize PostgreSQL customer records into ClickHouse.

    PostgreSQL remains the source of truth.
    Only new and changed records are inserted into ClickHouse.
    """

    if dataframe.empty:
        return {
            "inserted": 0,
            "updated": 0,
            "unchanged": 0,
        }

    customer_ids = sorted(
        set(int(value) for value in dataframe["customer_id"])
    )

    # Fetch the authoritative records from PostgreSQL.
    source_query = select(
        Customer.customer_id,
        Customer.customer_name,
        Customer.email,
        Customer.city,
        Customer.signup_date,
    ).where(
        Customer.customer_id.in_(customer_ids)
    )

    with postgres_engine.connect() as connection:
        source_rows = [
            dict(row)
            for row in connection.execute(
                source_query
            ).mappings().all()
        ]

    if len(source_rows) != len(customer_ids):
        raise ValueError(
            "PostgreSQL records do not match the requested customer IDs"
        )

    records = _prepare_records(pd.DataFrame(source_rows))

    client = get_clickhouse_client()

    try:
        client.command(CREATE_TABLE_SQL)

        ids_sql = ", ".join(
            str(customer_id)
            for customer_id in customer_ids
        )

        # Read latest logical versions, including records not yet merged.
        existing_rows = client.query(
            f"""
            SELECT customer_id, record_hash
            FROM {TABLE_NAME} FINAL
            WHERE customer_id IN ({ids_sql})
            """
        ).result_rows

        existing_hashes = {
            int(row[0]): (
                row[1].decode().rstrip("\x00")
                if isinstance(row[1], bytes)
                else str(row[1]).rstrip("\x00")
            )
            for row in existing_rows
        }

        inserted = []
        updated = []
        unchanged = 0

        for record in records:
            customer_id = record["customer_id"]
            existing_hash = existing_hashes.get(customer_id)

            if existing_hash is None:
                inserted.append(record)

            elif existing_hash == record["record_hash"]:
                unchanged += 1

            else:
                updated.append(record)

        records_to_write = inserted + updated

        if records_to_write:
            now = datetime.now(timezone.utc)

            version = int(now.timestamp() * 1_000_000)

            rows = [
                [
                    record["customer_id"],
                    record["customer_name"],
                    record["email"],
                    record["city"],
                    record["signup_date"],
                    record["record_hash"],
                    version,
                    now,
                ]
                for record in records_to_write
            ]

            client.insert(
                TABLE_NAME,
                rows,
                column_names=[
                    "customer_id",
                    "customer_name",
                    "email",
                    "city",
                    "signup_date",
                    "record_hash",
                    "version",
                    "synced_at",
                ],
            )

        result = {
            "inserted": len(inserted),
            "updated": len(updated),
            "unchanged": unchanged,
        }

        logger.info(
            "ClickHouse synchronization completed: %s",
            result,
        )

        return result

    finally:
        client.close()

def verify_customers_in_clickhouse(dataframe: pd.DataFrame) -> dict:
    """
    Verify that ClickHouse contains the latest versions
    of the requested PostgreSQL customer records.
    """

    if dataframe.empty:
        return {
            "verified": 0,
            "missing": 0,
            "mismatched": 0,
        }

    customer_ids = sorted(
        set(int(value) for value in dataframe["customer_id"])
    )

    # PostgreSQL is the authoritative source.
    source_query = select(
        Customer.customer_id,
        Customer.customer_name,
        Customer.email,
        Customer.city,
        Customer.signup_date,
    ).where(
        Customer.customer_id.in_(customer_ids)
    )

    with postgres_engine.connect() as connection:
        source_rows = [
            dict(row)
            for row in connection.execute(
                source_query
            ).mappings().all()
        ]

    if len(source_rows) != len(customer_ids):
        raise ValueError(
            "Some requested customers are missing from PostgreSQL"
        )

    expected_records = _prepare_records(
        pd.DataFrame(source_rows)
    )

    expected_hashes = {
        record["customer_id"]: record["record_hash"]
        for record in expected_records
    }

    ids_sql = ", ".join(str(value) for value in customer_ids)

    client = get_clickhouse_client()

    try:
        rows = client.query(
            f"""
            SELECT customer_id, record_hash
            FROM {TABLE_NAME} FINAL
            WHERE customer_id IN ({ids_sql})
            """
        ).result_rows

        actual_hashes = {
            int(row[0]): (
                row[1].decode().rstrip("\x00")
                if isinstance(row[1], bytes)
                else str(row[1]).rstrip("\\x00")
            )
            for row in rows
        }

    finally:
        client.close()

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
            f"ClickHouse verification failed. "
            f"Missing: {missing}, mismatched: {mismatched}"
        )

    return {
        "verified": len(customer_ids),
        "missing": 0,
        "mismatched": 0,
    }
