from dataclasses import dataclass
import os
import re
import time
from typing import Dict, List

from prometheus_client import start_http_server, Gauge
from exporters.bacnet.polling_templates import device_configs, PollingConfig
 # Adjust path as needed

# Define device structure
@dataclass
class Device:
    name: str
    ip_address: str

PROM_PORT = 9531

# Clean device name for use in Prometheus labels
def clean_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^\w]", "_", name)
    return name

# Ping function: returns 1 if host responds, 0 otherwise
def ping(ip_address: str) -> int:
    response = os.system(f"ping -c 1 {ip_address} > /dev/null 2>&1")
    return int(response == 0) # 0 = success -> 1; non-zero = fail -> 0

if __name__ == "__main__":
    devices: List[Device] = []
    start_http_server(PROM_PORT)

    # Build device list from config
    for config_list in device_configs.values():
        config: PollingConfig = config_list[0]
        name = clean_name(config.name)
        devices.append(Device(name, config.address))

    # Define Prometheus metric
    gauge = Gauge(
        "infra_heartbeat",
        "Heartbeat between service node and end device",
        ["device_name", "ip"]
    )

    # Monitoring loop
    while True:
        for device in devices:
            status = ping(device.ip_address)
            gauge.labels(device_name=device.name, ip=device.ip_address).set(status)
        time.sleep(20)