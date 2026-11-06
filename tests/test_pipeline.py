import pandas as pd
import pytest
from src.pipeline import SalesETLPipeline


def test_pipeline_validation_and_quarantine(tmp_path):
    test_csv = tmp_path / "test_sales.csv"
    test_csv.write_text(
        "transaction_id,customer_id,date,product_category,amount,quantity,status\n"
        "TXN-01,CUST-01,2024-01-01,Tech,100.0,1,Completed\n"
        "TXN-02,CUST-02,2024-01-01,Tech,-50.0,1,Completed\n"
    )

    test_db = tmp_path / "test.db"
    pipeline = SalesETLPipeline(db_path=str(test_db))
    clean_df, quarantine_df = pipeline.run_pipeline(str(test_csv))

    assert len(clean_df) == 1
    assert clean_df.iloc[0]["transaction_id"] == "TXN-01"
    assert len(quarantine_df) == 1
    assert quarantine_df.iloc[0]["transaction_id"] == "TXN-02"