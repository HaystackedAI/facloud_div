from datetime import datetime
import json
from .azure_data_lake import get_file_system_client
import asyncio

fs_client = get_file_system_client()

class DataLakeLogger:
    def __init__(self, folder="logs", flush_every=5):
        self.folder = folder
        self.buffer = []
        self.flush_every = flush_every  # flush after N events
        self.lock = asyncio.Lock()      # async-safe

    async def log_event(self, event_type: str, payload: dict):
        """Add a log to the buffer"""
        async with self.lock:
            log_entry = {
                "type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "payload": payload
            }
            self.buffer.append(log_entry)
            if len(self.buffer) >= self.flush_every:
                await self.flush()

    async def flush(self):
        """Write all buffered logs to Data Lake"""
        async with self.lock:
            if not self.buffer:
                return None

            file_name = f"{self.folder}/{datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')}.json"
            file_client = fs_client.get_file_client(file_name)

            content = json.dumps(self.buffer)
            file_client.create_file()
            file_client.append_data(content.encode("utf-8"), offset=0, length=len(content))
            file_client.flush_data(len(content))

            self.buffer = []
            return file_name
