import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.csv_ingestor import load_csv
from src.quality.customer_validator import validate_customers
from src.storage.postgres import create_tables, upsert_customers


def main():
    csv_path = (
        PROJECT_ROOT / "data" / "sample" / "customers.csv"
    )

    # 1. Ingest
    dataframe = load_csv(csv_path)

    # 2. Validate
    validated_data = validate_customers(dataframe)

    # 3. Create database table
    create_tables()

    # 4. Insert or update records
    records_processed = upsert_customers(validated_data)

    print("\nPostgreSQL ingestion completed!")
    print(f"Records processed: {records_processed}")


if __name__ == "__main__":
    main()
