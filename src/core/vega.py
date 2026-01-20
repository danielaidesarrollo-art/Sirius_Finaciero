import pandas as pd
import os
from datetime import datetime
import json
import time
from typing import List, Dict, Any, Optional
from src.security.financial_security import FinancialSecurity

class VegaFinancial:
    """
    DataCore Vega adapted for the Financial Division.
    Manages a unified Ledger for Farming, Lending, RWA, and Trading.
    Supports secure export to CSV and XLSX.
    """
    def __init__(self, storage_path: str = "data"):
        self.storage_path = storage_path
        self.ledger_file = os.path.join(storage_path, "unified_ledger.json")
        self.security = FinancialSecurity()
        self.connection_string = os.getenv("SUPABASE_URL", "mock://supabase.daniel-ai.internal") # Added for Supabase compatibility
        
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
        if not os.path.exists(self.ledger_file):
            self._save_ledger([])
            
        # Cache for get_summary
        self.summary_cache = {
            "timestamp": 0,
            "data": None,
            "ttl": 60 # seconds
        }

    def _load_ledger(self) -> List[Dict[str, Any]]:
        with open(self.ledger_file, 'r') as f:
            return json.load(f)

    def _save_ledger(self, data: List[Dict[str, Any]]):
        with open(self.ledger_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_transaction(self, module: str, amount: float, currency: str, description: str, metadata: Dict[str, Any] = None):
        """Adds a secure transaction to the unified ledger."""
        ledger = self._load_ledger()
        
        transaction = {
            "transaction_id": self.security.hash_id(f"{datetime.now().isoformat()}-{amount}"),
            "timestamp": datetime.now().isoformat(),
            "module": module, # Farming, Lending, RWA, Trading
            "amount": amount,
            "currency": currency,
            "description": description,
            "status": "COMPLETED",
            "metadata": metadata or {}
        }
        
        ledger.append(transaction)
        self._save_ledger(ledger)
        
        return transaction

    def export_ledger(self, format: str = "csv") -> str:
        """Exports the ledger to CSV or XLSX format."""
        ledger = self._load_ledger()
        df = pd.DataFrame(ledger)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ledger_export_{timestamp}.{format}"
        file_path = os.path.join(self.storage_path, filename)
        
        if format.lower() == "csv":
            df.to_csv(file_path, index=False)
        elif format.lower() == "xlsx":
            df.to_excel(file_path, index=False)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'xlsx'.")
            
        return file_path

    def get_summary(self) -> Dict[str, Any]:
        """Returns a financial summary across all modules. Cached for 60s."""
        current_time = time.time()
        if self.summary_cache["data"] and (current_time - self.summary_cache["timestamp"] < self.summary_cache["ttl"]):
            return self.summary_cache["data"]

        ledger = self._load_ledger()
        if not ledger:
            result = {"total_volume": 0, "module_breakdown": {}}
        else:
            df = pd.DataFrame(ledger)
            result = {
                "total_volume": float(df['amount'].sum()), # Ensure native float for JSON serialization
                "module_breakdown": df.groupby('module')['amount'].sum().to_dict(),
                "transaction_count": len(df)
            }
        
        self.summary_cache["data"] = result
        self.summary_cache["timestamp"] = current_time
        return result
