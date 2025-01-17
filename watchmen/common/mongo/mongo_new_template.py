import logging

import pymongo
from bson import regex, ObjectId

from watchmen.common.data_page import DataPage
from watchmen.common.mongo.index import build_code_options
from watchmen.common.mysql.model.table_definition import get_primary_key
from watchmen.common.storage.engine.storage_engine import get_client
from watchmen.common.utils.data_utils import build_data_pages, build_collection_name

client = get_client()

log = logging.getLogger("app." + __name__)

log.info("mongo template initialized")

'''
Build where, the common sql pattern is "column_name operator value", but we use dict,
so the pattern is {column_name: {operator: value}}. 

if operator is =, then can use {column_name: value}

About and|or , use 
    {"and": List(
                            {column_name1: {operator: value}}
                            {column_name2: {operator: value}}
                )
    }
    
support Nested:
    {"or": List(
                            {column_name1: {operator: value}}
                            {column_name2: {operator: value}}
                            {"and": List(
                                                    {column_name3:{operator: value}}
                                                    {column_name4:{operator: value}}
                                        )
                            }
                )
    }
'''


def build_mongo_where_expression(where: dict):
    for key, value in where.items():
        if key == "and" or key == "or":
            if isinstance(value, list):
                filters = []
                for express in value:
                    result = build_mongo_where_expression(express)
                    filters.append(result)
            if key == "and":
                return {"$and": filters}
            if key == "or":
                return {"$or": filters}
        else:
            if isinstance(value, dict):
                for k, v in value.items():
                    if k == "=":
                        return {key: {"$eq": v}}
                    if k == "like":
                        return {key: regex.Regex(v)}
                    if k == "in":
                        return {key: {"$in": v}}
                    if k == ">":
                        return {key: {"$gt": v}}
                    if k == ">=":
                        return {key: {"$gte": v}}
                    if k == "<":
                        return {key: {"$lt": v}}
                    if k == "<=":
                        return {key: {"$lte": v}}
                    if k == "between":
                        if (isinstance(v, tuple)) and len(v) == 2:
                            return {key: {"$gte": v[0], "$lt": v[1]}}
            else:
                return {key: {"$eq": value}}


def build_mongo_order(order_: list):
    result = []
    for item in order_:
        if isinstance(item, tuple):
            if item[1] == "desc":
                new_ = (item[0], pymongo.DESCENDING)
                result.append(new_)
            if item[1] == "asc":
                new_ = (item[0], pymongo.ASCENDING)
                result.append(new_)
    return result


def insert_one(one, model, name):
    collection = client.get_collection(name)
    collection.insert_one(__convert_to_dict(one))
    return model.parse_obj(one)


def insert_all(data, model, name):
    collection = client.get_collection(name)
    collection.insert_many(__convert_to_dict(data))


def update_one(one, model, name) -> any:
    collection = client.get_collection(name)
    primary_key = get_primary_key(name)
    one_dict = __convert_to_dict(one)
    query_dict = {primary_key: one_dict.get(primary_key)}
    collection.update_one(query_dict, {"$set": one_dict})
    return model.parse_obj(one)


def update_one_first(where, updates, model, name):
    collection = client.get_collection(name)
    query_dict = build_mongo_where_expression(where)
    collection.update_one(query_dict, {"$set": __convert_to_dict(updates)})
    return model.parse_obj(updates)


# equal create_or_update, To avoid multiple upserts, ensure that the filter fields are uniquely indexed.
def upsert_(where, updates, model, name):
    collections = client.get_collection(name)
    collections.update_one(where, {"$set": __convert_to_dict(updates)}, upsert=True)
    return model.parse_obj(updates)


def update_(where, updates, model, name):
    collection = client.get_collection(name)
    collection.update_many(build_mongo_where_expression(where), {"$set": __convert_to_dict(updates)})


def delete_one(id_, name):
    collection = client.get_collection(name)
    key = get_primary_key(name)
    collection.delete_one({key: id_})


def delete_(where, model, name):
    collection = client.get_collection(name)
    collection.delete_many(build_mongo_where_expression(where))


def find_by_id(id_, model, name):
    collections = client.get_collection(name)
    primary_key = get_primary_key(name)
    result = collections.find_one({primary_key: id_})
    if result is None:
        return
    else:
        return model.parse_obj(result)


def find_one(where: dict, model, name: str):
    collection = client.get_collection(name)
    result = collection.find_one(build_mongo_where_expression(where))
    if result is None:
        return
    else:
        return model.parse_obj(result)


def find_(where: dict, model, name: str) -> list:
    collection = client.get_collection(name)
    cursor = collection.find(build_mongo_where_expression(where))
    result_list = list(cursor)
    return [model.parse_obj(result) for result in result_list]


def exists(where, model, name):
    collection = client.get_collection(name)
    result = collection.find_one(where)
    if result is None:
        return False
    else:
        return True


def list_all(model, name: str):
    collection = client.get_collection(name)
    cursor = collection.find()
    result_list = list(cursor)
    return [model.parse_obj(result) for result in result_list]


def list_(where, model, name: str) -> list:
    collection = client.get_collection(name)
    cursor = collection.find(where)
    result_list = list(cursor)
    return [model.parse_obj(result) for result in result_list]


def page_all(sort, pageable, model, name) -> DataPage:
    codec_options = build_code_options()
    collection = client.get_collection(name, codec_options=codec_options)
    total = collection.find().count()
    skips = pageable.pageSize * (pageable.pageNumber - 1)
    cursor = collection.find().skip(skips).limit(pageable.pageSize).sort(build_mongo_order(sort))
    return build_data_pages(pageable, [model.parse_obj(result) for result in list(cursor)], total)


def page_(where, sort, pageable, model, name) -> DataPage:
    codec_options = build_code_options()
    collection = client.get_collection(name, codec_options=codec_options)

    mongo_where = build_mongo_where_expression(where)
    #print(mongo_where)
    total = collection.find(mongo_where).count()
    skips = pageable.pageSize * (pageable.pageNumber - 1)
    if sort is not None:
        cursor = collection.find(mongo_where).skip(skips).limit(pageable.pageSize).sort(
            build_mongo_order(sort))
    else:
        cursor = collection.find(mongo_where).skip(skips).limit(pageable.pageSize)
    if model is not None:
        return build_data_pages(pageable, [model.parse_obj(result) for result in list(cursor)], total)
    else:
        return build_data_pages(pageable, list(cursor), total)


def __convert_to_dict(instance) -> dict:
    if type(instance) is not dict:
        return instance.dict()
    else:
        return instance


def find_one_and_update(where: dict, updates: dict, name: str):
    codec_options = build_code_options()
    collection = client.get_collection(name, codec_options=codec_options)
    return collection.find_one_and_update(filter=build_mongo_where_expression(where), update=updates, upsert=True)


'''
for topic data impl
'''


# save_topic_instance, insert one
def topic_data_insert_one(one, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    topic_data_col.insert(one)
    return topic_name, one


# save_topic_instances, insert many
def topic_data_insert_(data, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    topic_data_col.insert_many(data)


def topic_data_update_one(id_, one, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    topic_data_col.update_one({"_id": ObjectId(id_)}, {"$set": one})


def topic_data_find_by_id(id_, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    result = topic_data_col.find_one({"_id": ObjectId(id_)})
    return result


def topic_data_find_one(where, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    return topic_data_col.find_one(where)


def topic_data_find_(where, topic_name):
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    return topic_data_col.find(where)


def topic_data_list_all(topic_name) -> list:
    codec_options = build_code_options()
    topic_data_col = client.get_collection(build_collection_name(topic_name), codec_options=codec_options)
    result = topic_data_col.find()
    return list(result)


def topic_find_one_and_update(where: dict, updates: dict, name: str):
    codec_options = build_code_options()
    collection = client.get_collection(build_collection_name(name), codec_options=codec_options)
    return collection.find_one_and_update(filter=build_mongo_where_expression(where), update=updates, upsert=True)
