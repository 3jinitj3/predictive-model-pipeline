from enum import Enum
from pydantic import BaseModel



class SalesOrderStatus(str, Enum):
    PENDING = 'PENDING'
    DISCOVERY = 'DISCOVERY'
    DEVELOPMENT = 'DEVELOPMENT'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'


class SalesLineItems(BaseModel):
    line_number: int
    service_id: int
    service: str
    description: str
    price: float


class SalesReceipt(BaseModel):
    sales_id: int
    items: list[SalesLineItems]
    gross_total: float
    tax_rate: float
    tax_amount: float
    total: float


class SalesTax(float, Enum):
    pass