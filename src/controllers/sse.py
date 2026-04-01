import asyncio

class SSEManager:
    def __init__(self):
        self.listeners: list[asyncio.Queue] = []

    def add_listener(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.listeners.append(queue)
        return queue

    def remove_listener(self, queue: asyncio.Queue):
        self.listeners.remove(queue)

    async def broadcast(self, data: dict) -> int:
        for queue in self.listeners:
            await queue.put(data)
        return len(self.listeners)

sse_manager = SSEManager()