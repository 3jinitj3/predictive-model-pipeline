from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, String, ARRAY, Integer, Interval, ForeignKey, func
from app.db.base import Base
from app.db.models.users import Users
from app.db.models.roles import Roles


class Logins(Base):
    __tablename__ = 'logins'
    __table_args__ = {'extend_existing': True}

    login_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False, init=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.role_id'), nullable=True, init=False)
    session_start: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, init=False, server_default=func.now())
    session_end: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, init=False)
    duration: Mapped[Interval| None] = mapped_column(Interval, nullable=True, init=False)
    activity: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True, init=False) # This could be a json file or dictionay do research 

    def __repr__(self) -> str:
        return f'Logins(login_in={self.login_id!r}, user_id={self.user_id!r}, username={self.role_id!r}, session_start={self.session_start!r}, \
                        session_end={self.session_end!r}, duration={self.duration!r}, activitiy={self.activity!r})'

