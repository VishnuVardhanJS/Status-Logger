import asyncio
import importlib
import yaml
from logger.logger import get_logger

logging = get_logger("Root")

async def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    services = []

    for service in config["services"]:
        try:
            module_name = service["module"]
            module = importlib.import_module(module_name)
            service_class = getattr(module, "Service")

            service_instance = service_class(service)
            services.append(service_instance)
        except Exception as e:
            logging.critical("Service %s Configured Properly", service.get("name", ""))

    await asyncio.gather(*(s.run() for s in services))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logging.info("All Services Stopped!")
