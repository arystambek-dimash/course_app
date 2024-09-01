import sqlalchemy as sa
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.db.database import Base


class TopicsOrm(Base):
    __tablename__ = 'student_topics'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(sa.Text, nullable=True, comment="Detailed description of the topic")
    order: Mapped[int] = mapped_column(sa.Integer, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, comment="Topic created at date")

    tests = relationship(
        'TestsOrm',
        back_populates='topic',
        uselist=True,
        cascade='all, delete-orphan',
        passive_deletes=True)
    user_statuses = relationship(
        'UserTopicStatusesOrm',
        back_populates='topic',
        cascade='all, delete-orphan',
        passive_deletes=True)
