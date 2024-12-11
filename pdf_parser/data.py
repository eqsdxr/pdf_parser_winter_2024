from dataclasses import dataclass
from datetime import datetime


@dataclass
class LotData:
    """Class for storing lot data"""
    lot: str
    lot_name: str
    customer_name: str
    customer_address: str
    planned_unit_price: int
    planned_total_price: int
    measurment_unit: str
    amount: int


@dataclass
class DeniedSuppliersTable:
    """Class for storing denied suppliers"""
    serial_number: int
    supplier_name: str
    bin_iin_unp: int
    reason_for_deviation: str


@dataclass
class WonAndPotentialSuppliersTable:
    """Class for storing third table with one winner and potential suppliers"""
    serial_number: int
    supplier_name: str
    unit_price: int
    total_price: int
    date_time: datetime
