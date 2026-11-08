from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String



class Permissions(Base):
    __tablename__ = 'permissions'

    permission_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    permission: Mapped[str] = mapped_column(String(75), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'Permissions(permission_id={self.permission_id!r}, permission={self.permission!r}, description={self.description!r})'