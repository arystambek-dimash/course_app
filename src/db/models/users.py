import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.db.database import Base


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    profile_image: Mapped[str] = mapped_column(sa.String, default=None, nullable=True)
    telephone_number: Mapped[str] = mapped_column(sa.String(length=15), unique=True, index=True, nullable=False,
                                                  comment="User telephone number")
    password: Mapped[str] = mapped_column(sa.String(length=128), nullable=False, comment="User password (hashed)")
    first_name: Mapped[str] = mapped_column(sa.String(length=50), nullable=False, comment="User first name")
    last_name: Mapped[str] = mapped_column(sa.String(length=50), nullable=False, comment="User last name")
    telephone_verified: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False,
                                                     comment="Telephone verify status")
    role: Mapped[str] = mapped_column(sa.String(length=20), nullable=False, comment="User role")

    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, nullable=False,
                                                 comment="User created at date")
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False, comment="User updated at date")

    test_attempts = relationship("AttemptsOrm", back_populates="user", cascade="all, delete-orphan")
    topic_statuses = relationship("UserTopicStatusesOrm", back_populates="user", cascade="all, delete-orphan")
    test_statuses = relationship("UserTestStatusesOrm", back_populates="user", cascade="all, delete-orphan")
