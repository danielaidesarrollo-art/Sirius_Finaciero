from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import os
import sys
from datetime import datetime

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the project root to sys.path to find bundled 'shared'
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from shared.verification import SiriusVerification

app = FastAPI(title="Sirius_Financial Core", version="1.0.0")

class AuditRequest(BaseModel):
    signature: str
    action: str

@app.post("/audit/verify")
def verify_action(request: AuditRequest):
    """
    Rector Level Audit: Banking & Security Verification.
    """
    # 1. Signature Check
    is_valid_sig = False
    if "ROLLBACK" in request.action:
        is_valid_sig = SiriusVerification.verify_global_admin(request.signature)
    else:
        is_valid_sig = SiriusVerification.verify_level_10(request.signature)
    
    if not is_valid_sig:
        raise HTTPException(status_code=403, detail="Sirius Rector Financial: Unauthorized Signature")

    # 2. Banking Compliance Check (AML/KYC Simulation)
    if "FINANCIAL" in request.action:
        print(f"[SIRIUS-FIN] Auditing financial transaction: {request.action}")
        if "SUSPICIOUS_ACT" in request.action:
             raise HTTPException(status_code=451, detail="BANKING REJECTED: Suspicious activity detected (AML violation).")
    
    return {
        "status": "AUTHORIZED", 
        "auditor": CORE_NAME, 
        "compliance": "BANKING-PASSED",
        "timestamp": datetime.utcnow().isoformat()
    }

# Directive 3: Identity
CORE_NAME = "Sirius_Financial"

@app.get("/api/compliance")
async def compliance():
    validator = ComplianceValidator()
    return {**validator.validate(), "system_state": "NORMAL", "timestamp": datetime.now().isoformat()}

@app.get("/")
def root():
    return {"status": "Running", "core": CORE_NAME}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def get_metrics():
    return {
        "core": CORE_NAME,
        "uptime": time.process_time(),
        "status": "HEALTHY",
        "cpu_load": "NORMAL"
    }

@app.get("/handshake")
def handshake():
    return {
        "status": "DataCore Level 10/10",
        "node": CORE_NAME,
        "secured": True,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)