import logging
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context

from src.ingestion.csv_ingestor import load_csv
from src.quality.customer_validator import validate_customers

from src.storage.postgres import (
    create_tables,
    sync_customers,
    verify_customer_records,
    start_ingestion_audit,
    complete_ingestion_audit,
    fail_ingestion_audit,
)

from src.storage.clickhouse import (
    sync_customers_to_clickhouse,
    verify_customers_in_clickhouse,
)


logger = logging.getLogger(__name__)

CSV_PATH = Path(
    "/opt/airflow/project/data/sample/customers.csv"
)

default_args = {
    "owner": "abdulla",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


def start_audit():
    context = get_current_context()
    run_id = context["run_id"]

    create_tables()

    start_ingestion_audit(
        run_id=run_id,
        source_file=str(CSV_PATH),
    )

    logger.info("Started ingestion audit: %s", run_id)

    return run_id


def extract_customers():
    dataframe = load_csv(CSV_PATH)

    logger.info(
        "Extracted %s customer records",
        len(dataframe),
    )

    return len(dataframe)


def validate_customer_data():
    dataframe = load_csv(CSV_PATH)
    validated_data = validate_customers(dataframe)

    logger.info(
        "Customer validation successful: %s records",
        len(validated_data),
    )

    return len(validated_data)


def load_customer_data():
    dataframe = load_csv(CSV_PATH)
    validated_data = validate_customers(dataframe)

    result = sync_customers(validated_data)

    logger.info(
        "PostgreSQL synchronization completed: %s",
        result,
    )

    return result


def sync_clickhouse_data():
    dataframe = load_csv(CSV_PATH)
    validated_data = validate_customers(dataframe)

    result = sync_customers_to_clickhouse(validated_data)

    logger.info(
        "ClickHouse synchronization completed: %s",
        result,
    )

    return result


def verify_postgres_data():
    dataframe = load_csv(CSV_PATH)
    validated_data = validate_customers(dataframe)

    result = verify_customer_records(validated_data)

    logger.info(
        "PostgreSQL verification successful: %s",
        result,
    )

    return result


def verify_clickhouse_data():
    dataframe = load_csv(CSV_PATH)
    validated_data = validate_customers(dataframe)

    result = verify_customers_in_clickhouse(validated_data)

    logger.info(
        "ClickHouse verification successful: %s",
        result,
    )

    return result


def complete_audit():
    context = get_current_context()
    ti = context["ti"]
    run_id = context["run_id"]

    records_read = ti.xcom_pull(
        task_ids="validate_customers"
    )

    postgres_result = ti.xcom_pull(
        task_ids="load_customers"
    )

    clickhouse_result = ti.xcom_pull(
        task_ids="sync_clickhouse"
    )

    complete_ingestion_audit(
        run_id=run_id,
        records_read=records_read,
        sync_result=postgres_result,
        clickhouse_result=clickhouse_result,
    )

    logger.info(
        "Completed ingestion audit successfully: %s",
        run_id,
    )


def record_pipeline_failure(context):
    run_id = context.get("run_id")
    exception = context.get("exception")

    if not run_id:
        logger.error("Unable to identify failed DAG run")
        return

    try:
        fail_ingestion_audit(
            run_id=run_id,
            error_message=str(
                exception or "Unknown pipeline failure"
            ),
        )

        logger.error(
            "Ingestion audit marked FAILED: %s",
            run_id,
        )

    except Exception:
        logger.exception(
            "Unable to update ingestion audit for run: %s",
            run_id,
        )


with DAG(
    dag_id="customer_ingestion_pipeline",
    default_args=default_args,
    description=(
        "Incremental customer ingestion into PostgreSQL "
        "and ClickHouse with audit tracking"
    ),
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=[
        "data-engineering",
        "postgresql",
        "clickhouse",
        "incremental-ingestion",
        "audit",
    ],
) as dag:

    audit_start = PythonOperator(
        task_id="start_ingestion_audit",
        python_callable=start_audit,
    )

    extract = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers,
        on_failure_callback=record_pipeline_failure,
    )

    validate = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customer_data,
        on_failure_callback=record_pipeline_failure,
    )

    load_postgres = PythonOperator(
        task_id="load_customers",
        python_callable=load_customer_data,
        on_failure_callback=record_pipeline_failure,
    )

    sync_clickhouse = PythonOperator(
        task_id="sync_clickhouse",
        python_callable=sync_clickhouse_data,
        on_failure_callback=record_pipeline_failure,
    )

    verify_postgres = PythonOperator(
        task_id="verify_postgres",
        python_callable=verify_postgres_data,
        on_failure_callback=record_pipeline_failure,
    )

    verify_clickhouse = PythonOperator(
        task_id="verify_clickhouse",
        python_callable=verify_clickhouse_data,
        on_failure_callback=record_pipeline_failure,
    )

    audit_complete = PythonOperator(
        task_id="complete_ingestion_audit",
        python_callable=complete_audit,
        on_failure_callback=record_pipeline_failure,
    )

    (
        audit_start
        >> extract
        >> validate
        >> load_postgres
        >> sync_clickhouse
        >> verify_postgres
        >> verify_clickhouse
        >> audit_complete
    )