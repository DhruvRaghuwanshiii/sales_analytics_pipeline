# Enterprise Sales & Operations Analytics Pipeline

A modular Python data pipeline that cleanses raw operational records, enforces strict schema contracts via Pydantic, isolates malformed rows into an audit quarantine, loads clean tables into SQLite, and displays executive KPIs via an interactive Streamlit dashboard.

## Key Features
- **Data Contracts & Validation:** Enforces data types, positive values, and valid status categories using Pydantic.
- **Automated Quarantine:** Automatically routes corrupted records to `data/quarantine_records.csv` without failing downstream pipelines.
- **Vectorized Transformation:** Uses Pandas for deduplication, unit-price calculation, and monthly revenue aggregations.
- **Relational Persistence:** Automatically writes and updates an indexed SQLite warehouse (`sales_warehouse.db`).
- **Interactive Dashboard:** Real-time KPI summary cards and dynamic Plotly charts built with Streamlit.
- **Automated Testing:** Test coverage implemented with Pytest.

## Tech Stack
- **Language:** Python 3.10+
- **Data Processing:** Pandas, NumPy
- **Validation:** Pydantic
- **Database:** SQLite
- **Visualization:** Streamlit, Plotly
- **Testing:** Pytest

## Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/sales_analytics_pipeline.git
   cd sales_analytics_pipeline
   