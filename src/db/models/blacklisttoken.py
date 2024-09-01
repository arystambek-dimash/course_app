import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class BlacklistToken(Base):
    __tablename__ = 'blacklisttoken'
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
