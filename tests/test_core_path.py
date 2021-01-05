from bson import ObjectId

from watchmen.common.log import log
from watchmen.connector.local_connector import raw_data_load
from watchmen.pipeline.single.pipeline_service import run_pipeline, build_pipeline
from watchmen.raw_data_back.model_schema import Domain
from watchmen.raw_data_back.service.import_data import process_raw_data, import_raw_data
from watchmen.raw_data_back.storage.row_schema_storage import load_raw_schema_by_code
from watchmen.raw_data_back.service.generate_schema import generate_basic_schema_for_list_data
from watchmen.routers.admin import create_topic
from watchmen.space.service.admin import save_space, load_space, add_topic_to_space, update_topic_in_space
from watchmen.space.space import Space
from watchmen.common.utils.copy import direct_copy_raw_schema_to_topic
import logging
import os

from watchmen.topic.service.topic_service import query_topic_schema, create_topic_schema, update_topic_schema
from watchmen.topic.storage.topic_schema_storage import get_topic_list_like_topic_name, update_topic
from watchmen.topic.topic import Topic




def test_create_space():
    logging.error("tst start")
    space = Space()
    space.name="test_demo"
    save_space(space)


def __build_json_list(files_name,path):
    json_list = []
    for filename in files_name:
        full_path = path+"/"+filename
        if os.path.isfile(full_path):
            json_list.append(raw_data_load(full_path))

    return json_list


def test_import_raw_data_list():
    path = '/Users/yifeng/PycharmProjects/ebaogi-data-collection/collection_data/PGA'
    files_name = os.listdir(path)
    json_list = __build_json_list(files_name,path)
    # node = generate_schema_for_list_data("4.5-sit-policy",json_list)
    # print(node)
    #
    # assert node is not None


def export_http_api_for_raw_data():


    pass





def test_create_target_topic():
    pass



def test_add_topic_to_space():
    space = load_space("test_demo")
    assert space is not None
    model_schema_set = load_raw_schema_by_code("policy")
    policy_topic = model_schema_set.schemas["policy"]
    topic = direct_copy_raw_schema_to_topic(policy_topic,None)
    add_topic_to_space(topic,space)


def test_update_topic_in_space():
    space = load_space("test_demo")
    model_schema_set = load_raw_schema_by_code("policy")
    policy_topic = model_schema_set.schemas["policy"]
    topic = direct_copy_raw_schema_to_topic(policy_topic, None)
    topic.alias=["test1"]
    return update_topic_in_space(topic, space)


def test_process_raw_data():
    model_schema_set = load_raw_schema_by_code("policy")
    process_raw_data(raw_data_load('../assert/data/policy.json'),model_schema_set,None)


def test_build_pipeline():
    stage_list = [{"name": "split_topic_by_schema", "parameter": {"split_factor": "PolicyStatus","filter_factor":"policy","split_factor_value":2}},
                  {"name": "mapping_to_topic", "parameter": {"mapping_rules": "PolicyId"}},
                  {"name": "insert_topic", "parameter": {"merge_key": "PolicyId","topic_name":"policy"}}]

    entity_set = import_raw_data(raw_data_load('../assert/data/policy.json'), load_raw_schema_by_code("policy"), None)


    # stage
    # tage("split_topic_by_schema", {"da", "da"})]  stage_list=[S
    pipeline = build_pipeline(stage_list)

    run_pipeline(pipeline, {"data": entity_set})



def test_build_aggregate_pipeline():
    pass



### user


def call_raw_data_collection_api():
    ## call api save raw data
    ## trigger pipeline
    pass


def test_create_subject():
    pass


def test_create_dataset():
    pass


def test_create_report():
    ## create a report query
    pass


def test_run_report():
    pass
    #load_raw_schema(name)

    #find policy schema

    # add topic to space

    # save to space


def test_create_topic():
    log.init()
    topic = {
        "topicId": '1', "code": 'quotation', "name": 'Quota', "type": "distinct",
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

    topic = Topic.parse_obj(topic)
    print(topic.json())
    result = create_topic_schema(topic)

    assert result["_id"] is not None
    # return result


def test_query_topic_list():
    query_name = "Quota"
    data_list = query_topic_schema(query_name)
    print(data_list)


def test_update_topic():
    topic = {
        "topicId": 796064005360713728, "code": 'quotation', "name": 'Quota2222', "type": "distinct",
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

    topic = Topic.parse_obj(topic)
    # data = topic.dict()

    # data["_id"]= ObjectId("5ff415ce2be5eaebbdd08b95")

    topicId = 796064005360713728
    update_topic_schema(topicId,topic)
    # create_topic_schema(data)






