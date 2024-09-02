from fastapi.responses import JSONResponse
import src.db.schemas.students.topics as topic_schema
from src.cruds.topic import TopicCRUD


class TopicService:
    @staticmethod
    async def add_new_topic(topic: topic_schema.TopicInCreate):
        db_topic = await TopicCRUD.get_topic_by_name(topic.name)
        all_topics = await TopicCRUD.get_all_topics()
        if db_topic:
            return JSONResponse(content={"message": "Topic already exists"}, status_code=400)
        topic.order = len(all_topics) + 1
        topic = await TopicCRUD.create_topic(topic)
        return topic

    @staticmethod
    async def update_topic(topic_id: int, topic: topic_schema.TopicInUpdate):
        db_topic = await TopicCRUD.get_topic_by_id(topic_id)
        if not db_topic:
            return JSONResponse(content={"message": "Topic does not exists"}, status_code=404)

        new_topic = await TopicCRUD.update_topic(topic_id, topic)
        return new_topic

    @staticmethod
    async def get_topic_by_id(topic_id: int):
        db_topic = await TopicCRUD.get_topic_by_id(topic_id)
        if not db_topic:
            return JSONResponse(content={"message": "Topic does not exists"}, status_code=404)
        return db_topic

    @staticmethod
    async def get_topic_with_details(topic_id: int):
        db_topic = await TopicCRUD.get_topics_by_details(topic_id)
        if not db_topic:
            return JSONResponse(content={"message": "Topic does not exists"}, status_code=404)
        return db_topic

    @staticmethod
    async def delete_topic(topic_id: int):
        db_topic = await TopicCRUD.get_topic_by_id(topic_id)
        if not db_topic:
            return JSONResponse(content={"message": "Topic does not exists"}, status_code=404)

        topic = await TopicCRUD.delete_topic(topic_id)
        return topic

    @staticmethod
    async def change_order(new_order: int, topic_id: int):
        try:
            topic_to_move = await TopicCRUD.get_topic_by_id(topic_id)
            if not topic_to_move:
                return JSONResponse(content={"message": "Topic not found"}, status_code=404)

            all_topics = await TopicCRUD.get_all_topics()

            if new_order < 1 or new_order > len(all_topics):
                return JSONResponse(content={"message": "Invalid new order"}, status_code=400)

            if topic_to_move.order == new_order:
                return JSONResponse(content={"message": "Topic is already in the requested order"}, status_code=200)
            is_moving_up = new_order < topic_to_move.order
            for topic in all_topics:
                if is_moving_up:
                    if new_order <= topic.order < topic_to_move.order:
                        await TopicCRUD.update_topic(topic.id, topic_schema.TopicInUpdate(order=topic.order + 1))
                else:
                    if topic_to_move.order < topic.order <= new_order:
                        await TopicCRUD.update_topic(topic.id, topic_schema.TopicInUpdate(order=topic.order - 1))

            await TopicCRUD.update_topic(topic_id, topic_schema.TopicInUpdate(order=new_order))

            return JSONResponse(content={"message": "Topic order updated successfully"}, status_code=200)

        except Exception as e:
            print(f"Error in change_order: {str(e)}")
            return JSONResponse(content={"message": "An error occurred while changing the topic order"},
                                status_code=500)
