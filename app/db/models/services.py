from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric
from app.db.base import Base


class Services(Base):

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoimcrement=True, nullable=True, init=False)
    service: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(percision=8, scale=2), nullable=False)

    def __repr__(self):
        return f'Services(service_id={self.service_id!r}, service={self.service!r}, description={self.description!r}, price={self.price!r})'



