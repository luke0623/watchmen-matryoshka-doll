import json

from lib.match.lexicon_matcher import lexicon_match
from lib.model.model_field import ModelField, FieldType
from lib.model.model_relationship import ModelRelationship, RelationshipType
from lib.model.model_schema import ModelSchema, Domain

ROOT = "root"


def __is_field_value(value):
    return type(value) != dict and type(value) != list


def __process_sub_models(key: str, sub_models: list, sub_model_schema: ModelSchema):
    for data in sub_models:
        result = __generate_sub_model(key, data, sub_model_schema)
        relationship = ModelRelationship()
        relationship.modelSchema = result
        relationship.type = RelationshipType.OneToMany
        if result is not None:
            sub_model_schema.relationships[key] = result


def __build_model_fields(key: str, value):
    model_field = ModelField()
    model_field.value.append(value)
    if type(value) == int or type(value) == float:
        model_field.name = key
        model_field.type = FieldType.NUM
    if type(value) == str:
        model_field.name = key
        model_field.type = FieldType.STR

    return model_field


def __generate_sub_model(key: str, sub_model: json, sub_model_schema: ModelSchema):
    sub_model_schema.name = key  # TODO add logic for key check
    process_attrs(sub_model, sub_model_schema)
    sub_model_schema.lexiconMatch = lexicon_match(sub_model_schema)
    return sub_model_schema


def __generate_root(key: str, data: json,domain:Domain):
    model_schema = ModelSchema()
    if key is None:
        model_schema.name = ROOT
    else:
        model_schema.name = key

    model_schema.domain = domain
    process_attrs(data, model_schema)
    # value content match
    model_schema.lexiconMatch=lexicon_match(model_schema)
    return model_schema


def process_attrs(data, model_schema):
    for key, value in data.items():
        if __is_field_value(value):
            model_field = __build_model_fields(key, value)
            # print (key in model_schema.businessFields)
            if key in model_schema.businessFields:
                model_schema.businessFields[key].value.append(value)
            else:
                model_schema.businessFields[key] = model_field
        else:
            # process sub model
            sub_model_schema = ModelSchema()
            relationship = ModelRelationship()
            if type(value) == dict or type(value) == list:
                for sub_model in value:
                    sub_model_schema = __generate_sub_model(key, sub_model, sub_model_schema)
                    if sub_model_schema is not None:
                        relationship.type = RelationshipType.OneToMany
                        relationship.modelSchema = sub_model_schema
                        # if key in model_schema.relationships:
                        model_schema.relationships[key] = relationship
            else:
                sub_model_schema = __generate_sub_model(key, value, sub_model_schema)
                if sub_model_schema is not None:
                    relationship.type = RelationshipType.OneToOne
                    relationship.modelSchema = sub_model_schema
                    model_schema.relationships[key] = relationship


def __find_sub_models(root: json):
    return []


def __filter_sub_models(model):
    return []


def __process_fields(fileds: []):
    # TODO return similar fields list and scope
    return {}


def __create_links():
    pass


def generate_basic_schema(key: str, data: json,domain:Domain):
    root = __generate_root(key, data,domain)

    print(root.json())

    return root

    # TODO  match domain topic

    # TODO match entity  and lexicon

    # TODO add entity extensions data collector

    # fields = __filter_sub_models(root)
    similar_fields = __process_fields(fields)
    sub_models = __find_sub_models(root)

    ##

    # match root schema
    # find sub model
    # recursion sub model
    # match lexicon
    # match entity schema
    # pass


def save_schema(data: json):
    pass


def __bind_lexicon_to_schema():
    pass


def __bind_entity_to_schema():
    pass
