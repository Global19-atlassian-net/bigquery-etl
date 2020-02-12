r"""Generate a query for incremental processing of scalar aggregates.

```bash
python -m bigquery_etl.glam.scalar_aggregates_incremental \
    > sql/telemetry_derived/clients_scalar_aggregates_v1/query.sql
```
"""
from jinja2 import Environment, PackageLoader
from bigquery_etl.format_sql.formatter import reformat
from typing import List


def render(
    header: str,
    user_data_type: str,
    user_data_attributes: List[str],
    attributes: List[str],
    extract_select_clause: str,
    join_filter: str,
    source_table: str,
    destination_table: str,
) -> str:
    env = Environment(loader=PackageLoader("bigquery_etl", "glam/templates"))
    main_sql = env.get_template("clients_scalar_aggregates_v1.sql")
    return reformat(
        main_sql.render(
            header=header,
            user_data_type=user_data_type,
            user_data_attributes=",".join(user_data_attributes),
            attributes=",".join(attributes),
            attributes_list=attributes,
            extract_select_clause=extract_select_clause,
            join_filter=join_filter,
            source_table=source_table,
            destination_table=destination_table,
        )
    )


def main():
    """Generate `telemetry_derived.clients_scalar_aggregates_v1`."""

    module_name = "bigquery_etl.glam.scalar_aggregates_incremental"
    header = f"-- generated by: python3 -m {module_name}"

    rendered = render(
        source_table="clients_daily_scalar_aggregates_v1",
        destination_table="clients_scalar_aggregates_v1",
        header=header,
        user_data_type="""
            ARRAY<
                STRUCT<
                metric STRING,
                metric_type STRING,
                key STRING,
                process STRING,
                agg_type STRING,
                value FLOAT64
                >
            >
        """,
        user_data_attributes=[
            "metric",
            "metric_type",
            "key",
            "process",
            # [agg_type, value] are shared between telemetry and glean
        ],
        attributes=["client_id", "os", "app_version", "app_build_id", "channel"],
        extract_select_clause=f"""
            * EXCEPT(app_version),
            CAST(app_version AS INT64) as app_version
        """,
        join_filter="""
            LEFT JOIN
                latest_versions
            USING
                (channel)
            WHERE
                app_version >= (latest_version - 2)
        """,
    )
    print(rendered)


if __name__ == "__main__":
    main()
