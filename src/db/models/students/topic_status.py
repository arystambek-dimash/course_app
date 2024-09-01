from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from src.db.database import Base


class UserTopicStatusesOrm(Base):
    __tablename__ = 'student_topic_status'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    topic_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('student_topics.id', ondelete='CASCADE'))
    completed: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)

    user = relationship('UsersOrm', back_populates='topic_statuses')
    topic = relationship('TopicsOrm', back_populates='user_statuses')
