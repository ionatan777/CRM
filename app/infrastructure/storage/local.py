import os
from app.core.interfaces.storage import StorageProvider

class LocalStorageProvider(StorageProvider):
    def __init__(self, upload_dir: str = "backups"):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def save_file(self, filename: str, content: bytes) -> str:
        file_path = os.path.join(self.upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

    def get_file(self, path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()
