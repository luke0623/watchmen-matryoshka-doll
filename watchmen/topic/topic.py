from enum import Enum
from typing import List

from watchmen.common.mongo_model import MongoModel
from watchmen.topic.factor.factor import Factor


class TopicType(Enum):
    RAW = "raw",
    DISTINCT = "distinct",
    AGGREGATE = "aggregate",
    TIME = "time",
    RATIO = "ratio",
    NOT_DEFINED = "not-defined",
    SYSTEM = "system"


class Topic(MongoModel):
    topicId: str = None
    name: str = None
    # code: str = None
    type: str = None
    kind: str = None
    factors: List[Factor] = []
    description: str = None
    # factorIds: list = []

    '''
    indexKey : List[str] = None
    isUnification:bool = False

    '''
