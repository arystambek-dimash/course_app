from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from src.db.database import Base


class UserTestStatusesOrm(Base):
    __tablename__ = 'topic_test_status'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    test_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('student_topic_tests.id', ondelete="CASCADE"))
    completed: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    max_earned_score: Mapped[float] = mapped_column(sa.Float, nullable=True)

    user = relationship('UsersOrm', back_populates='test_statuses')
    test = relationship('TestsOrm', back_populates='user_statuses')
