import uuid

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from typing import Literal, Optional
from typing_extensions import Annotated

PositiveFloat = Annotated[float, Field(gt=0)]

app = FastAPI()


class TransactionInfo(BaseModel):
    transaction_date: datetime
    liters_purchased: PositiveFloat
    price: PositiveFloat
    gas_type: Literal["DT", "92", "98", "100"]


class UpdateTransactionInfo(BaseModel):
    transaction_date: Optional[datetime] = None
    liters_purchased: Optional[PositiveFloat] = None
    price: Optional[PositiveFloat] = None
    gas_type: Optional[Literal["DT", "92", "98", "100"]] = None


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
async def update_transaction(transaction_id: uuid.UUID, updated_transaction: UpdateTransactionInfo):
    transaction_index = next((i for i, t in enumerate(transactions_db) if t.transaction_id == transaction_id), None)
    if transaction_index is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if updated_transaction.transaction_date is not None:
        transactions_db[transaction_index].transaction_info.transaction_date = updated_transaction.transaction_date
    if updated_transaction.liters_purchased is not None:
        transactions_db[transaction_index].transaction_info.liters_purchased = updated_transaction.liters_purchased
    if updated_transaction.price is not None:
        transactions_db[transaction_index].transaction_info.price = updated_transaction.price
    if updated_transaction.gas_type is not None:
        transactions_db[transaction_index].transaction_info.gas_type = updated_transaction.gas_type
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
