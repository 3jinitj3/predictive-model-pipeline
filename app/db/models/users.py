from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, String, VARCHAR, Integer, Date, BOOLEAN, ForeignKey, func
from app.db.base import Base
from app.db.models.roles import Roles



class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    created: Mapped[datetime] = mapped_column(TIMESTAMP, init=False, server_default=func.now())
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.role_id'), nullable=True, init=False)
    first_name: Mapped[str] = mapped_column(VARCHAR(75), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(75), nullable=False)
    birthdate: Mapped[datetime] = mapped_column(Date, nullable=False)
    username: Mapped[str] = mapped_column(VARCHAR(75), unique=True, nullable=False)
    passwd_hash: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)

    def __repr__(self) -> str:
        return f'Users(user_id={self.user_id!r}, created={self.created!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, \
                        birthdate={self.birthdate!r}, username={self.username!r}, passwd_hash={'SECRET'}, email={self.email!r}, is_active={self.is_active!r})'