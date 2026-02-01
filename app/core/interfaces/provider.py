from abc import ABC, abstractmethod
from typing import Dict, Any

class WhatsAppProvider(ABC):
    @abstractmethod
    async def send_message(self, to: str, content: str, msg_type: str = "text") -> Dict[str, Any]:
        """Send a message to the provider."""
        pass

    @abstractmethod
    def verify_webhook_token(self, token: str) -> bool:
        """Verify the webhook verification token."""
        pass

    @abstractmethod
    def validate_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Validate the webhook signature (HMAC)."""
        pass
