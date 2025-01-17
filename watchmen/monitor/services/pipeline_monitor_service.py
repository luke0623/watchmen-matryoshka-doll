# from watchmen.pipeline.index import trigger_pipeline
import watchmen.pipeline.index
from watchmen.collection.model.topic_event import TopicEvent
from watchmen.common.constants import pipeline_constants
from watchmen.monitor.model.pipeline_monitor import PipelineRunStatus
from watchmen.pipeline.model.trigger_type import TriggerType
from watchmen.pipeline.single.stage.unit.utils.units_func import add_audit_columns, INSERT
from watchmen.topic.storage.topic_data_storage import save_topic_instance
from watchmen.topic.storage.topic_schema_storage import get_topic


def sync_pipeline_monitor_data(pipeline_monitor: PipelineRunStatus):
    topic_event = TopicEvent(code="raw_pipeline_monitor", data=pipeline_monitor.dict())
    # asyncio.ensure_future(import_raw_topic_data(topic_event))

    topic = get_topic(topic_event.code)
    if topic is None:
        raise Exception("topic name does not exist")

    add_audit_columns(topic_event.data, INSERT)
    save_topic_instance(topic_event.code, topic_event.data)
    watchmen.pipeline.index.trigger_pipeline(topic_event.code,
                                             {pipeline_constants.NEW: topic_event.data, pipeline_constants.OLD: None},
                                             TriggerType.insert)
