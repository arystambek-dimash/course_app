from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class AttemptsOrm(Base):
    __tablename__ = "student_test_attempts"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("student_topic_tests.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
    score: Mapped[int] = mapped_column(sa.Integer, default=0, comment='User points on each test')
    start_time: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    user = relationship('UsersOrm', back_populates="test_attempts", uselist=False)
    test = relationship('TestsOrm', back_populates='test_attempts')
