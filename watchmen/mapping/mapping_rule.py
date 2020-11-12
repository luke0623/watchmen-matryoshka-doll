from pydantic import BaseModel

from watchmen.factors.model.factor import Factor
from watchmen.lake.model_field import ModelField


class MappingRule(BaseModel):
    mappingId: str = None
    masterFactor: Factor = None
    lateField:ModelField = None
    hasCodeMapping: bool = False
    codeRule: dict = None
    isBucket: bool = False
    bucketRule: dict = None
    extractRule: str = None