import httpx
import os

SAFECORE_URL = os.getenv("SAFECORE_URL", "http://localhost:3000")

class SafeCoreClient:
    async def verify_session(self, token: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{SAFECORE_URL}/health", headers={"Authorization": f"Bearer {token}"})
                if response.status_code == 200:
                    return {"valid": True, "details": response.json()}
                return {"valid": False}
        except Exception as e:
            print(f"[SafeCore] Error verifying session: {e}")
            return {"valid": False, "error": str(e)}

    async def sanitize_input(self, data: dict):
        pass
