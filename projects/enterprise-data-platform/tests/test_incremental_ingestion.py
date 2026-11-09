from datetime import date

import pandas as pd
import pytest

from src.storage.postgres import (
    _customer_hash,
    _prepare_records,
)


@pytest.fixture
def customer_record():
    return {
        "customer_id": 101,
        "customer_name": "Aarav Sharma",
        "email": "aarav@example.com",
        "city": "Bengaluru",
        "signup_date": "2026-01-10",
    }


def test_customer_hash_is_deterministic(customer_record):
    hash_one = _customer_hash(customer_record)
    hash_two = _customer_hash(customer_record)

    assert hash_one == hash_two


def test_customer_hash_changes_when_data_changes(customer_record):
    original_hash = _customer_hash(customer_record)

    modified_record = customer_record.copy()
    modified_record["city"] = "Mumbai"

    modified_hash = _customer_hash(modified_record)

    assert original_hash != modified_hash


def test_customer_hash_uses_all_relevant_fields(customer_record):
    original_hash = _customer_hash(customer_record)

    fields_to_modify = [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "signup_date",
    ]

    for field in fields_to_modify:
        modified_record = customer_record.copy()

        if field == "signup_date":
            modified_record[field] = "2026-02-10"
        elif field == "customer_id":
            modified_record[field] = 102
        else:
            modified_record[field] = "modified_value"

        assert _customer_hash(modified_record) != original_hash


def test_prepare_records_normalizes_customer_data(customer_record):
    dataframe = pd.DataFrame([customer_record])

    records = _prepare_records(dataframe)

    assert len(records) == 1
    assert records[0]["customer_id"] == 101
    assert records[0]["signup_date"] == date(2026, 1, 10)
    assert isinstance(records[0]["record_hash"], str)
    assert len(records[0]["record_hash"]) == 64


def test_prepare_records_handles_empty_dataframe():
    dataframe = pd.DataFrame(
        columns=[
            "customer_id",
            "customer_name",
            "email",
            "city",
            "signup_date",
        ]
    )

    records = _prepare_records(dataframe)

    assert records == []
