from dataclasses import dataclass
from typing import Dict, List, Optional

from bacpypes3.pdu import Address
from bacpypes3.primitivedata import ObjectType
from bacpypes3.basetypes import PropertyIdentifier

# from unit_conversion import Conversion  # Your custom unit conversion class


# Define a single BACnet point
@dataclass
class Point:
    name: str
    object_type: ObjectType
    object_num: int
    property: PropertyIdentifier = PropertyIdentifier.presentValue
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    # conversion: Optional[Conversion] = None


@dataclass
class Template:
    name: str
    points: List[Point]


@dataclass
class PollingConfig:
    name: str
    pollRate: int  # seconds
    address: Address
    templates: List[Template]


# Example configuration for a single device
defined_templates = {
    "pm_6A_crah5": Template(
        name="PM 6A Datahall CRAH5 ALARMS",
        points=[
            Point(
                name="infra_pm6a_crah5_smoke_alarm",
                object_type=ObjectType.binaryInput,
                object_num=2,
                description="6A Datahall CRAH5 smoke alarm. Siemens point TESLA.B6A.CRAH5.SD",
            ),
            Point(
                name="infra_pm6a_crah5_failure",
                object_type=ObjectType.binaryValue,
                object_num=19,
                description="6A Datahall CRAH5 failure. Siemens point TESLA.B6A.CRAH4.SF.FLT.ALM",
            ),
        ]
    )
}

device_configs: Dict[str, List[PollingConfig]] = {
    "192.168.62.20": [
        PollingConfig(
            name="Sergei' Laptop",
            pollRate=30,
            address=Address("192.168.62.20"),  # Replace with actual device IP
            templates=[
                defined_templates["pm_6A_crah5"]
            ]
        )
    ]
}