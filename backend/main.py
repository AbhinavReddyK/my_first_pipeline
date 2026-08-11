"""FastAPI backend serving the clean_sales data produced by etl_pipeline.py."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import fetch_all

app = FastAPI(title="Sales Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/orders")
def get_orders():
    return fetch_all(
        """
        SELECT order_id, customer, product, quantity, price, order_date, total_price
        FROM clean_sales
        ORDER BY order_date
        """
    )


@app.get("/api/revenue-by-product")
def get_revenue_by_product():
    return fetch_all(
        """
        SELECT product, SUM(total_price) AS revenue
        FROM clean_sales
        GROUP BY product
        ORDER BY revenue DESC
        """
    )


@app.get("/api/summary")
def get_summary():
    rows = fetch_all(
        """
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(total_price), 0) AS total_revenue,
            COUNT(DISTINCT product) AS product_count
        FROM clean_sales
        """
    )
    return rows[0]
