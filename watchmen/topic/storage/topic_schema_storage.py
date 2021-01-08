from bson import regex

from watchmen.common.pagination import Pagination
from watchmen.common.storage.engine.storage_engine import get_client
from watchmen.common.utils.data_utils import WATCHMEN, build_data_pages
from watchmen.topic.topic import Topic

db = get_client(WATCHMEN)

topic_col = db.get_collection('topic')


def save_topic(topic):
    return topic_col.insert_one(topic)


def get_topic_by_name(topic_name):
    return topic_col.find_one("topic_name", topic_name)


def get_topic_by_id(topic_id):
    return topic_col.find_one({"topicId":topic_id})


def get_topic_list_by_ids(topic_ids):
    # print(topic_ids)
    return topic_col.find({"_id": {"$in": topic_ids}})


def topic_dict_to_object(topic_schema_dict):
    topic = Topic()
    return topic


def query_topic_list_with_pagination(query_name: str, pagination: Pagination):
    item_count = topic_col.find({"name": regex.Regex(query_name)}).count()
    skips = pagination.pageSize * (pagination.pageNumber - 1)
    result = topic_col.find({"name": regex.Regex(query_name)}).skip(skips).limit(pagination.pageSize)
    return build_data_pages(pagination, list(result),item_count)


def update_topic(topic_id, topic: Topic):
    return topic_col.update_one({"topicId": topic_id}, {"$set": topic})
