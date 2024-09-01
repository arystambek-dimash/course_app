from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel


class _BaseTopicSchema(BaseModel):
    name: str
    description: Optional[str]
    order: int


class TopicInCreate(_BaseTopicSchema):
    pass


class TopicInUpdate(_BaseTopicSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None


class TopicBase(_BaseTopicSchema):
    id: int
    created_at: datetime


class TopicDetailResponse(TopicBase):
    tests: list

    class Config:
        from_attributes = True
