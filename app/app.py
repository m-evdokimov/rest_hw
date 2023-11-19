import uuid

from fastapi import FastAPI, HTTPException

from schemes import GasStationTransaction, TransactionInfo, UpdateTransactionInfo


app = FastAPI()
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
