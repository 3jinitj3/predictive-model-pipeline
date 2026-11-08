from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, String, TEXT,  Date, Integer, BOOLEAN, ForeignKey, func
from app.db.base import Base




class AuthEvents(Base):
    __tablename__ = 'auth_events'

    event_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True)
    event_type: Mapped[bool] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)


    def __repr__(self) -> str:
        return f'AuthEvents(event_id={self.event_id!r}, user_id={self.user_id!r}, event_type={self.event_type!r}, created_at={self.created_at!r},ip_address={self.ip_address!r})'