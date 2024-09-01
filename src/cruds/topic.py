from sqlalchemy import select, insert, update, delete

import src.db.schemas.students.topics as topic_schema
from src.constants.enums import Status
from src.db.database import async_session
from src.db.models.students.topics import TopicsOrm


class TopicCRUD:
    @staticmethod
    async def get_topic_by_id(topic_id: int) -> topic_schema.TopicBase | None:
        async with async_session() as session:
            query = select(TopicsOrm).where(TopicsOrm.id == topic_id)
            result = await session.execute(query)
            topic = result.scalar_one_or_none()  # Use scalar_one_or_none() to handle cases where no result is found
        return topic_schema.TopicBase.from_orm(topic) if topic else None

    @staticmethod
    async def create_topic(topic: topic_schema.TopicInCreate) -> topic_schema.TopicBase:
        try:
            async with async_session() as session:
                query = insert(TopicsOrm).values(**topic.dict())
                result = await session.execute(query)
                await session.commit()
                created_topic = result.inserted_primary_key
                created_topic_data = await session.get(TopicsOrm, created_topic[0])
            return topic_schema.TopicBase.from_orm(created_topic_data)
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def update_topic(topic_id: int, topic: topic_schema.TopicInUpdate) -> topic_schema.TopicBase:
        try:
            async with async_session() as session:
                query = (
                    update(TopicsOrm)
                    .where(TopicsOrm.id == topic_id)
                    .values(**topic.dict(exclude_none=True))
                    .returning(TopicsOrm)
                )
                result = await session.execute(query)
                await session.commit()
                updated_topic = result.scalar_one_or_none()  # Fetch the updated topic
            return topic_schema.TopicBase.from_orm(updated_topic) if updated_topic else None
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def delete_topic(topic_id: int) -> Status:
        try:
            async with async_session() as session:
                query = delete(TopicsOrm).where(TopicsOrm.id == topic_id)
                result = await session.execute(query)
                await session.commit()

                if result.rowcount == 0:
                    raise ValueError(f"Topic with id {topic_id} does not exist")

                return Status.DELETED
        except Exception as e:
            await session.rollback()
            raise e
