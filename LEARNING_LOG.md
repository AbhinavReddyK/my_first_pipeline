# Learning Log — my_first_pipeline

A track of what I've learned so far, reconstructed from the project files (built Jul 15 – Aug 5, 2026). Sharing this with my mentor for guidance on what to tackle next.

## Project in one line
A small end-to-end data pipeline: messy CSV → cleaned with pandas → loaded into Postgres → served by a FastAPI backend → visualized in a React dashboard. Backed by a pytest test suite.

---

## 1. Pandas fundamentals (`pandas_practice.py`)
Practiced the basics on a small hand-built DataFrame before using them for real:
- Creating a DataFrame from a dict of columns
- Selecting columns (`df['city']`, `df[['name','salary']]`)
- Boolean filtering (`df[df['salary'] >= 85000]`)
- Combining conditions with `&` and `|`
- Inspecting data: `.head()`, `.shape`, `.info()`, `.describe()`, `.dtypes`
- Finding missing values with `.isnull().sum()`
- **In progress:** was about to practice cleaning a DataFrame with nulls in every column (`data2`) — next step is likely `dropna()` / `fillna()` on real messy data.

## 2. Data cleaning / ETL logic (`etl_pipeline.py`)
Applied the pandas basics to a real "dirty" sales dataset:
- **Extract**: reading CSV with `pd.read_csv`
- **Transform**, in order:
  - Parsing inconsistent date formats in one column using `pd.to_datetime(..., format="mixed", errors="coerce")`
  - Dropping rows missing required fields with `dropna(subset=[...])`
  - Removing exact duplicate rows with `drop_duplicates()`
  - Handling a subtler case: duplicate `order_id`s with *different* values (e.g. a corrected price) — solved with `drop_duplicates(subset=["order_id"], keep="last")` to keep the business key unique
  - Type coercion (`astype(int)`) and derived columns (`total_price = quantity * price`)
- **Load**: writing the clean result back to CSV, and separately upserting into Postgres

**Key idea learned:** "clean data" isn't just dropping nulls — real datasets have structural issues (mixed formats, semantic duplicates on a business key) that need explicit rules.

## 3. SQL / Postgres integration (`etl_pipeline.py`, `backend/db.py`)
- Connecting to Postgres from Python with `psycopg2`
- Bulk inserts with `execute_values`
- **Upsert pattern**: `INSERT ... ON CONFLICT (order_id) DO UPDATE SET ...` so re-running the pipeline updates existing rows instead of erroring or duplicating
- Reading config (like `PGPASSWORD`) from environment variables instead of hardcoding secrets
- Safe connection handling with `try/finally` to always close the connection
- Read-side: `RealDictCursor` to get query results back as plain dicts instead of tuples

## 4. Automated testing (`test_etl_pipeline.py`)
Wrote a pytest suite (11 cases) covering:
- Happy path and edge cases separately (nulls, exact dupes, same-key-different-value dupes)
- Date-format edge cases: valid mixed formats vs. genuinely unparseable/missing dates
- Type assertions (`quantity` stays an int after transform)
- Using `tmp_path` (pytest's built-in fixture) to test file I/O without touching real files
- A full roundtrip test (extract → transform → load) to check the pieces work together, not just in isolation

**Key idea learned:** testing the *behavior* (what should be dropped/kept/computed) rather than just "does it run."

## 5. Backend API design (`backend/main.py`, `backend/db.py`)
- Built a small FastAPI service with three read-only endpoints (`/api/orders`, `/api/revenue-by-product`, `/api/summary`)
- Separated concerns: `db.py` owns the connection/query logic, `main.py` owns routing — the API layer doesn't know about `psycopg2` directly
- Configured CORS middleware to explicitly allow only the frontend's dev origin (`localhost:5173`) and only `GET`
- Used SQL aggregation (`GROUP BY`, `SUM`, `COUNT`, `COUNT DISTINCT`) instead of pulling all rows and aggregating in Python

## 6. Frontend basics (`frontend/`)
- Scaffolded with Vite + React 19
- Used `useState`/`useEffect` to fetch data on mount
- Fetched multiple endpoints concurrently with `Promise.all` rather than sequential awaits
- Basic error-state handling in the UI (shows a message if the API call fails, with a hint to check the backend)
- Split the UI into focused components: `SummaryCards`, `RevenueChart` (using the `recharts` library), `OrdersTable`
- Kept API calls in one place (`api.js`) instead of scattering `fetch` calls across components

## 7. Environment / tooling
- Set up an isolated Python virtual environment (`.venv`) and iterated on it (first tried a throwaway `.venv_test` to test something, then removed it)
- Managed Python deps via `requirements.txt`
- Managed JS deps via `package.json` / npm, with `oxlint` for linting

---

## What's unfinished / good topics for mentor guidance
1. `pandas_practice.py` stops right before cleaning a DataFrame with nulls — natural next step (`dropna`, `fillna`, `isnull` in practice).
2. No `.env` file or secrets management shown — `PGPASSWORD` is read from the environment but there's no documented setup step for it.
3. No CI, no error handling around a missing/unreachable Postgres connection in the FastAPI layer (a bad connection currently would surface as a raw 500).
4. No tests for `backend/` (FastAPI routes) or `frontend/` — only the ETL layer is tested.
5. Frontend has no loading/empty-state polish beyond a single "Loading…" text and a generic error message.
6. The project isn't in git yet — worth setting up version control to track future learning increments.
