import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Operations Dashboard", layout="wide")


@st.cache_data
def load_data():
    conn = sqlite3.connect("sales_warehouse.db")
    df = pd.read_sql("SELECT * FROM clean_sales", conn)
    conn.close()
    return df


st.title("📊 Enterprise Sales & Operations Dashboard")
st.markdown("Automated data pipeline ingestion with real-time KPI metrics.")

try:
    df = load_data()

    col1, col2, col3, col4 = st.columns(4)
    completed_sales = df[df["status"] == "Completed"]

    total_revenue = completed_sales["amount"].sum()
    total_orders = len(df)
    avg_order_value = completed_sales["amount"].mean() if not completed_sales.empty else 0
    unique_customers = df["customer_id"].nunique()

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Records Ingested", total_orders)
    col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    col4.metric("Active Customers", unique_customers)

    st.divider()

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Revenue by Category")
        category_rev = completed_sales.groupby("product_category")["amount"].sum().reset_index()
        fig_cat = px.bar(
            category_rev,
            x="product_category",
            y="amount",
            color="product_category",
            title="Total Revenue per Product Line",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with chart_col2:
        st.subheader("Monthly Revenue Run Rate")
        monthly_rev = completed_sales.groupby("year_month")["amount"].sum().reset_index()
        fig_trend = px.line(
            monthly_rev,
            x="year_month",
            y="amount",
            markers=True,
            title="Monthly Sales Trend",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Validated Records (SQLite Warehouse)")
    st.dataframe(df, use_container_width=True)

except Exception:
    st.warning("No database found. Run `python -m src.pipeline` first to ingest data.")