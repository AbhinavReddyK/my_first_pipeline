"""Simple ETL pipeline: extract sales data, clean it, and load the result."""

import os

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

SOURCE_FILE = "sample_data.csv"
OUTPUT_FILE = "clean_data.csv"

PG_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "sales_pipeline",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
}
PG_TABLE = "clean_sales"
PG_COLUMNS = ["order_id", "customer", "product", "quantity", "price", "order_date", "total_price"]


def extract(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Bad dates come in mixed formats (or are missing/garbage); coerce unparseable ones to NaT.
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

    df = df.dropna(subset=["customer", "quantity", "price", "order_date"])
    df = df.drop_duplicates()
    # order_id is the business key Postgres upserts on; rows that share an order_id
    # but disagree on other fields (e.g. a corrected price) aren't caught by drop_duplicates(),
    # so keep only the most recent row per order_id.
    df = df.drop_duplicates(subset=["order_id"], keep="last")

    df["quantity"] = df["quantity"].astype(int)
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df["total_price"] = df["quantity"] * df["price"]

    return df.reset_index(drop=True)


def load(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)


def load_to_postgres(df: pd.DataFrame) -> None:
    update_columns = [c for c in PG_COLUMNS if c != "order_id"]
    set_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_columns)

    conn = psycopg2.connect(**PG_CONFIG)
    try:
        with conn.cursor() as cur:
            execute_values(
                cur,
                f"""
                INSERT INTO {PG_TABLE} ({', '.join(PG_COLUMNS)}) VALUES %s
                ON CONFLICT (order_id) DO UPDATE SET {set_clause}
                """,
                df[PG_COLUMNS].values.tolist(),
            )
        conn.commit()
    finally:
        conn.close()


def summarize_revenue_by_product(df: pd.DataFrame) -> pd.Series:
    return df.groupby("product")["total_price"].sum().sort_values(ascending=False)


def main() -> None:
    raw = extract(SOURCE_FILE)
    clean = transform(raw)
    load(clean, OUTPUT_FILE)
    load_to_postgres(clean)

    print("ETL Summary")
    print("-----------")
    print(f"Records before cleaning: {len(raw)}")
    print(f"Records after cleaning:  {len(clean)}")
    print(f"Records removed:         {len(raw) - len(clean)}")
    print(f"Clean data written to:   {OUTPUT_FILE}")
    print(f"Clean data loaded to:    {PG_CONFIG['dbname']}.{PG_TABLE} ({len(clean)} rows)")

    print()
    print("Revenue by Product")
    print("-------------------")
    for product, revenue in summarize_revenue_by_product(clean).items():
        print(f"{product}: {revenue:.2f}")


if __name__ == "__main__":
    main()
