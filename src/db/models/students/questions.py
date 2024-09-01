from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.database import Base


class QuestionsOrm(Base):
    __tablename__ = 'student_test_questions'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    text: Mapped[str] = mapped_column(sa.TEXT, name='question_text', nullable=False)
    image: Mapped[str] = mapped_column(sa.String, name='question_image', nullable=True)
    question_type: Mapped[str] = mapped_column(sa.String, default='single')
    explanation: Mapped[str] = mapped_column(sa.TEXT, nullable=True)
    explanation_image: Mapped[str] = mapped_column(sa.String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    test_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('student_topic_tests.id', ondelete='CASCADE'))

    test = relationship('TestsOrm', back_populates='questions')
    options = relationship('QuestionOptionsOrm', back_populates='question', cascade='all, delete-orphan')
