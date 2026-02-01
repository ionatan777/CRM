from abc import ABC, abstractmethod

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, filename: str, content: bytes) -> str:
        """Save content to storage and return the path/identifier."""
        pass

    @abstractmethod
    def get_file(self, path: str) -> bytes:
        """Retrieve content from storage."""
        pass
