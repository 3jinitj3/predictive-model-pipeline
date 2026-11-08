from app.db.base import Base
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime



class Organizaitons(Base):
    __tablename__ = 'organization'

    org_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    org_name: Mapped[str] = mapped_column(String, nullable=False)
    industry: Mapped[str] = mapped_column(String, nullable=False)
    street_address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    num_employees: Mapped[int] = mapped_column(Integer, nullable=False)
    owner: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f'Organization(org_id={self.org_id!r}, created_at={self.created_at!r}, org_name={self.org_name!r}, industry={self.industry!r}, street_address={self.street_address!r}, city={self.city!r}, state={self.state!r}, num_employees={self.num_employees!r}, owner={self.owner!r})'