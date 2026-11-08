from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR





class Roles(Base):
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    role: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    def __repr__(self):
        return f'Roles(role_id={self.role_id!r}, role={self.role!r}, department={self.department!r})'
