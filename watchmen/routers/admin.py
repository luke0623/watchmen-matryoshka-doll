
from fastapi import APIRouter
from pydantic import BaseModel

from watchmen.factors.model.topic import Topic
from watchmen.index import select_domain, generate_suggestion_topic_service, generate_suggestion_factor, \
    save_topic_mapping, load_topic_mapping, SpaceOut, load_space_topic_list
from watchmen.lake.model_schema import ModelSchema
from watchmen.lake.model_schema_set import ModelSchemaSet
from watchmen.mapping.topic_mapping_rule import TopicMappingRule
from watchmen.master.master_space import MasterSpace

router = APIRouter()


class TopicSuggestionIn(BaseModel):
    lake_schema_set: ModelSchemaSet = None
    master_schema: MasterSpace = None


class FactorSuggestionIn(BaseModel):
    lake_schema: ModelSchema = None
    topic: Topic = None


@router.get("/select/domain", tags=["admin"], response_model=MasterSpace)
async def domain(name: str):
    return select_domain(name)


@router.post("/suggestion/topic",tags=["admin"],)
async def generate_suggestion_topic(topic_suggestion: TopicSuggestionIn):
    return generate_suggestion_topic_service(topic_suggestion.lake_schema, topic_suggestion.master_schema)


@router.post("/suggestion/factors",tags=["admin"],)
async def generate_suggestion_factor(factor_suggestion: FactorSuggestionIn):
    return generate_suggestion_factor(factor_suggestion.lake_schema, factor_suggestion.topic)


@router.post("/mapping/topic",tags=["admin"],)
async def save_topic_mapping_http(topic_mapping_rule:TopicMappingRule):
    return save_topic_mapping(topic_mapping_rule)


@router.get("/mapping/topic",tags=["admin"], response_model=TopicMappingRule)
async def load_topic_mapping_http(temp_topic_name:str,topic_name:str):
    return load_topic_mapping(temp_topic_name,topic_name)


@router.get("/space", tags=["admin"],response_model=SpaceOut)
async def load_space_topic_list_http(space_name:str):
    return load_space_topic_list(space_name)