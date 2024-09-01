from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.database import Base


class TestsOrm(Base):
    __tablename__ = 'student_topic_tests'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, index=True)
    avg_score: Mapped[float] = mapped_column(sa.Float, nullable=False)
    order: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, comment="Test created at date")
    topic_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('student_topics.id', ondelete='CASCADE'))

    topic = relationship('TopicsOrm', back_populates='tests')
    questions = relationship(
        'QuestionsOrm',
        back_populates='test',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    user_statuses = relationship(
        'UserTestStatusesOrm',
        back_populates='test',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    test_attempts = relationship(
        "AttemptsOrm",
        back_populates='test',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
