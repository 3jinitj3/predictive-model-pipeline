from app.db.base import Base
from sqlalchemy import Integer, String, ForeignKey, Date, Numeric, Boolean, VARCHAR
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.schemas.orders import SalesOrderStatus




class SalesOrderHeaders(Base):
    __tablename__ = 'sales_order_headers'

    sales_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    buyer_name: Mapped[int] = mapped_column(VARCHAR(150), nullable=False)
    sales_date: Mapped[datetime] = mapped_column(Date, nullable=False, init=False)
    gross_total: Mapped[float] = mapped_column(Numeric(percision=8, scale=2))
    tax_rate: Mapped[float] = mapped_column(Numeric(percision=8, scale=2))
    tax_amount: Mapped[float] = mapped_column(Numeric(percision=8, scale=2))
    total: Mapped[float] = mapped_column(Numeric(percision=8, scale=2), init=True)
    due_date: Mapped[datetime] = mapped_column(Date, nullable=False, init=True)
    status: Mapped[bool] = mapped_column(SQLEnum(SalesOrderStatus, name='order_status'), nullable=False, default=OrderStatus.PENDING, init=False)

    def __repr__(self):
        return f'SalesOrders(sales_id={self.sales_id!r}, line_item={self.line_item!r}, service_id={self.service_id!r}, org_id={self.org_id!r}, user_id={self.user_id!r}, buyer_name={self.buyer_name!r}, sales_date={self.due_date!r}, price={self.price!r}, due_date={self.due_date!r}, status={self.status!r})'


class SalesOrderLines(Base):
    __tablename__ = 'sales_order_lines'

    sales_id: Mapped[int] = mapped_column(Integer, ForeignKey('sales_order_headers.sales_id'), primary_key=True)
    line_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.service_id'), init=True)
    service: Mapped[int] = mapped_column(String, ForeignKey('services.service'), init=True)
    description: Mapped[str] = mapped_column(String, ForeignKey('services.description'), init=True)
    price: Mapped[float] = mapped_column(Numeric(8, scale=2), init=True)