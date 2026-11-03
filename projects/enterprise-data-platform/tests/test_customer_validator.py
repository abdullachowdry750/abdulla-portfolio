import pandas as pd
import pytest

from src.quality.customer_validator import validate_customers


@pytest.fixture
def valid_customers():
    return pd.DataFrame({
        "customer_id": [1, 2, 3],
        "customer_name": ["Aarav", "Sara", "Rahul"],
        "email": [
            "aarav@example.com",
            "sara@example.com",
            "rahul@example.com",
        ],
        "city": ["Bengaluru", "Mumbai", "Delhi"],
        "signup_date": [
            "2026-01-10",
            "2026-01-12",
            "2026-01-15",
        ],
    })


def test_valid_customers_pass(valid_customers):
    result = validate_customers(valid_customers)

    assert len(result) == 3
    assert result["customer_id"].dtype == "int64"
    assert pd.api.types.is_datetime64_any_dtype(
        result["signup_date"]
    )


def test_duplicate_customer_ids_rejected(valid_customers):
    valid_customers.loc[1, "customer_id"] = 1

    with pytest.raises(ValueError, match="Duplicate customer_id"):
        validate_customers(valid_customers)


def test_invalid_email_rejected(valid_customers):
    valid_customers.loc[0, "email"] = "invalid-email"

    with pytest.raises(ValueError, match="Invalid email"):
        validate_customers(valid_customers)


def test_missing_column_rejected(valid_customers):
    valid_customers = valid_customers.drop(columns=["city"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_customers(valid_customers)
