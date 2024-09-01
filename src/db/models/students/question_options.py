import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class QuestionOptionsOrm(Base):
    __tablename__ = "student_question_options"

    id: Mapped[int] = mapped_column(sa.INTEGER, primary_key=True)
    text: Mapped[str] = mapped_column(sa.TEXT, nullable=False)
    is_correct: Mapped[bool] = mapped_column(sa.BOOLEAN, nullable=False)

    question_id: Mapped[int] = mapped_column(sa.INTEGER, sa.ForeignKey("student_test_questions.id", ondelete="CASCADE"))

    question = relationship('QuestionsOrm', back_populates="options", uselist=False)
