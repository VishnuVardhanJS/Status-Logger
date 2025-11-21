from base_service.base_service import BasePollingService
import requests

from logger.logger import get_logger

class Service(BasePollingService):
    def __init__(self, service):
        self.name = service.get("name", "Unknown Service")
        self.poll_interval = service.get("poll_interval", 60)
        self.poll_interval_during_outage = service.get(
            "poll_interval_during_outage", 15
        )

        self.logging = get_logger(self.name)
        self.logging.info("Service %s Started!", self.name)

        self.components_endpoint = service.get("components_endpoint")
        self.incidents_endpoint = service.get("incidents_endpoint")
        self.status_endpoint = service.get("status_endpoint")

    def check_components_health(self):
        try:
            status_res = requests.get(self.status_endpoint).json()

            if status_res["status"]["indicator"] == "none":
                return "operational"

            components_res = requests.get(self.components_endpoint).json()

            for product in components_res["components"]:
                if product["status"] != "operational":
                    self.logging.warning("Product: %s - %s", self.name, product["name"])
        except Exception as e:
            self.logging.error("StatusPage Error for %s", self.name)

        return "service_outage"

    def check_incidents(self):
        try:
            incidents_res = requests.get(self.incidents_endpoint).json()

            for incident in incidents_res["incidents"]:
                if incident["status"] != "resolved":
                    self.logging.error("Status: %s - %s", self.name, incident["name"])
        except Exception as e:
            self.logging.error("StatusPage Error for %s", self.name)

        return "service_outage"

    async def poll(self):
        components_health = self.check_components_health()

        if components_health == "operational":
            return components_health
        else:
            return self.check_incidents()



