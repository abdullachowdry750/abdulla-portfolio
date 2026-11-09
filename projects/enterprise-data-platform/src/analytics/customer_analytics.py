from src.storage.clickhouse import get_clickhouse_client


def get_customer_analytics() -> dict:
    """
    Retrieve customer analytics from ClickHouse.

    PostgreSQL is the source of truth.
    ClickHouse provides the analytical read layer.
    """

    client = get_clickhouse_client()

    try:
        # 1. Customer distribution by city
        city_rows = client.query("""
            SELECT
                city,
                count() AS customer_count
            FROM customers_analytics FINAL
            GROUP BY city
            ORDER BY customer_count DESC, city
        """).result_rows

        city_distribution = [
            {
                "city": str(row[0]),
                "customer_count": int(row[1]),
            }
            for row in city_rows
        ]

        # 2. Monthly customer signups
        monthly_rows = client.query("""
            SELECT
                toStartOfMonth(signup_date) AS signup_month,
                count() AS new_customers
            FROM customers_analytics FINAL
            GROUP BY signup_month
            ORDER BY signup_month
        """).result_rows

        monthly_signups = [
            {
                "signup_month": row[0].isoformat(),
                "new_customers": int(row[1]),
            }
            for row in monthly_rows
        ]

        # 3. Overall customer metrics
        summary_row = client.query("""
            SELECT
                count() AS total_customers,
                uniqExact(city) AS unique_cities,
                min(signup_date) AS first_signup,
                max(signup_date) AS latest_signup
            FROM customers_analytics FINAL
        """).result_rows[0]

        summary = {
            "total_customers": int(summary_row[0]),
            "unique_cities": int(summary_row[1]),
            "first_signup": (
                summary_row[2].isoformat()
                if summary_row[2] else None
            ),
            "latest_signup": (
                summary_row[3].isoformat()
                if summary_row[3] else None
            ),
        }

        return {
            "summary": summary,
            "city_distribution": city_distribution,
            "monthly_signups": monthly_signups,
        }

    finally:
        client.close()
