import logging
import sys
from pathlib import Path

# Add project root to Python's import path FIRST
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Import project modules AFTER setting the path
from src.ingestion.csv_ingestor import load_csv
from src.quality.customer_validator import validate_customers

logging.basicConfig(level=logging.INFO)

CSV_PATH = PROJECT_ROOT / "data" / "sample" / "customers.csv"


def main():
    # Step 1: Ingest CSV
    dataframe = load_csv(CSV_PATH)

    print("\nIngested data:")
    print(dataframe)

    print("\nDataset summary:")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {list(dataframe.columns)}")

    # Step 2: Validate customer records
    validated_data = validate_customers(dataframe)

    print("\nData quality validation: PASSED")
    print(f"Validated records: {len(validated_data)}")

    print("\nColumn types:")
    print(validated_data.dtypes)


if __name__ == "__main__":
    main()