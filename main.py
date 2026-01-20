from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.vega import VegaFinancial
from typing import Dict, Any, Optional

app = FastAPI(title="Vega Financial", version="1.0.0")
core = VegaFinancial()

class TransactionRequest(BaseModel):
    module: str
    amount: float
    currency: str
    description: str
    metadata: Optional[Dict[str, Any]] = {}

@app.post("/transaction")
async def add_tx(req: TransactionRequest):
    return core.add_transaction(req.module, req.amount, req.currency, req.description, req.metadata)

@app.get("/summary")
async def summary():
    return core.get_summary()

@app.get("/health")
async def health():
    return {"status": "ok", "core": "Vega_Financiero"}
