import httpx
import os
import json

DATACORE_URL = os.getenv("DATACORE_URL", "http://localhost:4000")

class DataCoreClient:
    async def ingest_clinical_data(self, record_id: str, payload: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DATACORE_URL}/api/data/ingest",
                    json={"schema": "financial_audit_record", "id": record_id, "payload": payload}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"[DataCore] Ingestion failed: {e}")
            raise e
