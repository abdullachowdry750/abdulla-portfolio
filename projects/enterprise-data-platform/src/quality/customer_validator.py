import pandas as pd


REQUIRED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "city",
    "signup_date",
]


def validate_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Validate customer records and return a normalized DataFrame.

    Raises ValueError when data quality checks fail.
    """
    df = dataframe.copy()
    errors = []

    # 1. Required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # 2. Required fields cannot be null or blank
    for column in REQUIRED_COLUMNS:
        if df[column].isna().any():
            errors.append(f"{column} contains null values")

    for column in ["customer_name", "email", "city"]:
        if df[column].astype("string").str.strip().eq("").any():
            errors.append(f"{column} contains blank values")

    # 3. Customer ID must be unique and positive
    numeric_ids = pd.to_numeric(
        df["customer_id"], errors="coerce"
    )

    if numeric_ids.isna().any():
        errors.append("customer_id contains invalid values")
    elif (numeric_ids <= 0).any():
        errors.append("customer_id must be positive")
    elif (numeric_ids % 1 != 0).any():
        errors.append("customer_id must contain integers")

    if df["customer_id"].duplicated().any():
        errors.append("Duplicate customer_id values found")

    # 4. Email must be unique and have a basic valid format
    emails = df["email"].astype("string").str.strip()

    if emails.duplicated().any():
        errors.append("Duplicate email values found")

    if not emails.str.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        na=False
    ).all():
        errors.append("Invalid email addresses found")

    # 5. Signup date must be valid
    parsed_dates = pd.to_datetime(
        df["signup_date"], errors="coerce"
    )

    if parsed_dates.isna().any():
        errors.append("Invalid signup_date values found")

    if errors:
        raise ValueError(
            "Customer data validation failed:\n- "
            + "\n- ".join(errors)
        )

    df["customer_id"] = numeric_ids.astype("int64")
    df["signup_date"] = parsed_dates

    return df
