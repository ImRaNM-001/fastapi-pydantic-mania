from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import List, Dict

app: FastAPI = FastAPI()

class AccountTransaction(BaseModel):
    account_id: int
    account_type: str
    amount_transacted: int
    origin: str | None = None       
    # NOTE: Added type annotation
    # str | None is the modern way to say "Optional string".

    destination: str | None = None       

transactions: List[AccountTransaction] = []

@app.get('/')
def view_home() -> Dict[str, str]:
    return {
        'message': 'Account transaction landing page'
    }

@app.get('/transactions')
def get_transactions() -> List[AccountTransaction]:
    return transactions


@app.post('/transactions')
def add_transaction(new_transaction: AccountTransaction) -> AccountTransaction:
    transactions.append(new_transaction)       # insert a fresh transaction to the empty List
    return new_transaction


@app.put('/transactions/{acc_id}')
def update_transaction(acc_id: int,
                       updated_transaction: AccountTransaction) -> AccountTransaction:
    
    for index, val in enumerate(transactions):
        if val.account_id == acc_id:
            transactions[index] = updated_transaction
            return updated_transaction
            
    # If no matching account_id found, raise 404
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Transaction with account_id {acc_id} not found')


@app.delete('/transactions/{acc_id}')
def delete_transaction(acc_id: int) -> Response:
    for index, val in enumerate(transactions):
        if val.account_id == acc_id:
            transactions.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
 
     # If no matching account_id found, raise 404
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Transaction with account_id {acc_id} not found')


# return 200 OK (default) with the 'acc_id' if 'acc_id' is needed to be returned
"""
@app.delete('/transactions/{acc_id}')
def delete_transaction(acc_id: int) -> Dict[str, str]:
    for index, val in enumerate(transactions):
        if val.account_id == acc_id:
            transactions.pop(index)
            return {
                'deleted_id': acc_id, 
                'message': 'Transaction deleted'
            }
            
    raise HTTPException(status_code=404, detail=f'Transaction {acc_id} not found')
"""


# uvicorn 09-FastAPI_topics.9-0-crashing_api_routes:app --reload

