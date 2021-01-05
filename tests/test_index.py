import json
import logging

from bson import ObjectId

from watchmen.connector.local_connector import raw_data_load
from watchmen.index import select_domain, save_topic_mapping, generate_raw_data_schema
from watchmen.pipeline.mapping.mapping_rule import MappingRule
from watchmen.pipeline.mapping.mapping_rule_storage import load_topic_mapping_by_name, load_topic_mapping_by_id
from watchmen.pipeline.mapping.suggestion.generate_suggestion import generate_topic_suggestion, \
    generate_factor_suggestion
from watchmen.pipeline.mapping.topic_mapping_rule import TopicMappingRule
from watchmen.raw_data_back.model_field import ModelField
from watchmen.raw_data_back.storage.row_schema_storage import load_raw_schema_by_code
from watchmen.space.storage.space_storage import load_space_by_name
from watchmen.topic.factor.factor import Factor
from watchmen.topic.storage.topic_schema_storage import get_topic_list_by_ids


def test_select_domain():
    master_space = select_domain("insurance")
    assert master_space is not None


def test_import_raw_data_list():
    pass


def test_import_instance_data():
    logging.debug("tst start")
    generate_raw_data_schema([raw_data_load('../assert/data/policy.json'), raw_data_load('../assert/data/policy.json')],
                             "policy")


def test_save_topic_mapping_rule():
    topic_mapping_rule = TopicMappingRule()
    topic_mapping_rule.targetTopicId = "123"
    topic_mapping_rule.sourceTopicId = "235"
    topic_mapping_rule.targetTopicName = "test1"
    topic_mapping_rule.sourceTopicName = "test"
    factor_mapping_rule = MappingRule()
    factor_mapping_rule.isBucket = True
    factor_mapping_rule.masterFactor = Factor()
    factor_mapping_rule.lateField = ModelField()
    topic_mapping_rule.factor_rules["DD"] = factor_mapping_rule
    save_topic_mapping(topic_mapping_rule)


def test_generate_factor_suggestion():
    lake_schema = load_raw_schema_by_code("policy")
    master_schema = load_space_by_name("mock_insurance")
    topic_id_list = master_schema.topic_id_list
    object_ids = map(lambda x: ObjectId(x), topic_id_list)
    topic_list = get_topic_list_by_ids(list(object_ids))

    model_schema = lake_schema.schemas["policy"]

    # for topic in topic_list:
    #     print(topic)

    matches = (topic for topic in topic_list if topic['topic_name'] == "policy")
    # master_schema.topic_id_list

    for match_topic in list(matches):
        results = generate_factor_suggestion(model_schema, match_topic)
        # print(results)
        print(json.dumps(results))
    # lake_schema.


def test_load_topic_mapping_rule():
    print(load_topic_mapping_by_id("123", "235"))


def test_load_topic_mapping_rule():
    print(load_topic_mapping_by_name("test", "test1"))


def test_generate_suggestion():
    lake_schema = load_raw_schema_by_code("policy")
    master_schema = load_space_by_name("mock_insurance")
    topic_id_list = master_schema.topic_id_list
    object_ids = map(lambda x: ObjectId(x), topic_id_list)
    topic_list = get_topic_list_by_ids(list(object_ids))
    print(json.dumps(generate_topic_suggestion(lake_schema, topic_list)))


# def test_generate_suggestion_factor():
#     lake_schema = load_data_schema_by_code("policy")
#     master_schema = load_master_space_by_name("mock_insurance")
#     topic_id_list = master_schema.topic_id_list
#     object_ids = map(lambda x: ObjectId(x), topic_id_list)
#     topic_list = get_topic_list_by_ids(list(object_ids))
#     print(json.dumps(generate_topic_suggestion(lake_schema,topic_list)))


def test_object_to_json():
    data = {
        "topicId": '1', "code": 'quotation', "name": 'Quotation', "type": "distinct",
        "raw": False,

        "factors": [
            {
                "factorId": '101',
                "name": 'quotationId',
                "label": 'Quotation Sequence',
                "type": "sequence"
            },

            {
                "factorId": '103',
                "name": 'quoteDate',
                "label": 'Quotation Create Date',
                "type": "datetime"
            }
        ]
    }




    # print()
