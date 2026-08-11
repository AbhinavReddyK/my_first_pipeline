import pandas as pd

from etl_pipeline import extract, load, summarize_revenue_by_product, transform


def make_df(rows):
    return pd.DataFrame(
        rows,
        columns=["order_id", "customer", "product", "quantity", "price", "order_date"],
    )


def test_transform_drops_rows_with_nulls():
    df = make_df(
        [
            [1, "Alice", "Widget A", 3, 9.99, "2024-01-15"],
            [2, None, "Widget B", 2, 14.50, "2024-01-16"],
            [3, "Bob", "Widget C", None, 18.75, "2024-01-17"],
            [4, "Carla", "Widget D", 1, None, "2024-01-18"],
        ]
    )
    result = transform(df)
    assert len(result) == 1
    assert result.iloc[0]["customer"] == "Alice"


def test_transform_drops_duplicates():
    df = make_df(
        [
            [1, "Alice", "Widget A", 3, 9.99, "2024-01-15"],
            [1, "Alice", "Widget A", 3, 9.99, "2024-01-15"],
        ]
    )
    result = transform(df)
    assert len(result) == 1


def test_transform_keeps_latest_row_per_order_id():
    df = make_df(
        [
            [1, "Alice", "Widget A", 6, 9.95, "2024-01-25"],
            [1, "Alice", "Widget A", 6, 9.99, "2024-01-25"],
        ]
    )
    result = transform(df)
    assert len(result) == 1
    assert result.iloc[0]["price"] == 9.99


def test_transform_normalizes_mixed_date_formats():
    df = make_df(
        [
            [1, "Alice", "Widget A", 1, 10.0, "2024-01-15"],
            [2, "Bob", "Widget B", 1, 10.0, "01/16/2024"],
            [3, "Carla", "Widget C", 1, 10.0, "2024/01/17"],
            [4, "Dan", "Widget D", 1, 10.0, "01-18-2024"],
        ]
    )
    result = transform(df)
    assert list(result["order_date"]) == [
        "2024-01-15",
        "2024-01-16",
        "2024-01-17",
        "2024-01-18",
    ]


def test_transform_drops_unparseable_or_missing_dates():
    df = make_df(
        [
            [1, "Alice", "Widget A", 1, 10.0, "2024-01-15"],
            [2, "Bob", "Widget B", 1, 10.0, "not_a_date"],
            [3, "Carla", "Widget C", 1, 10.0, "2024-13-45"],
            [4, "Dan", "Widget D", 1, 10.0, None],
        ]
    )
    result = transform(df)
    assert len(result) == 1
    assert result.iloc[0]["customer"] == "Alice"


def test_transform_adds_total_price_column():
    df = make_df([[1, "Alice", "Widget A", 3, 9.99, "2024-01-15"]])
    result = transform(df)
    assert result.iloc[0]["total_price"] == 3 * 9.99


def test_transform_quantity_is_int():
    df = make_df([[1, "Alice", "Widget A", 3.0, 9.99, "2024-01-15"]])
    result = transform(df)
    assert result.iloc[0]["quantity"] == 3
    assert result["quantity"].dtype.kind == "i"


def test_extract_reads_csv(tmp_path):
    csv_path = tmp_path / "input.csv"
    make_df([[1, "Alice", "Widget A", 3, 9.99, "2024-01-15"]]).to_csv(csv_path, index=False)

    result = extract(str(csv_path))

    assert len(result) == 1
    assert result.iloc[0]["customer"] == "Alice"


def test_summarize_revenue_by_product():
    df = make_df(
        [
            [1, "Alice", "Widget A", 3, 10.0, "2024-01-15"],
            [2, "Bob", "Widget A", 1, 10.0, "2024-01-16"],
            [3, "Carla", "Widget B", 2, 5.0, "2024-01-17"],
        ]
    )
    clean = transform(df)

    result = summarize_revenue_by_product(clean)

    assert result["Widget A"] == 40.0
    assert result["Widget B"] == 10.0
    assert list(result.index) == ["Widget A", "Widget B"]  # sorted descending by revenue


def test_load_writes_csv(tmp_path):
    out_path = tmp_path / "output.csv"
    df = make_df([[1, "Alice", "Widget A", 3, 9.99, "2024-01-15"]])

    load(df, str(out_path))

    assert out_path.exists()
    reloaded = pd.read_csv(out_path)
    assert reloaded.iloc[0]["customer"] == "Alice"


def test_extract_transform_load_roundtrip(tmp_path):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    make_df(
        [
            [1, "Alice", "Widget A", 3, 9.99, "2024-01-15"],
            [1, "Alice", "Widget A", 3, 9.99, "2024-01-15"],
            [2, None, "Widget B", 2, 14.50, "2024-01-16"],
        ]
    ).to_csv(input_path, index=False)

    raw = extract(str(input_path))
    clean = transform(raw)
    load(clean, str(output_path))

    assert len(raw) == 3
    assert len(clean) == 1
    reloaded = pd.read_csv(output_path)
    assert list(reloaded.columns) == [
        "order_id",
        "customer",
        "product",
        "quantity",
        "price",
        "order_date",
        "total_price",
    ]
