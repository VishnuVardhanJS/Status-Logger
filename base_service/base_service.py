import asyncio
from logger.logger import get_logger


class BasePollingService:
    def __init__(self, name, poll_interval=60, poll_interval_during_outage=15):
        self.name = name
        self.poll_interval = poll_interval
        self.poll_interval_during_outage = poll_interval_during_outage
        self.logging = get_logger("Root")

    async def poll(self):
        """Override in each service class with custom logic"""
        raise NotImplementedError

    async def run(self):
        while True:
            try:
                results = await self.poll()
            except Exception as e:
                print(f"[{self.name}] Polling error: {e}")

            if results != "operational":
                await asyncio.sleep(self.poll_interval_during_outage)
            else:
                self.logging.info("%s has No incidents!", self.name)
                await asyncio.sleep(self.poll_interval)
