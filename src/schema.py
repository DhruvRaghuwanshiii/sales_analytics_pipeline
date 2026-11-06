from datetime import date
from pydantic import BaseModel, Field, field_validator


class TransactionRecord(BaseModel):
    transaction_id: str = Field(min_length=3)
    customer_id: str = Field(min_length=1)
    date: date
    product_category: str = Field(min_length=2)
    amount: float = Field(gt=0)
    quantity: int = Field(gt=0)
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        valid_statuses = {"Completed", "Pending", "Cancelled"}
        if value not in valid_statuses:
            raise ValueError(f"Invalid status: {value}. Must be one of {valid_statuses}")
        return value