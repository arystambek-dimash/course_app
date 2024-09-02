from sqlalchemy import select, insert, update, delete

import src.db.schemas.students.topics as topic_schema
from src.constants.enums import Status
from src.db.database import async_session
from src.db.models.students.topics import TopicsOrm


class TopicCRUD:
    @staticmethod
    async def get_topic_by_id(topic_id: int) -> TopicsOrm:
        async with async_session() as session:
            query = select(TopicsOrm).where(TopicsOrm.id == topic_id)
            result = await session.execute(query)
            topic = result.scalar_one_or_none()
        return topic if topic is not None else None

    @staticmethod
    async def get_topic_by_name(topic_name: str) -> TopicsOrm:
        async with async_session() as session:
            query = select(TopicsOrm).where(TopicsOrm.name == topic_name)
            result = await session.execute(query)
            topic = result.scalar_one_or_none()
        return topic if topic else None

    @staticmethod
    async def get_topic_by_order(order: int) -> TopicsOrm:
        async with async_session() as session:
            query = select(TopicsOrm).where(TopicsOrm.order == order)
            result = await session.execute(query)
            topic = result.scalar_one_or_none()
        return topic if topic else None

    @staticmethod
    async def create_topic(topic: topic_schema.TopicInCreate) -> TopicsOrm:
        try:
            async with async_session() as session:
                query = insert(TopicsOrm).values(**topic.dict())
                result = await session.execute(query)
                await session.commit()
                created_topic = result.inserted_primary_key
                created_topic_data = await session.get(TopicsOrm, created_topic[0])
            return created_topic_data if created_topic_data else None
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def update_topic(topic_id: int, topic: topic_schema.TopicInUpdate):
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
                updated_topic = result.scalar_one_or_none()
            return updated_topic if updated_topic else None
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

    @staticmethod
    async def get_all_topics():
        async with async_session() as session:
            query = select(TopicsOrm).order_by(TopicsOrm.order)
            result = await session.execute(query)
            db_topics = result.scalars().all()
        return db_topics
