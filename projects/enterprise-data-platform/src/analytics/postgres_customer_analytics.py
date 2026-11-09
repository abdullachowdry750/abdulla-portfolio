from sqlalchemy import func, select

from src.storage.postgres import Customer, engine


def get_customer_analytics() -> dict:
    """
    Generate customer analytics directly from PostgreSQL.

    This implementation is intended for the GCP deployment.
    The existing ClickHouse analytics implementation remains
    available for local Docker development.
    """

    customer_count = func.count(Customer.customer_id)
    month_expression = func.date_trunc(
        "month",
        Customer.signup_date,
    )

    with engine.connect() as connection:

        # Customer distribution by city
        city_query = (
            select(
                Customer.city,
                customer_count.label("customer_count"),
            )
            .group_by(Customer.city)
            .order_by(customer_count.desc(), Customer.city.asc())
        )

        city_rows = connection.execute(city_query).all()

        city_distribution = [
            {
                "city": str(row.city),
                "customer_count": int(row.customer_count),
            }
            for row in city_rows
        ]

        # Monthly customer signups
        monthly_query = (
            select(
                month_expression.label("signup_month"),
                customer_count.label("new_customers"),
            )
            .group_by(month_expression)
            .order_by(month_expression.asc())
        )

        monthly_rows = connection.execute(monthly_query).all()

        monthly_signups = [
            {
                "signup_month": (
                    row.signup_month.date().isoformat()
                    if hasattr(row.signup_month, "date")
                    else row.signup_month.isoformat()
                ),
                "new_customers": int(row.new_customers),
            }
            for row in monthly_rows
        ]

        # Overall customer metrics
        summary_query = select(
            customer_count.label("total_customers"),
            func.count(func.distinct(Customer.city)).label("unique_cities"),
            func.min(Customer.signup_date).label("first_signup"),
            func.max(Customer.signup_date).label("latest_signup"),
        )

        summary_row = connection.execute(summary_query).one()

        summary = {
            "total_customers": int(summary_row.total_customers),
            "unique_cities": int(summary_row.unique_cities),
            "first_signup": (
                summary_row.first_signup.isoformat()
                if summary_row.first_signup else None
            ),
            "latest_signup": (
                summary_row.latest_signup.isoformat()
                if summary_row.latest_signup else None
            ),
        }

    return {
        "summary": summary,
        "city_distribution": city_distribution,
        "monthly_signups": monthly_signups,
    }
