import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

app = FastAPI()


class TransactionInfo(BaseModel):
    transaction_date: datetime
    liters_purchased: float
    price: float
    gas_type: Literal["DT", "92", "98", "100"]


class GasStationTransaction(BaseModel):
    transaction_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    transaction_info: TransactionInfo


transactions_db: list[GasStationTransaction] = []


@app.post("/transaction/create")
async def create_transaction(transaction_info: TransactionInfo):
    # Generate a UUID for the transaction
    transaction = GasStationTransaction(
        transaction_info=transaction_info
    )
    transactions_db.append(transaction)
    return transaction.transaction_id


@app.put("/transaction/update/{transaction_id}")
async def update_transaction(transaction_id: uuid.UUID, updated_transaction: TransactionInfo):
    transaction_index = next((i for i, t in enumerate(transactions_db) if t.transaction_id == transaction_id), None)
    if transaction_index is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    transactions_db[transaction_index] = updated_transaction
    return {"message": f"Transaction {transaction_id} updated successfully"}


@app.delete("/transaction/delete/{transaction_id}")
async def delete_transaction(transaction_id: uuid.UUID):
    transaction_index = next((i for i, t in enumerate(transactions_db) if t.transaction_id == transaction_id), None)
    if transaction_index is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    del transactions_db[transaction_index]
    return {"message": f"Transaction {transaction_id} deleted successfully"}


@app.get("/transaction/read/{transaction_id}")
async def read_transaction(transaction_id: uuid.UUID):
    transaction = next((t for t in transactions_db if t.transaction_id == transaction_id), None)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.transaction_info


@app.get("/transaction/read_all")
async def read_all_transactions():
    return transactions_db
