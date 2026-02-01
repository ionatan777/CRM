from app.core.interfaces.provider import WhatsAppProvider
from app.core.config import settings
from typing import Dict, Any
import httpx
import hmac
import hashlib

class MetaProvider(WhatsAppProvider):
    def __init__(self):
        self.api_url = "https://graph.facebook.com/v18.0"
        # In a real app, these would come from settings/env
        self.phone_number_id = "123456789" 
        self.access_token = "TEST_TOKEN" 

    async def send_message(self, to: str, content: str, msg_type: str = "text") -> Dict[str, Any]:
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": msg_type,
        }

        if msg_type == "text":
            payload["text"] = {"body": content}
        
        # For MVP/Dev, we might mock the network call if no real credentials
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(url, headers=headers, json=payload)
        #     response.raise_for_status()
        #     return response.json()
        
        return {"id": "wamid.mock_id", "status": "sent_mock"}

    def verify_webhook_token(self, token: str) -> bool:
        # We need to add verify_token to settings
        # return token == settings.WHATSAPP_VERIFY_TOKEN
        return token == "my_secure_verify_token" # Hardcoded for MVP Phase

    def validate_webhook_signature(self, payload: bytes, signature: str) -> bool:
        # Implementation of HMAC SHA256 validation
        # app_secret = settings.APP_SECRET
        # expected = hmac.new(app_secret.encode(), payload, hashlib.sha256).hexdigest()
        # return hmac.compare_digest(f"sha256={expected}", signature)
        return True # Mock for now
