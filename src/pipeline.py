import sqlite3
from typing import Tuple
import pandas as pd
from src.schema import TransactionRecord


class SalesETLPipeline:
    def __init__(self, db_path: str = "sales_warehouse.db"):
        self.db_path = db_path

    def run_pipeline(self, raw_csv_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = pd.read_csv(raw_csv_path)

        # 1. Deduplication
        df = df.drop_duplicates(subset=["transaction_id"])

        valid_records = []
        quarantine_records = []

        # 2. Schema validation via Pydantic
        for row in df.to_dict(orient="records"):
            try:
                validated = TransactionRecord(**row)
                valid_records.append(validated.model_dump())
            except Exception as error:
                row["rejection_reason"] = str(error)
                quarantine_records.append(row)

        clean_df = pd.DataFrame(valid_records)
        quarantine_df = pd.DataFrame(quarantine_records)

        # 3. Vectorized transformations with Pandas
        if not clean_df.empty:
            clean_df["date"] = pd.to_datetime(clean_df["date"])
            clean_df["year_month"] = clean_df["date"].dt.to_period("M").astype(str)
            clean_df["unit_price"] = (clean_df["amount"] / clean_df["quantity"]).round(2)
            self._load_to_sqlite(clean_df)

        # 4. Save rejected records
        if not quarantine_df.empty:
            quarantine_df.to_csv("data/quarantine_records.csv", index=False)

        return clean_df, quarantine_df

    def _load_to_sqlite(self, df: pd.DataFrame) -> None:
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql("clean_sales", conn, if_exists="replace", index=False)


if __name__ == "__main__":
    pipeline = SalesETLPipeline()
    clean_data, bad_data = pipeline.run_pipeline("data/raw_sales.csv")
    print("Pipeline execution summary:")
    print(f" - Clean records loaded into SQLite: {len(clean_data)}")
    print(f" - Corrupted records quarantined: {len(bad_data)}")