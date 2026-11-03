import logging
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.csv_ingestor import load_csv
from src.quality.customer_validator import validate_customers
from src.storage.postgres import (
    create_tables,
    upsert_customers,
    engine,
    Customer,
)

from sqlalchemy import select, func


logger = logging.getLogger(__name__)

CSV_PATH = Path("/opt/airflow/project/data/sample/customers.csv")


default_args = {
    "owner": "abdulla",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


def extract_customers():
    dataframe = load_csv(CSV_PATH)

    logger.info("Extracted %s customer records", len(dataframe))

    return len(dataframe)


def validate_customer_data():
    dataframe = load_csv(CSV_PATH)

    validated_data = validate_customers(dataframe)

    logger.info(
        "Validation successful. Records: %s",
        len(validated_data),
    )

    return len(validated_data)


def load_customer_data():
    dataframe = load_csv(CSV_PATH)

    validated_data = validate_customers(dataframe)

    create_tables()

    records_loaded = upsert_customers(validated_data)

    logger.info(
        "PostgreSQL load completed. Records processed: %s",
        records_loaded,
    )

    return records_loaded


def verify_customer_data():
    with engine.connect() as connection:
        count = connection.execute(
            select(func.count()).select_from(Customer)
        ).scalar_one()

    logger.info("Total customers currently in PostgreSQL: %s", count)

    if count == 0:
        raise ValueError("PostgreSQL verification failed: no customers found")

    return count


with DAG(
    dag_id="customer_ingestion_pipeline",
    default_args=default_args,
    description="Automated customer CSV ingestion and PostgreSQL loading",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "postgresql", "ingestion"],
) as dag:

    extract = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers,
    )

    validate = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customer_data,
    )

    load = PythonOperator(
        task_id="load_customers",
        python_callable=load_customer_data,
    )

    verify = PythonOperator(
        task_id="verify_customers",
        python_callable=verify_customer_data,
    )

    extract >> validate >> load >> verify