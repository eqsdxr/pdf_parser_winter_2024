from dataclasses import dataclass
from datetime import datetime


@dataclass
class LotDataTable:
    """Class for storing lot data"""
    lot_number: str = None
    lot_name: str = None
    customer_name: str = None
    customer_address: str = None
    planned_unit_price: int = None
    planned_total_price: int = None
    measurment_unit: str = None
    amount: int = None

@dataclass
class DeniedSuppliersRow:
    """Class for storing denied suppliers"""
    serial_number: int
    supplier_name: str
    bin_iin_unp: int
    reason_for_deviation: str

@dataclass
class ResultsRow:
    """Class for storing a rows with one winner and potential suppliers"""
    serial_number: int
    supplier_name: str
    bin_iin_inn_unp: int
    unit_price: int
    total_price: int
    date_time: datetime

@dataclass
class ThreeTablesLDR:
    """Class for storing a unit of three tables (lot, denied, results)"""
    lot_data_table: LotDataTable
    denied_suppliers_table: list[DeniedSuppliersRow]
    results_table: list[ResultsRow]
