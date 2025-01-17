from typing import List, Any

from pydantic import BaseModel

from watchmen.common.mongo_model import MongoModel


class ConnectedSpaceBlockGraphics(BaseModel):
    rect: Any = None


class TopicGraphics(ConnectedSpaceBlockGraphics):
    topicId: str = None


class SubjectGraphics(ConnectedSpaceBlockGraphics):
    subjectId: str = None


class ConnectedSpaceGraphics(MongoModel):
    connectId: str = None
    topics: List[TopicGraphics]
    subjects: List[SubjectGraphics]
    userId: str = None
